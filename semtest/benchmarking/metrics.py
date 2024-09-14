"""Benchmark metrics and metadata classes"""
import numpy as np
from pydantic import BaseModel, Field, computed_field


class SemanticMetrics(BaseModel):
    """Semantic benchmark metric aggregator"""
    responses: list[str]
    exceptions: list[Exception]
    result_embeddings: list[list[float]] = Field(
        ..., exclude=True
    )
    semantic_distances: list[np.float64]

    class Config:
        """Semantic metrics configurations"""
        arbitrary_types_allowed = True
        json_encoders = {
            list[Exception]: lambda excs: [type(exc).__name__ for exc in excs]
        }

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
    expectation_input: str
    benchmarks: SemanticMetrics
