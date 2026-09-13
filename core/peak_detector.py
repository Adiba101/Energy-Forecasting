"""
Peak Detector and Load-Shifting Optimizer
Identifies consumption spikes, peak days, and recommends peak-shaving / load-shifting schedules.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np

def detect_peak_days_and_anomalies(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detects spike days where energy consumption deviates significantly from the median/mean.
    """
    kwh = df['kwh'].values
    mean_val = float(np.mean(kwh))
    std_val = float(np.std(kwh)) if len(kwh) > 1 else 0.1
    
    # Threshold: mean + 1.25 * std
    spike_threshold = mean_val + 1.25 * std_val
    
    spike_records = []
    for _, row in df.iterrows():
        val = float(row['kwh'])
        if val >= spike_threshold:
            spike_records.append({
                "date": pd.to_datetime(row['date']).strftime("%Y-%m-%d (%a)"),
                "kwh": round(val, 2),
                "excess_kwh": round(val - mean_val, 2),
                "excess_pct": round(((val - mean_val) / mean_val) * 100, 1) if mean_val > 0 else 0
            })
            
    # Day-of-week ranking
    df_dow = df.copy()
    df_dow['day_name'] = pd.to_datetime(df_dow['date']).dt.day_name()
    dow_avg = df_dow.groupby('day_name')['kwh'].mean().reset_index()
    dow_avg = dow_avg.sort_values(by='kwh', ascending=False)
    
    highest_day = dow_avg.iloc[0]['day_name'] if not dow_avg.empty else "N/A"
    highest_day_avg = round(float(dow_avg.iloc[0]['kwh']), 2) if not dow_avg.empty else 0.0
    lowest_day = dow_avg.iloc[-1]['day_name'] if not dow_avg.empty else "N/A"
    lowest_day_avg = round(float(dow_avg.iloc[-1]['kwh']), 2) if not dow_avg.empty else 0.0

    return {
        "spike_threshold_kwh": round(spike_threshold, 2),
        "spike_count": len(spike_records),
        "spikes": spike_records[:5],  # top 5
        "highest_usage_day": highest_day,
        "highest_usage_day_avg": highest_day_avg,
        "lowest_usage_day": lowest_day,
        "lowest_usage_day_avg": lowest_day_avg,
        "dow_breakdown": dow_avg.to_dict('records')
    }


def generate_load_shifting_recommendations(
    persona: str,
    peak_info: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Generates tailored load-shifting strategies based on the user persona and peak findings.
    """
    strategies = []
    
    if "Hostel" in persona:
        strategies.extend([
            {
                "title": "Stagger Electric Geyser Usage",
                "current_practice": "Heating water during peak morning hours (7:30 AM - 9:30 AM).",
                "recommended_action": "Switch on geyser 30-45 minutes earlier (before 7:00 AM) or share hot water batches.",
                "potential_impact": "Avoids drawing 2000W during grid peak; saves up to 15% on peak hostel power quota."
            },
            {
                "title": "Laptop & Device Charging Window",
                "current_practice": "Plugging in laptops and power banks continuously during evening peak study hours.",
                "recommended_action": "Charge devices during off-peak afternoon (1:00 PM - 4:00 PM) or after 10:00 PM.",
                "potential_impact": "Reduces room peak load by 65-100W."
            },
            {
                "title": "Study Lamp vs Ambient Room Tube",
                "current_practice": "Leaving dual 40W fluorescent ceiling fixtures on during midnight study.",
                "recommended_action": "Use a direct 5W-7W LED desk study lamp.",
                "potential_impact": "Cuts nighttime lighting power by 80%."
            }
        ])
    elif "Residential" in persona:
        strategies.extend([
            {
                "title": "Shift Heavy Laundry to Off-Peak / Solar Hours",
                "current_practice": "Running washing machine and dryer during evening hours (7:00 PM - 9:00 PM).",
                "recommended_action": "Schedule wash cycles for 11:00 AM - 3:00 PM (solar abundance) or after 10:00 PM.",
                "potential_impact": "Shifts 500W-1500W load completely away from evening peak grid stress."
            },
            {
                "title": "Air Conditioner Pre-Cooling Strategy",
                "current_practice": "Turning AC down to 18°C-20°C right at 8:00 PM when returning home.",
                "recommended_action": "Set AC thermostat to 24°C-26°C with ceiling fan circulation. Pre-cool room at 5:00 PM.",
                "potential_impact": "Every 1°C increase in thermostat saves approximately 6% in AC electricity consumption."
            },
            {
                "title": "Eliminate Vampire / Standby Power",
                "current_practice": "Leaving smart TVs, microwave displays, and set-top boxes on standby 24/7.",
                "recommended_action": "Plug entertainment setup into a master switch power strip and power down at night.",
                "potential_impact": "Saves 15-30 kWh per month effortlessly."
            }
        ])
    else:  # Small Office / Shop
        strategies.extend([
            {
                "title": "HVAC Pre-Cooling & Night Purge",
                "current_practice": "Starting all AC compressors simultaneously at 9:00 AM during grid ramp-up.",
                "recommended_action": "Stagger AC startup: unit 1 at 8:30 AM, unit 2 at 9:00 AM; set thermostat to 24°C.",
                "potential_impact": "Flattens initial maximum demand spike by 30-40%."
            },
            {
                "title": "Non-Critical Server / Backup Scheduling",
                "current_practice": "Running large data synchronizations, backups, and printer jobs at 2:00 PM.",
                "recommended_action": "Automate batch backup tasks and server indexing to trigger after 11:00 PM.",
                "potential_impact": "Reduces continuous daytime baseline load."
            },
            {
                "title": "Zoned Motion-Sensed Display & Restroom Lighting",
                "current_practice": "Keeping all showroom / office zone lights on during lunch and off-hours.",
                "recommended_action": "Install PIR motion sensors in cabins, storage, and conference rooms.",
                "potential_impact": "Reduces lighting energy consumption by 25-35%."
            }
        ])

    return strategies


def generate_diurnal_hourly_profile(persona: str, daily_avg_kwh: float) -> pd.DataFrame:
    """
    Generates realistic 24-hour diurnal load curve (current vs shifted load)
    based on consumer persona and typical Indian / global utility peak curves.
    """
    hours = list(range(24))
    hour_labels = [f"{h:02d}:00" for h in hours]
    
    # Base fractional distribution across 24 hours summing to 1.0
    if "Hostel" in persona:
        # High late night / early morning, morning geyser spike, evening peak
        weights = [
            0.035, 0.030, 0.025, 0.025, 0.025, 0.030, # 00 - 05
            0.045, 0.085, 0.075, 0.040, 0.025, 0.025, # 06 - 11 (Geyser spike 7-8 AM)
            0.030, 0.035, 0.030, 0.030, 0.035, 0.045, # 12 - 17
            0.055, 0.075, 0.085, 0.070, 0.050, 0.045  # 18 - 23 (Evening study & gaming)
        ]
    elif "Residential" in persona:
        # Morning breakfast & appliances, quiet afternoon, huge evening AC/entertainment peak
        weights = [
            0.035, 0.030, 0.028, 0.025, 0.025, 0.030, # 00 - 05
            0.045, 0.065, 0.070, 0.050, 0.035, 0.035, # 06 - 11 (Morning rush)
            0.038, 0.040, 0.038, 0.035, 0.040, 0.050, # 12 - 17
            0.065, 0.085, 0.095, 0.085, 0.060, 0.045  # 18 - 23 (Evening peak cooling/cooking)
        ]
    else: # Small Office / Shop
        # Low night baseline, sharp 9 AM ramp, high business hours 9-18, sharp wind down
        weights = [
            0.015, 0.015, 0.015, 0.015, 0.015, 0.018, # 00 - 05 (Server baseload)
            0.020, 0.025, 0.045, 0.085, 0.095, 0.095, # 06 - 11 (Office open & HVAC ramp)
            0.090, 0.080, 0.085, 0.085, 0.085, 0.080, # 12 - 17 (Peak operations)
            0.055, 0.035, 0.025, 0.020, 0.016, 0.015  # 18 - 23 (Closing)
        ]

    # Normalize weights
    total_w = sum(weights)
    weights = [w / total_w for w in weights]
    
    current_kwh = [round(daily_avg_kwh * w, 3) for w in weights]
    
    # Generate shifted / optimized load
    # Flattens peaks by ~18% and redistributes into off-peak solar/night slots
    shifted_kwh = []
    for h, k in enumerate(current_kwh):
        if 7 <= h <= 10 or 18 <= h <= 21: # Peak hours
            shifted_kwh.append(round(k * 0.78, 3))
        elif 11 <= h <= 15: # Solar valley
            shifted_kwh.append(round(k * 1.15, 3))
        elif 22 <= h or h <= 5: # Night off-peak
            shifted_kwh.append(round(k * 1.08, 3))
        else:
            shifted_kwh.append(k)

    # Classification
    tod_categories = []
    for h in hours:
        if 7 <= h <= 10:
            tod_categories.append("Morning Peak (ToD +20%)")
        elif 18 <= h <= 21:
            tod_categories.append("Evening Peak (ToD +25%)")
        elif 11 <= h <= 15:
            tod_categories.append("Solar Hours (Clean Energy)")
        else:
            tod_categories.append("Night Off-Peak (ToD -15%)")

    return pd.DataFrame({
        "hour": hours,
        "hour_label": hour_labels,
        "current_load_kwh": current_kwh,
        "shifted_load_kwh": shifted_kwh,
        "tod_category": tod_categories
    })


def get_persona_appliance_breakdown(persona: str, total_kwh: float, tariff_rate: float) -> pd.DataFrame:
    """
    Returns estimated appliance consumption breakdown and expenditure.
    """
    if "Hostel" in persona:
        shares = [
            {"appliance": "Electric Geyser & Water Kettle", "pct": 32, "category": "Heating"},
            {"appliance": "Room Cooler & Ceiling Fan", "pct": 28, "category": "Cooling & Vent"},
            {"appliance": "Laptop, Monitor & Chargers", "pct": 22, "category": "Computing"},
            {"appliance": "Room Tube & Study Lights", "pct": 10, "category": "Lighting"},
            {"appliance": "Phantom / Standby Loads", "pct": 8, "category": "Standby Waste"},
        ]
    elif "Residential" in persona:
        shares = [
            {"appliance": "Air Conditioning (Split Inverter)", "pct": 42, "category": "Cooling"},
            {"appliance": "Frost-Free Refrigerator", "pct": 18, "category": "Refrigeration"},
            {"appliance": "Electric Geyser / Water Heater", "pct": 16, "category": "Heating"},
            {"appliance": "Washing Machine & Kitchen", "pct": 12, "category": "Major Appliances"},
            {"appliance": "LED Lighting & Fans", "pct": 7, "category": "Lighting & Fans"},
            {"appliance": "Vampire / Standby Electronics", "pct": 5, "category": "Standby Waste"},
        ]
    else: # Small Office / Shop
        shares = [
            {"appliance": "Central / Split HVAC Systems", "pct": 46, "category": "HVAC"},
            {"appliance": "Computer Workstations & Monitors", "pct": 26, "category": "IT Equipment"},
            {"appliance": "Network Servers & Switches", "pct": 12, "category": "Critical Infrastructure"},
            {"appliance": "Storefront & Office Lighting", "pct": 10, "category": "Lighting"},
            {"appliance": "Pantry, Dispenser & Standby", "pct": 6, "category": "Auxiliary"},
        ]

    records = []
    for item in shares:
        kwh_val = round(total_kwh * (item["pct"] / 100.0), 1)
        cost_val = round(kwh_val * tariff_rate, 1)
        records.append({
            "Appliance Group": item["appliance"],
            "Category": item["category"],
            "Share (%)": item["pct"],
            "Consumption (kWh)": kwh_val,
            "Expense Incurred": cost_val
        })

    return pd.DataFrame(records)

