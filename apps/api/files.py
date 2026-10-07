from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, UploadFile

from apps.api.services.crs import transform_to_projected
from apps.api.services.file_processor import (
    process_kml,
    process_shapefile,
)
from apps.api.services.file_store import get_file, save_file
from apps.api.services.measurement import calculate_measurement


router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/api/files/")
async def upload_file(
    geo_file: Annotated[UploadFile, File()]
):
    if geo_file.filename is None:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing",
        )

    extension = Path(geo_file.filename).suffix.lower()

    if extension not in [".kml", ".zip"]:
        raise HTTPException(
            status_code=400,
            detail="File type is not supported",
        )

    file_path = UPLOAD_DIR / geo_file.filename

    with file_path.open("wb") as file:
        file.write(await geo_file.read())

    try:
        if extension == ".kml":
            gdf = process_kml(str(file_path))
        else:
            gdf = process_shapefile(str(file_path))

        projected_gdf = transform_to_projected(gdf)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )

    features = []

    for index, row in projected_gdf.iterrows():
        geometry = row.geometry

        measurement = calculate_measurement(geometry)

        features.append(
            {
                "id": index,
                "geometry_type": geometry.geom_type,
                "measurement": measurement,
                "properties": {
                    key: value
                    for key, value in row.items()
                    if key != "geometry"
                },
            }
        )

    processed_file = save_file(
        filename=geo_file.filename,
        feature_count=len(projected_gdf),
        source_crs=str(gdf.crs),
        measurement_crs=str(projected_gdf.crs),
        features=features,
    )

    return {
        "id": processed_file.id,
        "message": "File processed successfully",
        "filename": processed_file.filename,
        "feature_count": processed_file.feature_count,
        "source_crs": processed_file.source_crs,
        "measurement_crs": processed_file.measurement_crs,
    }


@router.get("/api/files/{file_id}/")
def get_file_details(file_id: int):
    processed_file = get_file(file_id)

    if processed_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return {
        "id": processed_file.id,
        "filename": processed_file.filename,
        "feature_count": processed_file.feature_count,
        "source_crs": processed_file.source_crs,
        "measurement_crs": processed_file.measurement_crs,
    }


@router.get("/api/files/{file_id}/measurements/")
def get_file_measurements(file_id: int):
    processed_file = get_file(file_id)

    if processed_file is None:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return {
        "file_id": processed_file.id,
        "filename": processed_file.filename,
        "measurements": [
            {
                "id": feature["id"],
                "geometry_type": feature["geometry_type"],
                "measurement": feature["measurement"],
            }
            for feature in processed_file.features
        ],
    }