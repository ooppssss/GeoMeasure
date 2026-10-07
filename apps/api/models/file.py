from dataclasses import dataclass
from typing import Any


@dataclass
class ProcessedFile:
    id: int
    filename: str
    feature_count: int
    source_crs: str
    measurement_crs: str
    features: list[dict[str, Any]]