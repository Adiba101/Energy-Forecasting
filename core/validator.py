"""
Input Validation and Sanitization Module
Ensures data integrity, realistic bounds, and prompt injection safety.
"""

import re
from typing import Dict, Any, Tuple, Optional
import pandas as pd

# Injection patterns to flag or neutralize
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s+prompt",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"jailbreak",
    r"<script.*?>",
    r"drop\s+table",
    r"--\s*$",
]

def sanitize_user_text(text: str) -> str:
    """
    Sanitize free-form user query to strip hazardous tokens or prompt injection attempts.
    """
    if not text:
        return ""
    
    cleaned = text.strip()
    
    # Check for obvious injection phrases and sanitize them
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            cleaned = re.sub(pattern, "[FILTERED_SECURITY_TOKEN]", cleaned, flags=re.IGNORECASE)
            
    # Remove HTML tags
    cleaned = re.sub(r"<[^>]*>", "", cleaned)
    
    return cleaned[:1000] # Limit length to prevent buffer bloat


def validate_manual_inputs(
    daily_kwh: float,
    tariff_rate: float,
    persona: str = "Residential Home (2-3 BHK)"
) -> Tuple[bool, Optional[str]]:
    """
    Validates user entered daily consumption and tariff rate.
    Returns (is_valid, error_message).
    """
    if daily_kwh is None or daily_kwh <= 0:
        return False, "Daily electricity consumption must be a positive number greater than 0."
        
    if daily_kwh > 5000:
        return False, "Daily consumption exceeds 5000 kWh, which is beyond the scope of domestic/small commercial tracking."
        
    if tariff_rate is None or tariff_rate <= 0:
        return False, "Tariff rate must be a positive number greater than 0."
        
    if tariff_rate > 100:
        return False, "Tariff rate seems unusually high (> ₹100 / $100 per kWh). Please verify."
        
    return True, None


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, Optional[str], Optional[pd.DataFrame]]:
    """
    Validates historical consumption DataFrame from CSV or manual entry.
    Requires a date column and a consumption column (kwh or units).
    """
    if df is None or df.empty:
        return False, "The provided dataset is empty.", None

    df_clean = df.copy()
    
    # Normalize column names
    col_map = {col: col.strip().lower() for col in df_clean.columns}
    df_clean.rename(columns=col_map, inplace=True)
    
    # Find date column
    date_col = None
    for candidate in ['date', 'timestamp', 'day', 'datetime', 'time']:
        if candidate in df_clean.columns:
            date_col = candidate
            break
            
    if not date_col:
        return False, "Dataset must include a 'Date' or 'Timestamp' column.", None

    # Find consumption column
    kwh_col = None
    for candidate in ['kwh', 'consumption_kwh', 'units', 'energy_kwh', 'consumption', 'power_kwh']:
        if candidate in df_clean.columns:
            kwh_col = candidate
            break
            
    if not kwh_col:
        return False, "Dataset must include an energy consumption column (e.g., 'kwh', 'units', 'consumption_kwh').", None

    try:
        df_clean['date'] = pd.to_datetime(df_clean[date_col])
    except Exception as e:
        return False, f"Failed to parse dates in column '{date_col}': {str(e)}", None

    # Convert kwh to numeric and drop invalid / negative values
    df_clean['kwh'] = pd.to_numeric(df_clean[kwh_col], errors='coerce')
    df_clean = df_clean.dropna(subset=['date', 'kwh'])
    df_clean = df_clean[df_clean['kwh'] >= 0]
    
    if len(df_clean) < 3:
        return False, "Dataset must contain at least 3 valid positive consumption records for forecasting.", None

    # Sort by date
    df_clean = df_clean.sort_values(by='date').reset_index(drop=True)
    
    return True, None, df_clean
