"""Benchmark metrics and metadata classes"""
import numpy as np
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    field_serializer,
)


class SemanticMetrics(BaseModel):
    """Semantic benchmark metric aggregator"""
    responses: list[str]
    exceptions: list[Exception]
    semantic_distances: list[np.float64]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_serializer('exceptions')
    def serialize_exceptions(self, excs: list[Exception]) -> list[str]:
        """Serializes exceptions in a compact name format"""
        return [type(exc).__name__ for exc in excs]

    @computed_field
    @property
    def mean_semantic_distance(self) -> np.float64:
        """Calculate mean semantic distance from result expectations"""
        return np.mean(self.semantic_distances)

    @computed_field
    @property
    def median_semantic_distance(self) -> np.float64:
        """Calculate median semantic distance from result expectation"""
        return np.median(self.semantic_distances)


class BenchmarkMetadata(BaseModel):
    """Core benchmark metadata/metrics class"""
    func: str
    iterations: int
    comparator: str
    expectation: str | None
    benchmarks: SemanticMetrics
