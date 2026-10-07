import geopandas as gpd


def get_projected_crs(gdf: gpd.GeoDataFrame):
    """
    Determine a suitable projected CRS for measurements.
    """

    if gdf.crs is None:
        raise ValueError("Input file does not contain a CRS")

    # If already projected, keep the existing CRS
    if not gdf.crs.is_geographic:
        return gdf.crs

    # Automatically select a suitable UTM CRS
    return gdf.estimate_utm_crs()


def transform_to_projected(
    gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Transform geometries to a suitable projected CRS.
    """

    projected_crs = get_projected_crs(gdf)

    return gdf.to_crs(projected_crs)