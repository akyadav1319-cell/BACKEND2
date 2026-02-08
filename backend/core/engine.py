"""
Policy Engine - Core Calculation Logic
Implements linear regression-style impact model for climate policies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.data.mock_repository import (
    POLICY_COSTS,
    BAU_PROJECTION,
    BASELINE_2026,
    BANKRUPTCY_THRESHOLD,
    get_complete_trend_data
)
from backend.utils.formatters import (
    format_currency,
    format_percentage,
    format_temperature,
    sanitize_slider_value,
    calculate_efficiency_index,
    round_to_precision
)


class PolicyEngine:
    """
    Core engine for calculating fiscal and climate impacts of policy decisions
    Uses linear regression model: Impact = Σ(policy_level * unit_impact)
    """

    def __init__(self):
        """Initialize the policy engine with baseline data"""
        self.policy_costs = POLICY_COSTS
        self.bau_projection = BAU_PROJECTION
        self.baseline = BASELINE_2026

    def calculate_impacts(self, policy_inputs):
        """
        Calculate total fiscal cost and temperature mitigation

        Args:
            policy_inputs: Dict with keys {ev_adoption, renewable_energy, carbon_tax,
                          reforestation, public_transport, industrial_controls,
                          green_buildings, waste_management}
                          Each value is 0-100 representing implementation level

        Returns:
            Dict containing:
                - total_cost: Total fiscal cost in $B
                - temperature_mitigation: Total °C reduction
                - policy_breakdown: Individual policy impacts
                - trend_line: Projected temperature trend (2026-2050)
                - fiscal_treemap: Budget allocation by policy
                - efficiency_index: Cost-effectiveness metrics per policy
                - bankruptcy_flag: True if national_debt > $1000B
        """
        # Sanitize inputs
        policies = {
            "ev_adoption": sanitize_slider_value(policy_inputs.get("ev_adoption", 0)),
            "renewable_energy": sanitize_slider_value(policy_inputs.get("renewable_energy", 0)),
            "carbon_tax": sanitize_slider_value(policy_inputs.get("carbon_tax", 0)),
            "reforestation": sanitize_slider_value(policy_inputs.get("reforestation", 0)),
            "public_transport": sanitize_slider_value(policy_inputs.get("public_transport", 0)),
            "industrial_controls": sanitize_slider_value(policy_inputs.get("industrial_controls", 0)),
            "green_buildings": sanitize_slider_value(policy_inputs.get("green_buildings", 0)),
            "waste_management": sanitize_slider_value(policy_inputs.get("waste_management", 0))
        }

        # Calculate individual policy impacts
        total_cost = 0
        total_temp_mitigation = 0
        policy_breakdown = []
        fiscal_treemap = []
        efficiency_metrics = []

        for policy_key, level in policies.items():
            if level == 0:
                continue

            policy_data = self.policy_costs[policy_key]

            # Linear impact calculation
            cost = policy_data["cost_per_unit"] * level
            temp_impact = policy_data["temperature_impact"] * level

            # Cap at maximum impact
            temp_impact = max(temp_impact, policy_data["max_impact"])

            total_cost += cost
            total_temp_mitigation += temp_impact

            # Store breakdown
            policy_breakdown.append({
                "policy": policy_data["label"],
                "level": level,
                "cost": round_to_precision(cost, 2),
                "cost_formatted": format_currency(cost),
                "temperature_impact": round_to_precision(temp_impact, 3),
                "temperature_formatted": format_temperature(temp_impact, 3),
                "description": policy_data["description"]
            })

            # Fiscal treemap (only include policies with positive cost)
            if cost > 0:
                fiscal_treemap.append({
                    "name": policy_data["label"],
                    "value": round_to_precision(cost, 2),
                    "formatted": format_currency(cost),
                    "percentage": 0  # Will calculate after total
                })

            # Efficiency index
            efficiency = calculate_efficiency_index(temp_impact, cost)
            efficiency_metrics.append({
                "policy": policy_data["label"],
                "efficiency": efficiency,
                "interpretation": self._interpret_efficiency(efficiency)
            })

        # Calculate treemap percentages
        total_positive_cost = sum(item["value"] for item in fiscal_treemap)
        if total_positive_cost > 0:
            for item in fiscal_treemap:
                item["percentage"] = round_to_precision(
                    (item["value"] / total_positive_cost) * 100, 1
                )

        # Generate projected trend line (2026-2050)
        trend_line = self._generate_trend_line(total_temp_mitigation)

        # Check bankruptcy threshold
        national_debt = total_cost
        bankruptcy_flag = national_debt > BANKRUPTCY_THRESHOLD

        # Prepare response
        return {
            "total_cost": round_to_precision(total_cost, 2),
            "total_cost_formatted": format_currency(total_cost),
            "temperature_mitigation": round_to_precision(total_temp_mitigation, 3),
            "temperature_mitigation_formatted": format_temperature(total_temp_mitigation, 3),
            "national_debt": round_to_precision(national_debt, 2),
            "national_debt_formatted": format_currency(national_debt),
            "bankruptcy_flag": bankruptcy_flag,
            "policy_breakdown": policy_breakdown,
            "trend_line": trend_line,
            "fiscal_treemap": fiscal_treemap,
            "efficiency_index": efficiency_metrics,
            "policies_applied": policies,
            "warning_message": "ECONOMIC COLLAPSE IMMINENT" if bankruptcy_flag else None
        }

    def _generate_trend_line(self, total_mitigation):
        """
        Generate projected temperature trend with policy mitigation applied

        Args:
            total_mitigation: Total °C reduction from all policies

        Returns:
            List of {year, anomaly, bau_anomaly} for 2026-2050
        """
        trend_data = []

        for bau_point in self.bau_projection:
            year = bau_point["year"]
            bau_temp = bau_point["anomaly"]

            # Apply mitigation (gradually phased in over time)
            # Full mitigation effect reaches by 2035, linear ramp from 2026
            years_from_start = year - 2026
            mitigation_factor = min(1.0, years_from_start / 9.0)  # 9 years to full effect

            adjusted_temp = bau_temp + (total_mitigation * mitigation_factor)

            trend_data.append({
                "year": year,
                "anomaly": round_to_precision(adjusted_temp, 3),
                "anomaly_formatted": format_temperature(adjusted_temp, 2),
                "bau_anomaly": round_to_precision(bau_temp, 3),
                "mitigation_applied": round_to_precision(total_mitigation * mitigation_factor, 3)
            })

        return trend_data

    def _interpret_efficiency(self, efficiency_score):
        """
        Provide human-readable interpretation of efficiency score

        Args:
            efficiency_score: Calculated efficiency value

        Returns:
            String interpretation (Excellent/Good/Moderate/Poor)
        """
        if efficiency_score >= 1.0:
            return "Excellent"
        elif efficiency_score >= 0.5:
            return "Good"
        elif efficiency_score >= 0.2:
            return "Moderate"
        else:
            return "Poor"

    def get_baseline_state(self):
        """
        Get initial 2026 baseline for dashboard initialization

        Returns:
            Dict with baseline temperature, debt, and empty policy state
        """
        return {
            "year": self.baseline["year"],
            "temperature_anomaly": self.baseline["temperature_anomaly"],
            "temperature_formatted": format_temperature(self.baseline["temperature_anomaly"], 2),
            "national_debt": self.baseline["national_debt"],
            "national_debt_formatted": format_currency(self.baseline["national_debt"]),
            "policies": self.baseline["policies"],
            "bau_projection": [
                {
                    "year": point["year"],
                    "anomaly": point["anomaly"],
                    "anomaly_formatted": format_temperature(point["anomaly"], 2)
                }
                for point in self.bau_projection
            ],
            "historical_data": [
                {
                    "year": point["year"],
                    "anomaly": point["anomaly"],
                    "anomaly_formatted": format_temperature(point["anomaly"], 2)
                }
                for point in get_complete_trend_data()
                if point["year"] < 2026
            ]
        }