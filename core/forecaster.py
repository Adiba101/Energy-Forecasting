"""
Forecasting Engine
Provides explainable pattern-based, trend-aware, and seasonal forecasting for electricity consumption.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from datetime import timedelta

def calculate_usage_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes summary statistical metrics from historical daily consumption.
    """
    kwh = df['kwh'].values
    mean_val = float(np.mean(kwh))
    median_val = float(np.median(kwh))
    std_val = float(np.std(kwh)) if len(kwh) > 1 else 0.0
    min_val = float(np.min(kwh))
    max_val = float(np.max(kwh))
    total_val = float(np.sum(kwh))
    
    # Peak to Average Ratio (PAR)
    par = max_val / mean_val if mean_val > 0 else 1.0
    
    # Simple linear trend slope (kWh change per day)
    if len(kwh) >= 3:
        x = np.arange(len(kwh))
        slope, _ = np.polyfit(x, kwh, 1)
    else:
        slope = 0.0
        
    trend_direction = "Increasing" if slope > 0.05 else ("Decreasing" if slope < -0.05 else "Stable")

    return {
        "mean_kwh": round(mean_val, 2),
        "median_kwh": round(median_val, 2),
        "std_kwh": round(std_val, 2),
        "min_kwh": round(min_val, 2),
        "max_kwh": round(max_val, 2),
        "total_kwh": round(total_val, 2),
        "peak_to_avg_ratio": round(par, 2),
        "trend_slope": round(float(slope), 4),
        "trend_direction": trend_direction,
        "sample_count": len(kwh)
    }


def generate_forecast(df: pd.DataFrame, forecast_days: int = 7) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Generates an explainable time-series forecast for the next N days.
    Combines:
    1. Base level from exponential weighted moving average
    2. Linear trend momentum
    3. Day-of-week seasonality (weekend vs weekday multiplier)
    4. Gaussian confidence interval
    """
    df_sorted = df.sort_values(by='date').copy()
    kwh_series = df_sorted['kwh'].values
    dates = df_sorted['date'].values
    
    # 1. Day of week multipliers
    df_sorted['day_of_week'] = pd.to_datetime(df_sorted['date']).dt.dayofweek
    day_means = df_sorted.groupby('day_of_week')['kwh'].mean()
    overall_mean = np.mean(kwh_series) if len(kwh_series) > 0 else 1.0
    
    # Normalize day factor
    day_factors = {}
    for d in range(7):
        if d in day_means and overall_mean > 0:
            day_factors[d] = day_means[d] / overall_mean
        else:
            day_factors[d] = 1.0

    # 2. Baseline and Trend calculation
    # Exponential weighted moving average with alpha=0.3
    weights = np.exp(np.linspace(-1, 0, len(kwh_series)))
    weights /= weights.sum()
    weighted_baseline = np.sum(kwh_series * weights)
    
    # Trend slope
    if len(kwh_series) >= 5:
        x = np.arange(len(kwh_series))
        slope, _ = np.polyfit(x, kwh_series, 1)
        # Dampen trend slope to avoid runaway projections
        dampened_slope = slope * 0.5
    else:
        dampened_slope = 0.0

    # Standard deviation for confidence band
    std_residual = np.std(kwh_series) if len(kwh_series) > 1 else (0.1 * weighted_baseline)

    # 3. Forecast sequence
    last_date = pd.to_datetime(dates[-1])
    forecast_dates = []
    forecast_kwh = []
    lower_bounds = []
    upper_bounds = []

    for step in range(1, forecast_days + 1):
        target_date = last_date + timedelta(days=step)
        dow = target_date.dayofweek
        
        # Predicted value = (Baseline + step * trend) * Seasonality Factor
        trend_component = dampened_slope * step
        base_pred = max(0.5, (weighted_baseline + trend_component))
        seasonal_pred = base_pred * day_factors.get(dow, 1.0)
        
        # Ensure realistic non-negative values
        pred_val = max(0.2, round(seasonal_pred, 2))
        
        # Expanding uncertainty window over time
        uncertainty = 1.96 * std_residual * np.sqrt(1 + 0.05 * step)
        lower_val = max(0.1, round(pred_val - uncertainty, 2))
        upper_val = round(pred_val + uncertainty, 2)
        
        forecast_dates.append(target_date)
        forecast_kwh.append(pred_val)
        lower_bounds.append(lower_val)
        upper_bounds.append(upper_val)

    forecast_df = pd.DataFrame({
        "date": forecast_dates,
        "forecast_kwh": forecast_kwh,
        "lower_kwh": lower_bounds,
        "upper_kwh": upper_bounds,
        "day_name": [d.strftime("%A") for d in forecast_dates]
    })

    # Summary metrics
    total_forecast_kwh = float(np.sum(forecast_kwh))
    avg_forecast_kwh = float(np.mean(forecast_kwh))
    
    # Comparison to past window of same duration
    if len(kwh_series) >= forecast_days:
        past_window_total = float(np.sum(kwh_series[-forecast_days:]))
    else:
        past_window_total = float(np.mean(kwh_series) * forecast_days)
        
    pct_change = ((total_forecast_kwh - past_window_total) / past_window_total * 100) if past_window_total > 0 else 0.0

    summary = {
        "forecast_days": forecast_days,
        "total_forecast_kwh": round(total_forecast_kwh, 2),
        "avg_daily_forecast_kwh": round(avg_forecast_kwh, 2),
        "past_period_kwh": round(past_window_total, 2),
        "percentage_change": round(pct_change, 1),
        "peak_predicted_day": forecast_df.loc[forecast_df['forecast_kwh'].idxmax()]['date'].strftime("%Y-%m-%d (%A)"),
        "peak_predicted_val": float(forecast_df['forecast_kwh'].max()),
        "min_predicted_day": forecast_df.loc[forecast_df['forecast_kwh'].idxmin()]['date'].strftime("%Y-%m-%d (%A)"),
        "min_predicted_val": float(forecast_df['forecast_kwh'].min())
    }

    return forecast_df, summary
