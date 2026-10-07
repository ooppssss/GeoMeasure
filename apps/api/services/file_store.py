from apps.api.models.file import ProcessedFile


files: dict[int, ProcessedFile] = {}

_next_id = 1


def save_file(
    filename: str,
    feature_count: int,
    source_crs: str,
    measurement_crs: str,
    features: list[dict],
) -> ProcessedFile:
    global _next_id

    processed_file = ProcessedFile(
        id=_next_id,
        filename=filename,
        feature_count=feature_count,
        source_crs=source_crs,
        measurement_crs=measurement_crs,
        features=features,
    )

    files[_next_id] = processed_file
    _next_id += 1

    return processed_file


def get_file(file_id: int) -> ProcessedFile | None:
    return files.get(file_id)