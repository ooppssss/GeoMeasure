from typing import Annotated
from pathlib import Path

from fastapi import FastAPI, UploadFile, File

from apps.api.services.file_processor import process_kml


app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/api/files")
async def read_files(
    geo_file: Annotated[UploadFile, File()]
):
    # Check that a filename was provided
    if geo_file.filename is None:
        return {"message": "Filename is missing"}

    # Determine the file extension
    extension = Path(geo_file.filename).suffix.lower()

    # Validate supported file types
    if extension not in [".kml", ".zip"]:
        return {"message": "File type is not supported"}

    # Create the path where the uploaded file will be stored
    file_path = UPLOAD_DIR / geo_file.filename

    # Save the uploaded file
    with file_path.open("wb") as file:
        file.write(await geo_file.read())

    # Process KML files
    if extension == ".kml":
        features = process_kml(str(file_path))

        return {
            "message": "KML file processed successfully",
            "features": features,
        }

    # ZIP/Shapefile processing will be implemented next
    return {
        "message": "ZIP file uploaded successfully",
        "filename": geo_file.filename,
    }