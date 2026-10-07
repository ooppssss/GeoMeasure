from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import geopandas as gpd


def process_kml(file_path: str) -> gpd.GeoDataFrame:
    """
    Read a KML file and return it as a GeoDataFrame.
    """

    gdf = gpd.read_file(file_path, driver="KML")

    if gdf.empty:
        raise ValueError("No features found in KML file")

    return gdf


def process_shapefile(zip_path: str) -> gpd.GeoDataFrame:
    """
    Extract a Shapefile from a ZIP archive and return it
    as a GeoDataFrame.
    """

    with TemporaryDirectory() as temp_dir:

        with ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(temp_dir)

        shapefiles = list(
            Path(temp_dir).rglob("*.shp")
        )

        if not shapefiles:
            raise ValueError(
                "ZIP file does not contain a Shapefile"
            )

        if len(shapefiles) > 1:
            raise ValueError(
                "ZIP file contains multiple Shapefiles"
            )

        return gpd.read_file(shapefiles[0])