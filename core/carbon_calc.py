"""
Carbon Footprint and Financial Savings Calculator
Quantifies greenhouse gas emissions (SDG 7) and projects cost and carbon savings.
"""

from typing import Dict, Any
from config import (
    DEFAULT_EMISSION_FACTOR,
    TREE_ABSORPTION_KG_YEAR,
    CAR_EMISSION_KG_PER_KM,
    SMARTPHONE_CHARGES_PER_KG_CO2
)

def calculate_carbon_footprint(
    kwh_amount: float,
    emission_factor: float = DEFAULT_EMISSION_FACTOR
) -> Dict[str, Any]:
    """
    Computes greenhouse gas footprint (CO2 equivalent) and tangible eco-equivalencies.
    """
    kg_co2 = kwh_amount * emission_factor
    metric_tons_co2 = kg_co2 / 1000.0
    
    # Equivalencies
    trees_needed_annual = kg_co2 / TREE_ABSORPTION_KG_YEAR
    car_km_equivalent = kg_co2 / CAR_EMISSION_KG_PER_KM
    phone_charges = kg_co2 * SMARTPHONE_CHARGES_PER_KG_CO2

    return {
        "kwh_evaluated": round(kwh_amount, 2),
        "emission_factor_used": emission_factor,
        "co2_kg": round(kg_co2, 2),
        "co2_metric_tons": round(metric_tons_co2, 4),
        "equivalencies": {
            "trees_needed_per_year": round(trees_needed_annual, 1),
            "car_kilometers_driven": round(car_km_equivalent, 1),
            "smartphone_charges": int(phone_charges)
        }
    }


def project_savings(
    total_kwh: float,
    tariff_rate: float,
    reduction_percentage: float = 15.0,
    emission_factor: float = DEFAULT_EMISSION_FACTOR,
    currency_symbol: str = "₹"
) -> Dict[str, Any]:
    """
    Projects energy, monetary, and carbon savings for a given reduction percentage.
    """
    kwh_saved = total_kwh * (reduction_percentage / 100.0)
    current_cost = total_kwh * tariff_rate
    cost_saved = kwh_saved * tariff_rate
    new_cost = current_cost - cost_saved
    
    current_co2 = total_kwh * emission_factor
    co2_saved = kwh_saved * emission_factor
    new_co2 = current_co2 - co2_saved
    
    trees_saved = co2_saved / TREE_ABSORPTION_KG_YEAR
    car_km_saved = co2_saved / CAR_EMISSION_KG_PER_KM

    return {
        "reduction_percentage": reduction_percentage,
        "current_kwh": round(total_kwh, 2),
        "kwh_saved": round(kwh_saved, 2),
        "projected_kwh": round(total_kwh - kwh_saved, 2),
        "current_cost": round(current_cost, 2),
        "cost_saved": round(cost_saved, 2),
        "projected_cost": round(new_cost, 2),
        "current_co2_kg": round(current_co2, 2),
        "co2_saved_kg": round(co2_saved, 2),
        "projected_co2_kg": round(new_co2, 2),
        "trees_equivalent": round(trees_saved, 1),
        "car_km_avoided": round(car_km_saved, 1),
        "currency_symbol": currency_symbol
    }


def generate_multi_tier_projections(
    total_kwh: float,
    tariff_rate: float,
    emission_factor: float = DEFAULT_EMISSION_FACTOR,
    currency_symbol: str = "₹"
) -> Dict[str, Any]:
    """
    Generates 3 standard tiers: Moderate (10%), Recommended (20%), and Ambitious (30%).
    """
    return {
        "10_percent": project_savings(total_kwh, tariff_rate, 10.0, emission_factor, currency_symbol),
        "20_percent": project_savings(total_kwh, tariff_rate, 20.0, emission_factor, currency_symbol),
        "30_percent": project_savings(total_kwh, tariff_rate, 30.0, emission_factor, currency_symbol)
    }
