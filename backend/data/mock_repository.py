"""
Mock Data Repository for National Policy Command Centre
Provides historical climate data, BAU projections, and fiscal constants
"""

# Historical Global Temperature Anomalies (2000-2025)
# Baseline relative to 1850-1900 pre-industrial average
HISTORICAL_TEMPERATURE_DATA = [
    {"year": 2000, "anomaly": 0.62},
    {"year": 2001, "anomaly": 0.65},
    {"year": 2002, "anomaly": 0.68},
    {"year": 2003, "anomaly": 0.71},
    {"year": 2004, "anomaly": 0.66},
    {"year": 2005, "anomaly": 0.76},
    {"year": 2006, "anomaly": 0.73},
    {"year": 2007, "anomaly": 0.77},
    {"year": 2008, "anomaly": 0.64},
    {"year": 2009, "anomaly": 0.74},
    {"year": 2010, "anomaly": 0.82},
    {"year": 2011, "anomaly": 0.71},
    {"year": 2012, "anomaly": 0.75},
    {"year": 2013, "anomaly": 0.77},
    {"year": 2014, "anomaly": 0.86},
    {"year": 2015, "anomaly": 1.02},
    {"year": 2016, "anomaly": 1.09},
    {"year": 2017, "anomaly": 1.01},
    {"year": 2018, "anomaly": 0.95},
    {"year": 2019, "anomaly": 1.08},
    {"year": 2020, "anomaly": 1.15},
    {"year": 2021, "anomaly": 0.98},
    {"year": 2022, "anomaly": 1.04},
    {"year": 2023, "anomaly": 1.35},
    {"year": 2024, "anomaly": 1.38},
    {"year": 2025, "anomaly": 1.18},
]

# Business-As-Usual (BAU) Projection 2026-2050
# No policy intervention scenario - linear warming trend
BAU_PROJECTION = [
    {"year": 2026, "anomaly": 1.2},
    {"year": 2027, "anomaly": 1.25},
    {"year": 2028, "anomaly": 1.31},
    {"year": 2029, "anomaly": 1.36},
    {"year": 2030, "anomaly": 1.42},
    {"year": 2031, "anomaly": 1.47},
    {"year": 2032, "anomaly": 1.53},
    {"year": 2033, "anomaly": 1.58},
    {"year": 2034, "anomaly": 1.64},
    {"year": 2035, "anomaly": 1.69},
    {"year": 2036, "anomaly": 1.75},
    {"year": 2037, "anomaly": 1.80},
    {"year": 2038, "anomaly": 1.86},
    {"year": 2039, "anomaly": 1.91},
    {"year": 2040, "anomaly": 1.97},
    {"year": 2041, "anomaly": 2.02},
    {"year": 2042, "anomaly": 2.08},
    {"year": 2043, "anomaly": 2.13},
    {"year": 2044, "anomaly": 2.19},
    {"year": 2045, "anomaly": 2.24},
    {"year": 2046, "anomaly": 2.30},
    {"year": 2047, "anomaly": 2.35},
    {"year": 2048, "anomaly": 2.41},
    {"year": 2049, "anomaly": 2.46},
    {"year": 2050, "anomaly": 2.52},
]

# Fiscal Constants - Unit Costs for Policy Levers
# All values in $ Billion per percentage point of implementation
POLICY_COSTS = {
    "ev_adoption": {
        "cost_per_unit": 1.2,  # $1.2B per 1% EV adoption
        "temperature_impact": -0.0008,  # -0.0008°C per 1% adoption
        "max_impact": -0.08,  # Maximum -0.08°C at 100%
        "label": "EV Adoption Incentives",
        "description": "Subsidies, charging infrastructure, and manufacturer incentives"
    },
    "renewable_energy": {
        "cost_per_unit": 2.5,  # $2.5B per 1% renewable expansion
        "temperature_impact": -0.0012,  # -0.0012°C per 1%
        "max_impact": -0.12,  # Maximum -0.12°C at 100%
        "label": "Renewable Energy Expansion",
        "description": "Solar, wind, hydro infrastructure and grid upgrades"
    },
    "carbon_tax": {
        "cost_per_unit": -0.8,  # Revenue generating: -$0.8B per 1% (negative cost)
        "temperature_impact": -0.0015,  # -0.0015°C per 1%
        "max_impact": -0.15,  # Maximum -0.15°C at 100%
        "label": "Carbon Tax Implementation",
        "description": "Industrial emissions pricing and regulatory enforcement"
    },
    "reforestation": {
        "cost_per_unit": 0.6,  # $0.6B per 1% coverage
        "temperature_impact": -0.0005,  # -0.0005°C per 1%
        "max_impact": -0.05,  # Maximum -0.05°C at 100%
        "label": "Reforestation Programs",
        "description": "Tree planting, forest protection, and carbon sequestration"
    },
    "public_transport": {
        "cost_per_unit": 1.8,  # $1.8B per 1% expansion
        "temperature_impact": -0.0010,  # -0.0010°C per 1%
        "max_impact": -0.10,  # Maximum -0.10°C at 100%
        "label": "Public Transport Expansion",
        "description": "Mass transit infrastructure, bus networks, and rail systems"
    },
    "industrial_controls": {
        "cost_per_unit": 1.5,  # $1.5B per 1% regulation implementation
        "temperature_impact": -0.0013,  # -0.0013°C per 1%
        "max_impact": -0.13,  # Maximum -0.13°C at 100%
        "label": "Industrial Emission Controls",
        "description": "Factory regulations, emission standards, and monitoring systems"
    },
    "green_buildings": {
        "cost_per_unit": 1.0,  # $1.0B per 1% building retrofits
        "temperature_impact": -0.0007,  # -0.0007°C per 1%
        "max_impact": -0.07,  # Maximum -0.07°C at 100%
        "label": "Green Building Standards",
        "description": "Energy-efficient construction, retrofits, and building codes"
    },
    "waste_management": {
        "cost_per_unit": 0.8,  # $0.8B per 1% system improvement
        "temperature_impact": -0.0006,  # -0.0006°C per 1%
        "max_impact": -0.06,  # Maximum -0.06°C at 100%
        "label": "Waste Management & Recycling",
        "description": "Recycling programs, waste-to-energy, and landfill reduction"
    }
}

# Initial Baseline State (2026)
BASELINE_2026 = {
    "year": 2026,
    "temperature_anomaly": 1.2,
    "national_debt": 0,
    "policies": {
        "ev_adoption": 0,
        "renewable_energy": 0,
        "carbon_tax": 0,
        "reforestation": 0,
        "public_transport": 0,
        "industrial_controls": 0,
        "green_buildings": 0,
        "waste_management": 0
    }
}

# Economic Thresholds
BANKRUPTCY_THRESHOLD = 1000  # $1,000B national debt triggers collapse
SUSTAINABILITY_THRESHOLD = 1.5  # +1.5°C considered critical threshold

# Helper function to get complete trend data
def get_complete_trend_data():
    """Combine historical and BAU data for complete timeline"""
    return HISTORICAL_TEMPERATURE_DATA + BAU_PROJECTION