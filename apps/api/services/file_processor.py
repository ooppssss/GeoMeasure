from pathlib import Path
import geopandas as gpd
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from fastkml import kml
from fastkml.features import Placemark


def process_kml(file_path: str) -> list[dict]:
    """
    Parse a KML file and extract all Placemark features.
    """

    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        kml_data = file.read()

    root = kml.KML()
    root.from_string(kml_data)

    features: list[dict] = []

    def extract_features(items) -> None:
        for item in items:

            if isinstance(item, Placemark):
                geometry = item.geometry

                features.append(
                    {
                        "id": len(features),
                        "name": item.name,
                        "geometry_type": (
                            geometry.geom_type
                            if geometry is not None
                            else None
                        ),
                        "geometry": geometry,
                    }
                )

            elif hasattr(item, "features"):
                extract_features(item.features)

    extract_features(root.features)

    return features


def process_shapefile(zip_path: str) -> list[dict]:
    """
    Extract a Shapefile from a ZIP and return its features.
    """

    with TemporaryDirectory() as temp_dir:

        with ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(temp_dir)

        shapefiles = list(Path(temp_dir).rglob("*.shp"))

        if not shapefiles:
            raise ValueError(
                "ZIP file does not contain a Shapefile"
            )

        if len(shapefiles) > 1:
            raise ValueError(
                "ZIP file contains multiple Shapefiles"
            )

        gdf = gpd.read_file(shapefiles[0])

        features = []

        for index, row in gdf.iterrows():
            geometry = row.geometry

            properties = row.drop("geometry").to_dict()

            features.append(
                {
                    "id": index,
                    "geometry_type": (
                        geometry.geom_type
                        if geometry is not None
                        else None
                    ),
                    "geometry": geometry,
                    "properties": properties,
                }
            )

        return features
