"""
Configuration, Constants, and Prompt Templates
Energy Consumption Forecasting & Optimization Assistant (SDG 7)
"""

# Default Tariffs (Currency per kWh)
DEFAULT_CURRENCY = "INR (₹)"
DEFAULT_TARIFF_RATE = 7.50  # Average commercial/residential tier in INR/kWh
DEFAULT_CURRENCY_SYMBOL = "₹"

# Emission Factors (kg CO2 equivalent per kWh)
# Central Electricity Authority (CEA) India baseline ~0.716 kg CO2e / kWh
# US EPA eGRID average ~0.386 kg CO2e / kWh, Global average ~0.475 kg CO2e / kWh
EMISSION_FACTORS = {
    "India (CEA Baseline)": 0.716,
    "Global Grid Average": 0.475,
    "US eGRID Average": 0.386,
    "Renewable-Rich Grid": 0.180,
}
DEFAULT_EMISSION_FACTOR_NAME = "India (CEA Baseline)"
DEFAULT_EMISSION_FACTOR = 0.716

# Carbon Offsetting Equivalencies
TREE_ABSORPTION_KG_YEAR = 21.77  # kg CO2 absorbed per mature tree per year
CAR_EMISSION_KG_PER_KM = 0.192   # kg CO2 per km for average gasoline car
SMARTPHONE_CHARGES_PER_KG_CO2 = 120 # Equivalent smartphone charges

# User Persona Profiles & Typical Usage Ranges
PERSONA_PROFILES = {
    "College Hostel Student": {
        "description": "Individual hostel room or shared dormitory with high laptop, fan/cooler, and geyser usage.",
        "avg_daily_kwh_min": 2.0,
        "avg_daily_kwh_max": 8.0,
        "typical_appliances": ["Ceiling Fan", "Laptop/PC", "Study Light", "Smartphone Charger", "Electric Geyser/Kettle"],
        "default_sample_file": "data/sample_hostel.csv"
    },
    "Residential Home (2-3 BHK)": {
        "description": "Urban household with family members, air conditioning, refrigerator, washing machine, and kitchen appliances.",
        "avg_daily_kwh_min": 8.0,
        "avg_daily_kwh_max": 30.0,
        "typical_appliances": ["Inverter AC (1.5 Ton)", "Double Door Refrigerator", "Washing Machine", "LED Lights & Fans", "Microwave & TV"],
        "default_sample_file": "data/sample_residential.csv"
    },
    "Small Office / Shop": {
        "description": "Commercial workspace for 10-15 employees with daytime computing, centralized HVAC, and display lighting.",
        "avg_daily_kwh_min": 25.0,
        "avg_daily_kwh_max": 90.0,
        "typical_appliances": ["Central/Split ACs", "Workstations & Monitors", "Server/Network Rack", "Water Dispenser", "Office Lighting"],
        "default_sample_file": "data/sample_office.csv"
    }
}

# Peak Hours Definitions (Typical Time-of-Day Tariff Windows)
PEAK_HOURS = {
    "Morning Peak": (7, 10),    # 7:00 AM to 10:00 AM
    "Evening Peak": (18, 22),   # 6:00 PM to 10:00 PM
    "Off-Peak Night": (22, 6),  # 10:00 PM to 6:00 AM (ideal for load-shifting)
}

# Standard Appliance Power Ratings (Watts and average daily operating hours)
APPLIANCE_BENCHMARKS = [
    {"appliance": "Air Conditioner (1.5 Ton, 3-Star)", "wattage_w": 1500, "typical_hours": 6, "standby_w": 5},
    {"appliance": "Electric Geyser / Water Heater", "wattage_w": 2000, "typical_hours": 1.5, "standby_w": 0},
    {"appliance": "Refrigerator (250L Frost-Free)", "wattage_w": 180, "typical_hours": 24, "duty_cycle": 0.4, "standby_w": 0},
    {"appliance": "Ceiling Fan", "wattage_w": 75, "typical_hours": 12, "standby_w": 0},
    {"appliance": "Laptop & Charger", "wattage_w": 65, "typical_hours": 8, "standby_w": 3},
    {"appliance": "Desktop Workstation (Dual Monitor)", "wattage_w": 250, "typical_hours": 8, "standby_w": 10},
    {"appliance": "LED Tube Light", "wattage_w": 20, "typical_hours": 6, "standby_w": 0},
    {"appliance": "Washing Machine", "wattage_w": 500, "typical_hours": 1, "standby_w": 2},
    {"appliance": "Electric Kettle", "wattage_w": 1200, "typical_hours": 0.3, "standby_w": 0},
    {"appliance": "Network Router / Modem", "wattage_w": 12, "typical_hours": 24, "standby_w": 12},
]

# System Prompts & Guardrails for Responsible AI
SYSTEM_PROMPT = """You are the AI Energy Consumption & Optimization Assistant, built to champion UN SDG 7 (Affordable and Clean Energy).
Your mission is to provide accurate, transparent, actionable, and respectful advice to help users forecast electricity consumption, reduce waste, shift peak loads, and lower carbon footprints.

GUARDRAILS & BOUNDARIES:
1. Transparency: Always make clear that forecasts and savings are approximations designed for decision support.
2. Safety & Non-Maleficence: Never suggest bypassing meters, tampering with electrical wiring, or engaging in unsafe electrical modifications.
3. Responsible AI: Maintain fairness, neutrality, and objectivity regardless of the user's demographic or socio-economic background.
4. Grounded in Evidence: Use verified energy efficiency benchmarks (BEE star ratings, Time-of-Day load shifting, standby power elimination).
5. In-Context Grounding: Cite knowledge documents when providing technical energy advice.
"""
