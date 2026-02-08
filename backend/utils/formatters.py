"""
Utility Functions for Data Formatting
Handles currency, percentages, and numerical sanitization
"""

def format_currency(value, decimals=2):
    """
    Format numerical value as currency string

    Args:
        value: Numerical value to format
        decimals: Number of decimal places (default: 2)

    Returns:
        Formatted string like "$123.45B" or "$1,234.56M"
    """
    abs_value = abs(value)

    if abs_value >= 1000:
        formatted = f"${abs_value / 1000:.{decimals}f}T"
    elif abs_value >= 1:
        formatted = f"${abs_value:.{decimals}f}B"
    else:
        formatted = f"${abs_value * 1000:.{decimals}f}M"

    # Add negative sign if applicable
    if value < 0:
        formatted = "-" + formatted

    return formatted


def format_percentage(value, decimals=1):
    """
    Format numerical value as percentage string

    Args:
        value: Numerical value to format (0-100 scale)
        decimals: Number of decimal places (default: 1)

    Returns:
        Formatted string like "45.5%"
    """
    return f"{value:.{decimals}f}%"


def format_temperature(value, decimals=2):
    """
    Format temperature anomaly with proper sign

    Args:
        value: Temperature anomaly value
        decimals: Number of decimal places (default: 2)

    Returns:
        Formatted string like "+1.25°C" or "-0.35°C"
    """
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{decimals}f}°C"


def sanitize_slider_value(value):
    """
    Sanitize and validate slider input (0-100 range)

    Args:
        value: Raw input value

    Returns:
        Clamped integer between 0 and 100
    """
    try:
        num_value = float(value)
        # Clamp between 0 and 100
        return max(0, min(100, int(num_value)))
    except (ValueError, TypeError):
        return 0


def calculate_efficiency_index(temperature_impact, fiscal_cost):
    """
    Calculate policy efficiency (temperature mitigation per billion spent)

    Args:
        temperature_impact: Temperature reduction in °C (negative value)
        fiscal_cost: Total cost in $ Billion

    Returns:
        Efficiency score (higher is better)
        Returns 0 if cost is 0 or negative (revenue-generating policies)
    """
    if fiscal_cost <= 0:
        # Revenue-generating policies get special handling
        return abs(temperature_impact) * 1000  # Bonus multiplier

    # Standard efficiency: °C reduced per $B spent
    efficiency = abs(temperature_impact) / fiscal_cost
    return round(efficiency * 1000, 2)  # Scale up for readability


def round_to_precision(value, precision=2):
    """
    Round value to specified decimal precision

    Args:
        value: Numerical value
        precision: Number of decimal places

    Returns:
        Rounded float
    """
    return round(float(value), precision)