"""
AI Energy Advisor & Prompt Engineering Engine
Supports IBM Granite / Watsonx REST API, generic OpenAI-compatible API,
and a grounded offline knowledge engine for zero-dependency demos.
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from config import SYSTEM_PROMPT
from core.rag_engine import get_knowledge_retriever
from core.validator import sanitize_user_text

def build_structured_prompt(
    task: str,
    persona: str,
    stats: Dict[str, Any],
    peak_info: Optional[Dict[str, Any]] = None,
    savings_info: Optional[Dict[str, Any]] = None,
    user_query: Optional[str] = None,
    retrieved_context: Optional[str] = None
) -> str:
    """
    Constructs a structured prompt incorporating user context, data stats, RAG knowledge, and guardrails.
    """
    prompt = f"""{SYSTEM_PROMPT}

USER PROFILE: {persona}

HISTORICAL USAGE METRICS:
- Sample Count: {stats.get('sample_count', 'N/A')} records
- Average Daily Usage: {stats.get('mean_kwh', 'N/A')} kWh
- Peak-to-Average Ratio: {stats.get('peak_to_avg_ratio', 'N/A')}
- Trend Direction: {stats.get('trend_direction', 'Stable')} (slope: {stats.get('trend_slope', 0)})
"""

    if peak_info:
        prompt += f"""
PEAK LOAD OBSERVATIONS:
- Spike Threshold: {peak_info.get('spike_threshold_kwh')} kWh
- Total Spikes Detected: {peak_info.get('spike_count')}
- Highest Usage Day of Week: {peak_info.get('highest_usage_day')} (avg {peak_info.get('highest_usage_day_avg')} kWh)
"""

    if savings_info:
        prompt += f"""
POTENTIAL SAVINGS ESTIMATE (Target {savings_info.get('reduction_percentage')}% reduction):
- Energy Saved: {savings_info.get('kwh_saved')} kWh
- Cost Saved: {savings_info.get('currency_symbol')}{savings_info.get('cost_saved')}
- Avoided Carbon: {savings_info.get('co2_saved_kg')} kg CO2
"""

    if retrieved_context:
        prompt += f"""
{retrieved_context}
"""

    if user_query:
        cleaned_query = sanitize_user_text(user_query)
        prompt += f"""
USER INQUIRY:
"{cleaned_query}"
"""

    prompt += f"""
TASK: {task}
INSTRUCTIONS:
1. Provide practical, high-impact suggestions tailored to the {persona}.
2. Quantify expected benefits (energy kWh, cost, or carbon) whenever possible.
3. Keep the tone encouraging, professional, and aligned with SDG 7.
4. Include a concise disclaimer that outputs are approximate guidance for decision support.
"""
    return prompt


def call_llm_api(
    prompt: str,
    api_provider: str = "offline",
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    model_name: Optional[str] = None
) -> Optional[str]:
    """
    Dispatches prompt to chosen LLM provider (IBM Watsonx / OpenAI compatible / Offline).
    """
    if api_provider == "ibm_watsonx" and api_key and project_id:
        try:
            # Watsonx generation REST API endpoint
            url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            body = {
                "input": prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 600,
                    "min_new_tokens": 10,
                    "stop_sequences": [],
                    "repetition_penalty": 1.1
                },
                "model_id": model_name or "ibm/granite-13b-chat-v2",
                "project_id": project_id
            }
            res = requests.post(url, headers=headers, json=body, timeout=20)
            if res.status_code == 200:
                data = res.json()
                return data["results"][0]["generated_text"].strip()
        except Exception:
            pass # Fallback to grounded offline engine

    elif api_provider == "openai_compatible" and api_key:
        try:
            endpoint = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            body = {
                "model": model_name or "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 600
            }
            res = requests.post(endpoint, headers=headers, json=body, timeout=20)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

    return None


def generate_offline_explanation(
    persona: str,
    stats: Dict[str, Any],
    forecast_summary: Dict[str, Any],
    peak_info: Dict[str, Any]
) -> str:
    """
    Intelligent built-in reasoning engine for offline demos.
    Produces rigorous, transparent, and persona-specific explanations without external APIs.
    """
    trend = stats.get('trend_direction', 'Stable')
    pct_change = forecast_summary.get('percentage_change', 0.0)
    change_direction = "higher" if pct_change > 0 else "lower"
    
    explanation = f"""### 📊 AI Forecast Breakdown & Insights

1. **Consumption Trajectory**:
   - Over the historical window, your consumption pattern was characterized as **{trend}** with an average daily baseline of **{stats.get('mean_kwh')} kWh**.
   - The AI forecast projects a **{abs(pct_change)}% {change_direction}** aggregate consumption for the upcoming {forecast_summary.get('forecast_days')} days (estimated total: **{forecast_summary.get('total_forecast_kwh')} kWh**).
   - Expected daily peak: **{forecast_summary.get('peak_predicted_day')}** with **{forecast_summary.get('peak_predicted_val')} kWh**.

2. **Load Characterization ({persona})**:
   - **Peak-to-Average Ratio (PAR)** is **{stats.get('peak_to_avg_ratio')}**. A ratio above 1.5 indicates clustered high-power appliance runs rather than uniform baseload.
   - Historical spikes were observed most heavily on **{peak_info.get('highest_usage_day')}** (averaging {peak_info.get('highest_usage_day_avg')} kWh).

3. **Key Drivers**:
   - Periodic appliance cycles (e.g. heating/cooling systems, washing loads, or continuous computer workstations).
   - Day-of-week occupancy variance typical of {persona.lower()} environments.

> *Disclaimer: This forecast is an AI-generated approximation based on historical data patterns and seasonal adjustments for decision-support.*
"""
    return explanation


def generate_offline_recommendations(
    persona: str,
    stats: Dict[str, Any],
    peak_info: Dict[str, Any],
    savings_info: Dict[str, Any],
    retrieved_context: Optional[str] = None
) -> str:
    """
    Intelligent built-in recommendation synthesis for offline demos.
    """
    tips = f"""### 💡 AI-Curated Energy Optimization Action Plan

Aligned with **UN SDG 7 (Target 7.3: Energy Efficiency)**:

1. **Immediate High-Impact Shift (Peak Shaving)**:
   - Your highest energy strain occurs on **{peak_info.get('highest_usage_day')}**.
   - Shifting discretionary high-wattage appliance usage (washing machines, electric kettles, water heaters) out of the 6:00 PM – 10:00 PM evening peak to off-peak hours cuts grid strain and lowers Time-of-Day utility bills.

2. **Thermostat & Baseline Discipline**:
   - If utilizing cooling or heating equipment, maintain the Bureau of Energy Efficiency standard of **24°C**. Each 1°C increase reduces compressor draw by approximately 6%.
   - Ensure ceiling fans run at moderate speeds to enhance air circulation.

3. **Standby Vampire Power Elimination**:
   - Idle electronics (laptops, monitors, television boxes) draw 5-10% in phantom loads. Use switched power boards to disconnect devices overnight.

4. **Projected Impact for You**:
   - By adopting a **{savings_info.get('reduction_percentage')}%** efficiency improvement:
     - ⚡ **{savings_info.get('kwh_saved')} kWh** conserved per period.
     - 💰 **{savings_info.get('currency_symbol')}{savings_info.get('cost_saved')}** saved directly on your electricity expenses.
     - 🌱 **{savings_info.get('co2_saved_kg')} kg CO₂** avoided (equivalent to planting **{savings_info.get('trees_equivalent')} mature trees**).

> *Note: Recommended actions adhere to ethical, safe, and transparent energy management standards.*
"""
    return tips


def ask_advisor_bot(
    user_query: str,
    chat_history: List[Dict[str, str]],
    persona: str,
    current_stats: Dict[str, Any],
    api_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main conversational agent loop:
    1. Sanitize user query (Anti-Injection)
    2. Query local RAG knowledge retriever
    3. Construct structured prompt
    4. Call API or use grounded domain reasoning
    5. Return grounded response with citations
    """
    cleaned_query = sanitize_user_text(user_query)
    
    # 1. RAG Retrieval
    retriever = get_knowledge_retriever()
    rag_results = retriever.retrieve(cleaned_query, top_k=2)
    context_block = retriever.format_context_block(rag_results)
    
    # 2. Build Structured Prompt
    task_desc = "Answer the user's question clearly, citing energy conservation principles and UN SDG 7 targets where applicable."
    full_prompt = build_structured_prompt(
        task=task_desc,
        persona=persona,
        stats=current_stats,
        user_query=cleaned_query,
        retrieved_context=context_block
    )
    
    # 3. Try LLM API
    api_response = call_llm_api(
        prompt=full_prompt,
        api_provider=api_config.get("provider", "offline"),
        api_key=api_config.get("api_key"),
        project_id=api_config.get("project_id"),
        model_name=api_config.get("model_name")
    )
    
    if api_response:
        final_answer = api_response
    else:
        # Fallback to grounded conversational response using RAG context
        final_answer = format_offline_chat_response(cleaned_query, rag_results, persona, current_stats)

    return {
        "answer": final_answer,
        "sources": [r["source"] for r in rag_results],
        "rag_snippets": rag_results
    }


def format_offline_chat_response(
    query: str,
    rag_results: List[Dict[str, Any]],
    persona: str,
    stats: Dict[str, Any]
) -> str:
    """
    Synthesizes a grounded response using RAG snippets when offline.
    """
    query_lower = query.lower()
    
    intro = f"Based on your profile as a **{persona}** (current avg: **{stats.get('mean_kwh', 'N/A')} kWh/day**) and energy conservation benchmarks:"
    
    specific_advice = ""
    if "ac" in query_lower or "air condition" in query_lower or "cooling" in query_lower:
        specific_advice = (
            "• **Air Conditioning**: Maintain thermostat at **24°C**. Every degree increase saves ~6% energy. "
            "Clean dust filters every 14 days for optimal airflow. Pre-cooling before 6 PM avoids expensive peak tariff periods."
        )
    elif "geyser" in query_lower or "water heater" in query_lower:
        specific_advice = (
            "• **Water Heating**: A 2000W geyser consumes 1 kWh in just 30 minutes! "
            "Switch on only 20-30 minutes prior to use instead of maintaining continuous thermostat cycling. Descale annually."
        )
    elif "refrigerator" in query_lower or "fridge" in query_lower:
        specific_advice = (
            "• **Refrigeration**: Keep freezer at -18°C and fridge compartment at 3-4°C. "
            "Never store warm food directly. Leave at least 5 cm clearance around rear coils for heat dissipation."
        )
    elif "laptop" in query_lower or "computer" in query_lower or "hostel" in query_lower:
        specific_advice = (
            "• **Electronics**: Enable power-saving sleep plans (screen off after 5 mins, sleep after 15 mins). "
            "Switch off charger bricks at the socket when done to eliminate 3W-10W continuous vampire draw."
        )
    elif "peak" in query_lower or "time" in query_lower:
        specific_advice = (
            "• **Peak Load Shifting**: Peak demand windows generally run from 7:00-10:00 AM and 6:00-10:00 PM. "
            "Run washing machines, pumps, and heavy charging sessions during off-peak slots (after 10 PM or solar noon 11 AM-3 PM)."
        )
    else:
        specific_advice = (
            "• **General Optimization**: Focus on eliminating phantom loads (unplugging idle appliances), "
            "staggering high-wattage equipment to prevent demand surges, and adopting 5-star BEE or Energy Star rated devices."
        )

    # Add RAG snippet highlights if found
    rag_highlight = ""
    if rag_results:
        top_snippet = rag_results[0]['snippet'].replace('\n', ' ')
        rag_highlight = f"\n\n> 📖 **Referenced Guide ({rag_results[0]['source']})**:\n> *\"{top_snippet}\"*"

    footer = "\n\n*SDG 7 Alignment: Small habitual changes aggregate to substantial carbon reductions across communities.*"
    
    return f"{intro}\n\n{specific_advice}{rag_highlight}{footer}"
