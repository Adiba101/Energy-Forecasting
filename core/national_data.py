"""
National Energy Data Module
Central repository for Indian Regional Grids, State Energy Profiles,
National Schemes & Directives, AI Forecasting Model Benchmarks, and Repository Metadata.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

# =====================================================================
# 1. FIVE REGIONAL POWER GRIDS OF INDIA
# =====================================================================
REGIONAL_GRID_DATA = {
    "Northern Region": {
        "code": "NR",
        "states": ["Delhi", "Punjab", "Haryana", "Rajasthan", "Uttar Pradesh", "Himachal Pradesh", "Uttarakhand", "Jammu & Kashmir"],
        "current_demand_gw": 68.4,
        "forecast_demand_gw": 71.2,
        "peak_demand_gw": 74.8,
        "renewable_gen_gw": 28.6,
        "renewable_share_pct": 41.8,
        "grid_frequency_hz": 50.02,
        "status": "Normal / Balanced",
        "status_color": "#10B981",
        "center_coords": [28.6139, 77.2090]
    },
    "Western Region": {
        "code": "WR",
        "states": ["Maharashtra", "Gujarat", "Madhya Pradesh", "Chhattisgarh", "Goa"],
        "current_demand_gw": 72.8,
        "forecast_demand_gw": 76.5,
        "peak_demand_gw": 79.2,
        "renewable_gen_gw": 31.4,
        "renewable_share_pct": 43.1,
        "grid_frequency_hz": 49.98,
        "status": "High Demand Window",
        "status_color": "#F59E0B",
        "center_coords": [21.1458, 79.0882]
    },
    "Southern Region": {
        "code": "SR",
        "states": ["Tamil Nadu", "Karnataka", "Andhra Pradesh", "Telangana", "Kerala"],
        "current_demand_gw": 54.1,
        "forecast_demand_gw": 55.4,
        "peak_demand_gw": 58.7,
        "renewable_gen_gw": 24.8,
        "renewable_share_pct": 45.8,
        "grid_frequency_hz": 50.01,
        "status": "High Renewable Injection",
        "status_color": "#0284C7",
        "center_coords": [13.0827, 80.2707]
    },
    "Eastern Region": {
        "code": "ER",
        "states": ["West Bengal", "Bihar", "Odisha", "Jharkhand"],
        "current_demand_gw": 29.5,
        "forecast_demand_gw": 30.1,
        "peak_demand_gw": 32.4,
        "renewable_gen_gw": 6.2,
        "renewable_share_pct": 21.0,
        "grid_frequency_hz": 50.00,
        "status": "Normal / Base Load Stable",
        "status_color": "#10B981",
        "center_coords": [22.5726, 88.3639]
    },
    "North-Eastern Region": {
        "code": "NER",
        "states": ["Assam", "Meghalaya", "Tripura", "Manipur", "Nagaland", "Arunachal Pradesh", "Mizoram"],
        "current_demand_gw": 3.8,
        "forecast_demand_gw": 4.1,
        "peak_demand_gw": 4.6,
        "renewable_gen_gw": 1.4,
        "renewable_share_pct": 36.8,
        "grid_frequency_hz": 50.03,
        "status": "Hydro Rich / Low Demand",
        "status_color": "#10B981",
        "center_coords": [26.1445, 91.7362]
    }
}

# =====================================================================
# 2. STATE-WISE ENERGY DATABASE (28 States & Key UTs)
# =====================================================================
STATE_ENERGY_DB = {
    "Maharashtra": {"region": "Western Region", "current_gw": 26.8, "forecast_gw": 28.2, "peak_gw": 29.5, "renewable_gw": 11.2, "growth_pct": 5.2, "accuracy_pct": 95.8, "risk": "Moderate", "solar_gw": 4.8, "wind_gw": 5.1, "hydro_gw": 1.3},
    "Gujarat": {"region": "Western Region", "current_gw": 21.5, "forecast_gw": 22.8, "peak_gw": 23.9, "renewable_gw": 13.6, "growth_pct": 6.0, "accuracy_pct": 96.4, "risk": "Low", "solar_gw": 7.2, "wind_gw": 5.9, "hydro_gw": 0.5},
    "Tamil Nadu": {"region": "Southern Region", "current_gw": 17.6, "forecast_gw": 18.2, "peak_gw": 19.1, "renewable_gw": 10.8, "growth_pct": 3.4, "accuracy_pct": 96.1, "risk": "Low", "solar_gw": 4.9, "wind_gw": 5.3, "hydro_gw": 0.6},
    "Uttar Pradesh": {"region": "Northern Region", "current_gw": 25.4, "forecast_gw": 26.9, "peak_gw": 28.7, "renewable_gw": 5.3, "growth_pct": 5.9, "accuracy_pct": 94.2, "risk": "High", "solar_gw": 3.8, "wind_gw": 0.2, "hydro_gw": 1.3},
    "Rajasthan": {"region": "Northern Region", "current_gw": 15.2, "forecast_gw": 16.0, "peak_gw": 17.1, "renewable_gw": 14.8, "growth_pct": 5.3, "accuracy_pct": 95.2, "risk": "Low", "solar_gw": 11.8, "wind_gw": 2.8, "hydro_gw": 0.2},
    "Karnataka": {"region": "Southern Region", "current_gw": 14.8, "forecast_gw": 15.3, "peak_gw": 16.2, "renewable_gw": 11.4, "growth_pct": 3.4, "accuracy_pct": 95.9, "risk": "Low", "solar_gw": 7.5, "wind_gw": 3.2, "hydro_gw": 0.7},
    "Madhya Pradesh": {"region": "Western Region", "current_gw": 13.9, "forecast_gw": 14.8, "peak_gw": 15.6, "renewable_gw": 5.8, "growth_pct": 6.5, "accuracy_pct": 94.7, "risk": "Moderate", "solar_gw": 3.6, "wind_gw": 1.8, "hydro_gw": 0.4},
    "Andhra Pradesh": {"region": "Southern Region", "current_gw": 11.2, "forecast_gw": 11.8, "peak_gw": 12.6, "renewable_gw": 6.1, "growth_pct": 5.4, "accuracy_pct": 95.1, "risk": "Moderate", "solar_gw": 3.9, "wind_gw": 1.9, "hydro_gw": 0.3},
    "Telangana": {"region": "Southern Region", "current_gw": 12.4, "forecast_gw": 13.1, "peak_gw": 14.0, "renewable_gw": 4.6, "growth_pct": 5.6, "accuracy_pct": 94.8, "risk": "Moderate", "solar_gw": 4.1, "wind_gw": 0.2, "hydro_gw": 0.3},
    "Punjab": {"region": "Northern Region", "current_gw": 10.8, "forecast_gw": 11.5, "peak_gw": 12.2, "renewable_gw": 2.2, "growth_pct": 6.5, "accuracy_pct": 93.8, "risk": "High", "solar_gw": 1.6, "wind_gw": 0.1, "hydro_gw": 0.5},
    "Haryana": {"region": "Northern Region", "current_gw": 10.4, "forecast_gw": 11.0, "peak_gw": 11.8, "renewable_gw": 1.9, "growth_pct": 5.8, "accuracy_pct": 94.5, "risk": "Moderate", "solar_gw": 1.5, "wind_gw": 0.1, "hydro_gw": 0.3},
    "West Bengal": {"region": "Eastern Region", "current_gw": 10.2, "forecast_gw": 10.6, "peak_gw": 11.4, "renewable_gw": 1.8, "growth_pct": 3.9, "accuracy_pct": 95.3, "risk": "Low", "solar_gw": 0.9, "wind_gw": 0.1, "hydro_gw": 0.8},
    "Delhi": {"region": "Northern Region", "current_gw": 7.4, "forecast_gw": 7.9, "peak_gw": 8.6, "renewable_gw": 1.2, "growth_pct": 6.8, "accuracy_pct": 96.8, "risk": "High", "solar_gw": 1.1, "wind_gw": 0.0, "hydro_gw": 0.1},
    "Odisha": {"region": "Eastern Region", "current_gw": 6.8, "forecast_gw": 7.1, "peak_gw": 7.7, "renewable_gw": 1.9, "growth_pct": 4.4, "accuracy_pct": 95.5, "risk": "Low", "solar_gw": 0.8, "wind_gw": 0.1, "hydro_gw": 1.0},
    "Bihar": {"region": "Eastern Region", "current_gw": 7.1, "forecast_gw": 7.5, "peak_gw": 8.0, "renewable_gw": 0.9, "growth_pct": 5.6, "accuracy_pct": 93.9, "risk": "Moderate", "solar_gw": 0.7, "wind_gw": 0.0, "hydro_gw": 0.2},
    "Chhattisgarh": {"region": "Western Region", "current_gw": 5.2, "forecast_gw": 5.4, "peak_gw": 5.9, "renewable_gw": 1.4, "growth_pct": 3.8, "accuracy_pct": 95.7, "risk": "Low", "solar_gw": 1.0, "wind_gw": 0.0, "hydro_gw": 0.4},
    "Kerala": {"region": "Southern Region", "current_gw": 4.6, "forecast_gw": 4.8, "peak_gw": 5.1, "renewable_gw": 2.1, "growth_pct": 4.3, "accuracy_pct": 96.0, "risk": "Low", "solar_gw": 0.8, "wind_gw": 0.1, "hydro_gw": 1.2},
    "Himachal Pradesh": {"region": "Northern Region", "current_gw": 2.2, "forecast_gw": 2.3, "peak_gw": 2.6, "renewable_gw": 2.8, "growth_pct": 4.5, "accuracy_pct": 96.2, "risk": "Low", "solar_gw": 0.2, "wind_gw": 0.0, "hydro_gw": 2.6},
    "Uttarakhand": {"region": "Northern Region", "current_gw": 2.5, "forecast_gw": 2.6, "peak_gw": 2.9, "renewable_gw": 2.4, "growth_pct": 4.0, "accuracy_pct": 95.8, "risk": "Low", "solar_gw": 0.4, "wind_gw": 0.0, "hydro_gw": 2.0},
    "Assam": {"region": "North-Eastern Region", "current_gw": 2.4, "forecast_gw": 2.5, "peak_gw": 2.8, "renewable_gw": 0.6, "growth_pct": 4.2, "accuracy_pct": 94.6, "risk": "Low", "solar_gw": 0.3, "wind_gw": 0.0, "hydro_gw": 0.3},
    "Jharkhand": {"region": "Eastern Region", "current_gw": 3.4, "forecast_gw": 3.6, "peak_gw": 3.9, "renewable_gw": 0.7, "growth_pct": 5.9, "accuracy_pct": 94.1, "risk": "Moderate", "solar_gw": 0.5, "wind_gw": 0.0, "hydro_gw": 0.2},
    "Jammu & Kashmir": {"region": "Northern Region", "current_gw": 2.9, "forecast_gw": 3.1, "peak_gw": 3.4, "renewable_gw": 1.8, "growth_pct": 6.9, "accuracy_pct": 93.4, "risk": "Moderate", "solar_gw": 0.2, "wind_gw": 0.0, "hydro_gw": 1.6},
    "Goa": {"region": "Western Region", "current_gw": 0.8, "forecast_gw": 0.8, "peak_gw": 0.9, "renewable_gw": 0.1, "growth_pct": 2.5, "accuracy_pct": 97.1, "risk": "Low", "solar_gw": 0.1, "wind_gw": 0.0, "hydro_gw": 0.0},
    "Tripura": {"region": "North-Eastern Region", "current_gw": 0.6, "forecast_gw": 0.6, "peak_gw": 0.7, "renewable_gw": 0.2, "growth_pct": 3.3, "accuracy_pct": 95.0, "risk": "Low", "solar_gw": 0.1, "wind_gw": 0.0, "hydro_gw": 0.1},
    "Meghalaya": {"region": "North-Eastern Region", "current_gw": 0.4, "forecast_gw": 0.4, "peak_gw": 0.5, "renewable_gw": 0.3, "growth_pct": 2.8, "accuracy_pct": 95.4, "risk": "Low", "solar_gw": 0.05, "wind_gw": 0.0, "hydro_gw": 0.25}
}

# =====================================================================
# 3. INTERACTIVE NATIONAL SCHEMES & DIRECTIVES (11 Items)
# =====================================================================
SCHEMES_DATABASE = {
    "🇮🇳 मिशन LiFE (Lifestyle for Environment)": {
        "title_en": "Mission LiFE (Lifestyle for Environment)",
        "title_hi": "मिशन LiFE (पर्यावरण के अनुकूल जीवनशैली)",
        "ministry": "Ministry of Environment, Forest and Climate Change & NITI Aayog",
        "category": "Citizen Climate Action & Energy Conservation",
        "icon": "🇮🇳",
        "tagline": "Pledge to Action: Mindful and deliberate utilization of energy instead of mindless and wasteful consumption.",
        "summary": "Introduced by the Hon'ble Prime Minister at COP26, Mission LiFE mobilizes citizens into 'Pro-Planet People' (P3). It emphasizes 7 core action categories with direct electricity-saving rules: switching off appliances from plug point, setting ACs to 24°C, installing BEE 5-star equipment, and taking public transit.",
        "key_initiatives": [
            "Mandatory avoidance of vampire standby loads by turning off socket switches.",
            "Optimum room cooling setting at 24°C to save 24% air-conditioning power nationwide.",
            "Maximizing natural daylight harvesting in homes and institutional campuses.",
            "Energy Audits for all public buildings and educational institutions."
        ],
        "subsidies_and_benefits": "National LiFE Green Credit certification, carbon offset credits, and municipal rebates on solar installations.",
        "carbon_impact": "Expected reduction of 1 billion tonnes of CO₂ emissions annually by 2030 across India.",
        "citizen_action_checklist": [
            "Switch off appliances at the wall outlet when not in active use.",
            "Use natural ventilation during early morning and late evening hours.",
            "Replace conventional tube lights with 20W LED fixtures.",
            "Take the official LiFE Pledge on the MyGov.in portal."
        ],
        "official_link": "https://missionlife-moefcc.nic.in/"
    },
    "☀️ पीएम सूर्य घर: मुफ्त बिजली योजना": {
        "title_en": "PM Surya Ghar: Muft Bijli Yojana",
        "title_hi": "पीएम सूर्य घर: मुफ्त बिजली योजना",
        "ministry": "Ministry of New and Renewable Energy (MNRE)",
        "category": "Rooftop Solar & Citizen Energy Independence",
        "icon": "☀️",
        "tagline": "Empowering 1 Crore Households with Up to 300 Units of Free Clean Electricity Every Month.",
        "summary": "Cabinet-approved national flagship scheme with an outlay of ₹75,021 Crore. Provides direct DBT subsidies to residential homeowners to install rooftop solar PV systems, drastically relieving grid peak stress and producing surplus clean energy for grid feed-in.",
        "key_initiatives": [
            "Central Financial Assistance (CFA): ₹30,000 subsidy for 1 kW system; ₹60,000 for 2 kW; ₹78,000 for 3 kW and above.",
            "Zero-hassle collateral-free loans at concessional interest rate (~7%) via nationalized banks.",
            "Digital net-metering integration within 30 days via national DISCOM portal.",
            "Model Solar Villages designated in each district of India with ₹1 Crore incentive per village."
        ],
        "subsidies_and_benefits": "Up to ₹78,000 direct bank transfer subsidy; zero electricity bills for up to 300 units/month; net-metering income from surplus power.",
        "carbon_impact": "Reduction of 720 million tonnes of CO₂ emissions over the 25-year lifetime of 1 crore rooftop systems.",
        "citizen_action_checklist": [
            "Register on the National Portal: pmsuryaghar.gov.in using Consumer Electricity Account ID.",
            "Select an MNRE-empaneled registered vendor for rooftop feasibility audit.",
            "Submit online application and net-metering request.",
            "Receive direct bank transfer (DBT) subsidy into linked account upon commissioning."
        ],
        "official_link": "https://pmsuryaghar.gov.in/"
    },
    "💡 उजाला (UJALA) 5-स्टार एलईडी मिशन": {
        "title_en": "UJALA (Unnat Jyoti by Affordable LEDs for All)",
        "title_hi": "उजाला योजना (उन्नत ज्योति किफायती एलईडी द्वारा)",
        "ministry": "Ministry of Power & Energy Efficiency Services Limited (EESL)",
        "category": "High-Efficiency Lighting & Demand Side Management",
        "icon": "💡",
        "tagline": "The World's Largest Zero-Subsidy Domestic Energy-Efficient Lighting Programme.",
        "summary": "UJALA revolutionized domestic illumination by mass-procuring high-grade LED bulbs and distributing them at affordable prices. Over 36.8 Crore LED bulbs, 72 Lakh LED tube lights, and 23 Lakh energy-efficient fans have been deployed, cutting national peak load substantially.",
        "key_initiatives": [
            "Bulk aggregation lowering LED retail cost from ₹310 to under ₹70 without government subsidies.",
            "9W LED bulbs delivering equivalent lumens to 60W incandescent lamps at 85% energy savings.",
            "Super-efficient 28W brushless DC (BLDC) 5-star ceiling fans.",
            "Replacement of inefficient streetlights with smart automated LED luminaires under SLNP."
        ],
        "subsidies_and_benefits": "Subsidized high-reliability LED bulbs available at local DISCOM offices with 3-year replacement warranty.",
        "carbon_impact": "Annual CO₂ mitigation of 38.7 million tonnes; saved over 47.7 billion kWh of electricity per year.",
        "citizen_action_checklist": [
            "Replace all halogen and CFL bulbs with 5-star rated BEE LEDs.",
            "Install 28W BLDC ceiling fans in all living areas and bedrooms.",
            "Utilize localized task lighting rather than illuminating entire unoccupied rooms."
        ],
        "official_link": "https://ujala.gov.in/"
    },
    "❄️ बीईई 24°C अनिवार्य एसी तापमान मानक": {
        "title_en": "BEE 24°C Mandatory AC Default Temperature Standard",
        "title_hi": "बीईई 24°C अनिवार्य एसी तापमान मानक",
        "ministry": "Bureau of Energy Efficiency (BEE), Ministry of Power",
        "category": "Statutory Standards & Thermostat Regulation",
        "icon": "❄️",
        "tagline": "Every 1°C increase in AC temperature setting saves 6% electricity consumption.",
        "summary": "Under Gazette Notification S.O. 4235(E), all room air conditioners manufactured or sold in India are mandatorily set with a default temperature of 24°C out of the box. Running ACs at 24°C-26°C instead of 18°C-20°C optimizes comfort while slashing summer peak grid strain.",
        "key_initiatives": [
            "Mandatory 24°C factory default setpoint on all inverter and fixed-speed split/window ACs.",
            "Guidelines for commercial establishments, airports, hotels, and government offices to maintain room temperatures at 24°C-25°C.",
            "Thermal comfort standard based on the Indian National Building Code (NBC 2016).",
            "Periodic energy auditing of commercial complexes having connected loads > 100 kW."
        ],
        "subsidies_and_benefits": "Immediate 24% to 30% reduction in monthly summer electricity tariffs for homes and institutions without capital expense.",
        "carbon_impact": "Conserves over 20 billion units of electricity annually, avoiding ~16.5 million tonnes of CO₂.",
        "citizen_action_checklist": [
            "Set home and office air conditioner thermostats to 24°C or higher.",
            "Use a ceiling fan on low speed simultaneously to circulate conditioned air.",
            "Clean AC filters every fortnight to maintain heat-exchange efficiency.",
            "Ensure room doors and windows are tightly sealed with weatherstripping."
        ],
        "official_link": "https://beeindia.gov.in/"
    },
    "🕒 टाइम-ऑफ-डे (ToD) पीक-लोड शेविंग नियम": {
        "title_en": "Time-of-Day (ToD) Dynamic Tariff & Peak-Load Shaving",
        "title_hi": "टाइम-ऑफ-डे (ToD) टैरिफ एवं पीक-लोड शेविंग नियम",
        "ministry": "Ministry of Power / Central Electricity Regulatory Commission (CERC)",
        "category": "Grid Flexibility & Demand Response Architecture",
        "icon": "🕒",
        "tagline": "Smart Pricing: 20% Cheaper Electricity During Solar Hours; Surcharges on Evening Peak.",
        "summary": "Under the Electricity (Rights of Consumers) Amendment Rules, ToD tariffs incentivize consumers to shift power-intensive activities (washing machines, EV charging, irrigation pumps) to daytime solar hours (9 AM - 4 PM) and conserve during peak evening hours (6 PM - 10 PM).",
        "key_initiatives": [
            "Solar Hours Tariff: 10% to 20% discount on normal tariff during abundant renewable solar hours.",
            "Peak Hours Tariff: 1.2x to 1.3x surcharge during evening high-demand windows (18:00 - 22:00).",
            "Smart Prepaid Metering deployment under RDSS across 25 Crore consumer connections.",
            "Automated demand-response protocols for industrial and commercial consumers."
        ],
        "subsidies_and_benefits": "Smart meter consumers can trim their overall monthly bill by 15-22% simply by rescheduling heavy appliance use.",
        "carbon_impact": "Reduces thermal peaker plant ramp-up emissions by 42,000 metric tons of CO₂ daily across the national grid.",
        "citizen_action_checklist": [
            "Run washing machines, dishwashers, and water pumps between 10:00 AM and 4:00 PM.",
            "Charge Electric Vehicles (EVs) during night off-peak or daytime solar windows.",
            "Avoid operating electric geysers and ovens simultaneously during 7:00-9:30 PM."
        ],
        "official_link": "https://powermin.gov.in/"
    },
    "🌾 पीएम-कुसुम (PM-KUSUM) कृषि सौर ऊर्जा": {
        "title_en": "PM-KUSUM (Kisan Urja Suraksha evam Utthaan Mahabhiyan)",
        "title_hi": "पीएम-कुसुम: किसान ऊर्जा सुरक्षा एवं उत्थान महाभियान",
        "ministry": "Ministry of New and Renewable Energy (MNRE)",
        "category": "Agricultural Solarization & Rural Energy Empowerment",
        "icon": "🌾",
        "tagline": "De-dieselizing the Indian Farm Sector while Turning Farmers into Energy Producers ('Urjadata').",
        "summary": "PM-KUSUM provides clean, daytime solar power for irrigation to millions of farmers. It replaces costly, polluting diesel pump sets, solarizes existing agricultural grid feeders, and enables farmers to sell surplus solar power back to DISCOMs.",
        "key_initiatives": [
            "Component A: 10,000 MW of decentralized ground-mounted solar power plants on barren/fallow land.",
            "Component B: Installation of 20 Lakh standalone solar-powered agriculture pumps.",
            "Component C: Solarization of 15 Lakh grid-connected agricultural pumps including feeder-level solarization."
        ],
        "subsidies_and_benefits": "60% government subsidy (30% Central + 30% State); 30% bank loan; farmer contributes only 10% upfront.",
        "carbon_impact": "Mitigates 32 million tonnes of CO₂ annually while eliminating diesel consumption of 1.38 billion liters/yr.",
        "citizen_action_checklist": [
            "Apply via State Renewable Energy Development Agency (SREDA) portal.",
            "Verify land ownership and existing agricultural pump rating.",
            "Opt for feeder-level solarization under Component C for daytime irrigation access."
        ],
        "official_link": "https://pmkusum.mnre.gov.in/"
    },
    "🎓 छात्रावास एवं संस्थान ऊर्जा कोटा (Hostel Norms)": {
        "title_en": "Hostel & Educational Campus Energy Efficiency Norms",
        "title_hi": "छात्रावास एवं शैक्षणिक संस्थान ऊर्जा दक्षता मानक",
        "ministry": "Ministry of Education & Bureau of Energy Efficiency (BEE)",
        "category": "Institutional Benchmarking & Campus Sustainability",
        "icon": "🎓",
        "tagline": "Benchmarking per-capita student hostel consumption to under 2.5 kWh/student/day.",
        "summary": "Statutory energy conservation guidelines formulated for higher education institutions (IITs, NITs, Central Universities, and private colleges). Prescribes rooftop solar mandates, centralized heat-pump geysers, smart key-card power cutoffs, and campus student green audit councils.",
        "key_initiatives": [
            "Per-Capita Energy Target: Capped at 2.0 - 2.5 kWh/student/day for hostel rooms without individual ACs.",
            "Solar water heating and centralized heat pumps mandated for all mess and bath complexes.",
            "Mandatory automatic occupancy sensors in lecture halls, laboratories, and libraries.",
            "Student-led Energy Champions conducting quarterly building-wise audits."
        ],
        "subsidies_and_benefits": "Grants under Green Campus NIRF ranking criteria and subsidized central solar rooftop allocations.",
        "carbon_impact": "Prevents over 3.2 million metric tons of CO₂ emissions across India's 45,000+ colleges and universities.",
        "citizen_action_checklist": [
            "Unplug laptops and personal chargers when leaving hostel dorm rooms.",
            "Report faulty bathroom cisterns and running geysers to maintenance immediately.",
            "Conduct campus energy audits with student clubs to identify base-load leakage."
        ],
        "official_link": "https://beeindia.gov.in/en/standards-labeling"
    },
    "🏡 2-3 बीएचके स्मार्ट गृह दक्षता मानक": {
        "title_en": "2-3 BHK Smart Home Energy Efficiency Standards",
        "title_hi": "2-3 बीएचके स्मार्ट गृह ऊर्जा दक्षता मानक",
        "ministry": "Bureau of Energy Efficiency (BEE) & Ministry of Housing and Urban Affairs",
        "category": "Residential Energy Conservation Code & Smart Living",
        "icon": "🏡",
        "tagline": "Eco-Niwas Samhita (ENS) Standards for Low-Carbon Urban Living.",
        "summary": "The Eco-Niwas Samhita (Energy Conservation Building Code for Residential Buildings) sets energy performance indices for typical 2-3 BHK urban flats. A standard household should target an EPI of 30-45 kWh/m²/year through envelope insulation, cross-ventilation, and 5-star appliance usage.",
        "key_initiatives": [
            "Window-to-Wall Ratio (WWR) optimization and high-performance reflective window glazing.",
            "Smart power strips to eradicate 'vampire' standby loads from TVs, gaming consoles, and microwaves.",
            "BLDC ceiling fan adoption reducing fan power from 75W to 28W.",
            "Zonal air conditioning with inverter technology sized strictly to room volume."
        ],
        "subsidies_and_benefits": "Reduces typical household monthly bills by ₹1,500 to ₹3,500; enhances thermal comfort during heatwaves.",
        "carbon_impact": "Saves approximately 1.8 metric tons of CO₂ per household every year.",
        "citizen_action_checklist": [
            "Perform a 10-minute home energy audit: check refrigerator door seal with a paper slip.",
            "Install timer switches on storage geysers (maximum 30 minutes runtime).",
            "Use smart WiFi plugs for home entertainment centers to cut overnight power drain."
        ],
        "official_link": "https://econiwas.beeindia.gov.in/"
    },
    "🏬 एमएसएमई एवं खुदरा दुकान ऊर्जा दक्षता": {
        "title_en": "MSME & Commercial Retail Energy Efficiency Program",
        "title_hi": "एमएसएमई एवं खुदरा दुकान ऊर्जा दक्षता कार्यक्रम",
        "ministry": "Ministry of Micro, Small & Medium Enterprises & BEE",
        "category": "Small Business Productivity & Cost Reduction",
        "icon": "🏬",
        "tagline": "Slashing OPEX for Retailers and Small Enterprises via Energy Audits & Efficient Equipment.",
        "summary": "Targeted support for small retail establishments, workshops, and commercial offices. Focuses on commercial refrigeration, display lighting, server room cooling, and motor retrofits to boost profitability and national competitiveness.",
        "key_initiatives": [
            "Financial assistance up to ₹10 Lakhs for Investment Grade Energy Audits (IGEA).",
            "Concessional credit through SIDBI for replacement of obsolete motors with IE3 / IE4 efficiency class.",
            "Retail display lighting conversion to high CRI 110 lm/W LED fixtures.",
            "Submetering for separate monitoring of HVAC, lighting, and equipment power."
        ],
        "subsidies_and_benefits": "Up to 25% capital subsidy on energy-efficient technology acquisition under CLCSS and SIDBI green schemes.",
        "carbon_impact": "Cuts 15.4 million metric tons of CO₂ emissions annually while reducing business operating costs by 20%.",
        "citizen_action_checklist": [
            "Conduct a connected load inventory to prevent DISCOM maximum demand penalties.",
            "Install auto-cut door closers on air-conditioned showroom entrances.",
            "Maintain power factor above 0.95 using Automatic Power Factor Correction (APFC) capacitors."
        ],
        "official_link": "https://www.dcmsme.gov.in/"
    },
    "⭐ बीईई 5-स्टार उपकरण मानक (Star Labeling)": {
        "title_en": "BEE Standards & Star Labeling Program",
        "title_hi": "बीईई स्टार लेबलिंग एवं उपकरण मानक कार्यक्रम",
        "ministry": "Bureau of Energy Efficiency (BEE), Ministry of Power",
        "category": "Appliance Energy Benchmarks & Consumer Protection",
        "icon": "⭐",
        "tagline": "India's Gold Standard for Energy Efficiency: Look for the BEE Star Label Before Buying.",
        "summary": "Mandatory and voluntary star labeling scheme covering 34 appliances including ACs, refrigerators, distribution transformers, electric geysers, washing machines, and LED lamps. More stars equal higher energy savings and lower lifecycle electricity costs.",
        "key_initiatives": [
            "Periodic tightening of star rating thresholds every 2 years to drive manufacturing innovation.",
            "QR-code enabled verification on all star labels linking directly to BEE's compliance database.",
            "Mandatory star labeling for frost-free refrigerators, air conditioners, and ceiling fans.",
            "ISEER (Indian Seasonal Energy Efficiency Ratio) calculation tailored to Indian climatic zones."
        ],
        "subsidies_and_benefits": "A 5-star AC consumes ~38% less power than a 1-star AC; amortizes the price difference within 14 months of operation.",
        "carbon_impact": "Cumulative energy savings of 300+ billion kWh, avoiding over 250 million metric tonnes of CO₂.",
        "citizen_action_checklist": [
            "Scan the QR code on any star label using the BEE Star App before purchasing.",
            "Compare ISEER ratings for air conditioners and annual kWh consumption for refrigerators.",
            "Dispose of unrated 10+ year old appliances through registered e-waste recyclers."
        ],
        "official_link": "https://beestarlabel.com/"
    },
    "🌱 संयुक्त राष्ट्र सतत विकास लक्ष्य 7 (UN SDG 7)": {
        "title_en": "UN Sustainable Development Goal 7: Affordable & Clean Energy",
        "title_hi": "संयुक्त राष्ट्र सतत विकास लक्ष्य 7: सस्ती एवं स्वच्छ ऊर्जा",
        "ministry": "NITI Aayog (National Focal Point) & Ministry of Power",
        "category": "Global Sustainable Development Goals & National Commitments",
        "icon": "🌱",
        "tagline": "Ensure Access to Affordable, Reliable, Sustainable and Modern Energy for All by 2030.",
        "summary": "India's Panchamrit commitments at COP26 and NDC submissions under the Paris Agreement: reaching 500 GW non-fossil electricity capacity by 2030, reducing carbon intensity of GDP by 45%, and achieving Net Zero emissions by 2070. Targets 7.1 (Universal Access), 7.2 (Renewable Energy), and 7.3 (Doubling Energy Efficiency).",
        "key_initiatives": [
            "Target 7.1: 100% village electrification achieved under Saubhagya & DDUGJY schemes.",
            "Target 7.2: Over 190 GW non-fossil capacity already installed (44% of total installed power capacity).",
            "Target 7.3: PAT (Perform, Achieve and Trade) scheme saving 15 million tonnes of oil equivalent per cycle.",
            "National Green Hydrogen Mission targeting 5 MMT annual production by 2030."
        ],
        "subsidies_and_benefits": "Accelerated capital depreciation for green investments, green bond issuances, and carbon market trading mechanisms.",
        "carbon_impact": "Reduces India's economy-wide emission intensity by >45% from 2005 levels by 2030.",
        "citizen_action_checklist": [
            "Support local rooftop solar and community renewable energy projects.",
            "Track your household carbon footprint and strive for a 20% annual reduction.",
            "Advocate for energy efficiency in your housing society, workplace, and school."
        ],
        "official_link": "https://www.un.org/sustainabledevelopment/energy/"
    }
}

# =====================================================
# 4. AI FORECASTING MODELS BENCHMARK COMPARISON
# =====================================================
AI_MODELS_BENCHMARK = [
    {
        "Model Architecture": "Ensemble (Transformer + XGBoost)",
        "Type": "Hybrid Deep + Gradient Boosted",
        "RMSE (GW)": 2.45,
        "MAE (GW)": 1.78,
        "MAPE (%)": "1.82%",
        "R² Score": 0.988,
        "Inference Time": "14 ms",
        "Status": "Production Champion"
    },
    {
        "Model Architecture": "Temporal Transformer",
        "Type": "Self-Attention Multi-Horizon",
        "RMSE (GW)": 2.82,
        "MAE (GW)": 2.05,
        "MAPE (%)": "2.14%",
        "R² Score": 0.981,
        "Inference Time": "28 ms",
        "Status": "Active Evaluator"
    },
    {
        "Model Architecture": "Bidirectional LSTM",
        "Type": "Recurrent Deep Neural Net",
        "RMSE (GW)": 3.15,
        "MAE (GW)": 2.34,
        "MAPE (%)": "2.46%",
        "R² Score": 0.974,
        "Inference Time": "19 ms",
        "Status": "Baseline Deep Net"
    },
    {
        "Model Architecture": "Gated Recurrent Unit (GRU)",
        "Type": "Gated Recurrent Network",
        "RMSE (GW)": 3.38,
        "MAE (GW)": 2.49,
        "MAPE (%)": "2.61%",
        "R² Score": 0.969,
        "Inference Time": "16 ms",
        "Status": "Lightweight Baseline"
    },
    {
        "Model Architecture": "XGBoost Regressor",
        "Type": "Gradient Boosted Decision Trees",
        "RMSE (GW)": 3.64,
        "MAE (GW)": 2.71,
        "MAPE (%)": "2.85%",
        "R² Score": 0.962,
        "Inference Time": "4 ms",
        "Status": "Fast Tabular Model"
    }
]

# =====================================================
# 5. ENERGY DATA REPOSITORY INVENTORY
# =====================================================
DATA_REPOSITORY_CATALOG = [
    {
        "Dataset Name": "National Grid Hourly Demand & Dispatch Logs",
        "Data Source": "Grid Controller of India (POSOCO)",
        "Date Range": "2020-01-01 to Present",
        "Number of Records": "52,600+ Hourly Timesteps",
        "Update Frequency": "Real-time (Every 15 mins)",
        "Format": "CSV / Parquet / API",
        "Last Updated": "Today (Automated Stream)"
    },
    {
        "Dataset Name": "CEA State-Wise Monthly Electricity Generation",
        "Data Source": "Central Electricity Authority (CEA)",
        "Date Range": "2015 to 2026",
        "Number of Records": "3,960 Monthly Regional Records",
        "Update Frequency": "Monthly",
        "Format": "Excel / CSV",
        "Last Updated": "1st of Current Month"
    },
    {
        "Dataset Name": "IMD Weather & Solar Irradiation Covariates",
        "Data Source": "India Meteorological Department (IMD)",
        "Date Range": "2018 to Present",
        "Number of Records": "70,000+ Station Readings",
        "Update Frequency": "Hourly",
        "Format": "NetCDF / JSON",
        "Last Updated": "1 Hour ago"
    },
    {
        "Dataset Name": "BEE Appliance Energy Consumption Norms",
        "Data Source": "Bureau of Energy Efficiency (BEE)",
        "Date Range": "2022 to 2026",
        "Number of Records": "1,450 Certified Models",
        "Update Frequency": "Quarterly",
        "Format": "CSV / PDF Gazette",
        "Last Updated": "Quarter 2, 2026"
    },
    {
        "Dataset Name": "National Rooftop Solar Generation Telemetry",
        "Data Source": "MNRE / National Solar Mission",
        "Date Range": "2023 to Present",
        "Number of Records": "18,200 Inverter Feeds",
        "Update Frequency": "Daily",
        "Format": "CSV",
        "Last Updated": "Yesterday 23:59"
    }
]

# =====================================================
# 6. OFFICIAL GAZETTE REPORTS DATABASE
# =====================================================
OFFICIAL_REPORTS_LIST = [
    {
        "id": "rep_daily",
        "title": "Daily National Electricity Demand Forecast Report",
        "doc_number": "CEA/DP/2026/D-254",
        "date": "Daily (Updated 06:00 AM IST)",
        "pages": 14,
        "format": "PDF / CSV",
        "summary": "Comprehensive 24-hour hour-by-hour demand outlook across all five regional grids, peaker ramp forecast, and inter-state transmission flow margins."
    },
    {
        "id": "rep_weekly",
        "title": "Weekly Inter-Regional Grid Outlook & Reserve Margins",
        "doc_number": "GRID-INDIA/W-2026-36",
        "date": "Weekly (Every Monday)",
        "pages": 28,
        "format": "PDF / CSV",
        "summary": "7-day lookahead analyzing weather forecasts, thermal coal availability, hydro reservoir levels, and spinning reserves across Northern and Western corridors."
    },
    {
        "id": "rep_monthly",
        "title": "Monthly National Clean Energy & Decarbonization Review",
        "doc_number": "BEE/SDG7/2026-M08",
        "date": "Monthly Gazette",
        "pages": 46,
        "format": "PDF / CSV",
        "summary": "Assessment of India's non-fossil capacity expansion, CO₂ avoided, state-wise renewable compliance targets, and SDG Target 7.2 progress."
    },
    {
        "id": "rep_renewable",
        "title": "Comprehensive Renewable Integration & Curtailment Audit",
        "doc_number": "MNRE/RES-INT/2026-Q2",
        "date": "Quarterly Publication",
        "pages": 62,
        "format": "PDF / CSV",
        "summary": "Deep dive into solar park dispatch, wind generation seasonality, battery energy storage system (BESS) cycles, and transmission grid absorption."
    },
    {
        "id": "rep_peak",
        "title": "Peak Demand & Time-of-Day (ToD) Load Shifting Analysis",
        "doc_number": "POSOCO/PEAK/TOD-09",
        "date": "Bi-Annual Study",
        "pages": 38,
        "format": "PDF / CSV",
        "summary": "Statistical evaluation of evening peak stress, seasonal air conditioning load penetration, and DISCOM tariff incentive effectiveness."
    },
    {
        "id": "rep_state",
        "title": "State-Wise Electricity Demand & Transmission Performance Index",
        "doc_number": "CEA/STATE-INDEX/2026",
        "date": "Annual White Paper",
        "pages": 84,
        "format": "PDF / CSV",
        "summary": "Comparative scorecard for all 28 states measuring forecasting accuracy, transmission losses (AT&C), renewable adoption, and smart meter rollouts."
    }
]

def generate_sample_dataset_csv() -> bytes:
    """Generates an authentic municipal/regional sample energy dataset."""
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    np.random.seed(42)
    base_gw = 210.0
    actual_gw = [round(base_gw + np.sin(i / 3) * 12 + np.random.normal(0, 3), 2) for i in range(30)]
    forecast_gw = [round(actual_gw[i] + np.random.normal(0, 2.5), 2) for i in range(30)]
    solar_gw = [round(45.0 + np.sin(i / 4) * 8 + np.random.normal(0, 2), 2) for i in range(30)]
    wind_gw = [round(32.0 + np.cos(i / 3) * 6 + np.random.normal(0, 1.8), 2) for i in range(30)]
    frequency_hz = [round(50.0 + np.random.normal(0, 0.03), 3) for i in range(30)]

    df = pd.DataFrame({
        "Timestamp": dates.strftime('%Y-%m-%d'),
        "Actual_Demand_GW": actual_gw,
        "AI_Forecast_Demand_GW": forecast_gw,
        "Solar_Generation_GW": solar_gw,
        "Wind_Generation_GW": wind_gw,
        "Hydro_Generation_GW": [round(18.5 + np.random.normal(0, 1), 2) for _ in range(30)],
        "Grid_Frequency_Hz": frequency_hz,
        "Peak_Flag": ["YES" if val > 218 else "NO" for val in actual_gw]
    })
    return df.to_csv(index=False).encode('utf-8')
