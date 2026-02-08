"""
NPCC Backend Package
National Policy Command Centre - Climate Policy Simulation Engine
"""

__version__ = "2.0.0"
__author__ = "NPCC Development Team"

from .core.engine import PolicyEngine
from .core.image_generator import UrbanImpactGenerator

__all__ = [
    "PolicyEngine",
    "UrbanImpactGenerator"
]