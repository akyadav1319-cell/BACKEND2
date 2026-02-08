"""
NPCC Data Module
Contains historical climate data, BAU projections, and policy cost constants
"""

from .mock_repository import (
    HISTORICAL_TEMPERATURE_DATA,
    BAU_PROJECTION,
    POLICY_COSTS,
    BASELINE_2026,
    BANKRUPTCY_THRESHOLD,
    SUSTAINABILITY_THRESHOLD,
    get_complete_trend_data
)

__all__ = [
    "HISTORICAL_TEMPERATURE_DATA",
    "BAU_PROJECTION",
    "POLICY_COSTS",
    "BASELINE_2026",
    "BANKRUPTCY_THRESHOLD",
    "SUSTAINABILITY_THRESHOLD",
    "get_complete_trend_data"
]