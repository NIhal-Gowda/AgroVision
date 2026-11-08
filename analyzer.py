"""
AI Agronomic Analyzer for AgroVision
Integrates with Google Cloud Gemini Multimodal API via google-genai SDK.
Detects early crop diseases, nutrient deficiencies, recommends precise fertilizers,
and produces optimistic agronomy advice in multiple languages.
"""

import os
import json
import base64
from typing import Dict, Any, Optional
from PIL import Image
import io

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


SYSTEM_INSTRUCTION = """
You are AgroVision AI, an expert agricultural scientist, plant pathologist, and agronomist built for Google Cloud Meet the Builders.
Your goal is to inspect crop imagery, provide early disease detection BEFORE it causes yield loss, accurately diagnose issues (pathogenic, pest-related, or nutrient deficiency), and provide optimistic, practical farming recommendations with exact fertilizer formulations.

Always reply strictly in valid JSON matching this schema:
{
  "crop_identified": "Crop name",
  "health_status": "Healthy" | "Early Warning" | "Diseased" | "Nutrient Deficient" | "Pest Damage",
  "primary_diagnosis": "Common name of condition or 'Optimal Healthy Crop'",
  "scientific_name": "Scientific / botanical pathogen name or 'None'",
  "confidence_percentage": 92,
  "severity_level": "None" | "Low" | "Moderate" | "Severe" | "Critical",
  "early_warning_signals": [
    "Observable symptom 1 (e.g. faint yellowing on lower leaves)",
    "Observable symptom 2"
  ],
  "root_causes": [
    "Favorable humidity and soil moisture",
    "Microbial infection / insect vectors"
  ],
  "fertilizer_prescription": {
    "recommended_fertilizer": "Specific product name (e.g., NPK 19-19-19 or Calcium Nitrate or Chelated Zinc)",
    "dosage_per_acre": "Exact dosage (e.g., 2.5 kg per acre via foliar spray or 50 kg/ha)",
    "application_method": "Foliar Spray" | "Soil Drenching" | "Basal Application" | "Drip Fertigation",
    "application_timing": "Best time of day (e.g. early morning 6-8 AM)",
    "frequency": "Frequency (e.g. Every 10 days for 2 cycles)"
  },
  "organic_eco_friendly_alternatives": [
    "Organic remedy 1 (e.g., Cold-pressed Neem Oil 10,000 ppm spray @ 3ml/L)",
    "Organic remedy 2 (e.g., Trichoderma viride bio-fungicide or Jeevamrutha)"
  ],
  "optimistic_farming_tips": [
    "Forward-looking advice 1 to boost yield and plant immunity",
    "Forward-looking advice 2 to improve soil health and moisture retention",
    "Actionable crop management tip"
  ],
  "summary_for_farmer_audio": "A concise 2-3 sentence verbal summary written directly in the requested target language, explaining the diagnosis and what fertilizer or immediate action to take in simple, encouraging terms."
}
"""

def analyze_crop_image(
    image: Image.Image,
    crop_name: str,
    soil_type: str,
    growth_stage: str,
    weather_info: Dict[str, Any],
    language_name: str = "English",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes crop image using Gemini multimodal or mock simulation.
    """
    # 1. Check if API key is provided either as arg or env
    key = api_key or os.getenv("GEMINI_API_KEY")

    if not key or not GENAI_AVAILABLE:
        # Fallback to rich agronomic simulation
        return get_simulated_diagnosis(crop_name, soil_type, growth_stage, weather_info, language_name)

    try:
        client = genai.Client(api_key=key)

        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=85)
        img_bytes = img_byte_arr.getvalue()

        weather_context = (
            f"Local Weather: {weather_info.get('temperature_c', 28)}°C, "
            f"Relative Humidity: {weather_info.get('humidity_percent', 65)}%, "
            f"Rain Probability: {weather_info.get('rain_probability', 20)}%, "
            f"Pre-calculated Microclimate Disease Pressure: {weather_info.get('pathogen_risk', 'MODERATE')}."
        )

        user_prompt = f"""
Inspect this image for the specified crop:
- Targeted Crop: {crop_name}
- Soil Type: {soil_type}
- Growth Stage: {growth_stage}
- Environmental Weather Context: {weather_context}
- Farmer's Preferred Language for Audio Summary: {language_name}

Analyze the plant foliage, stems, or fruits in the image. 
Identify if there are any early symptoms of fungal blights, rust, bacterial wilt, viral leaf curl, insect infestation, or N-P-K / micronutrient deficiencies.
If the plant is completely healthy, celebrate it and provide growth-maximizing fertilizer and care tips.
Ensure the 'summary_for_farmer_audio' is translated directly into {language_name}.
Return strictly valid JSON.
"""

        # Call Gemini 2.5 Flash / 1.5 Flash
        # We try gemini-2.5-flash first, then gemini-1.5-flash
        model_name = "gemini-2.5-flash"

        response = client.models.generate_content(
            model=model_name,
            contents=[
                types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
                user_prompt
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.2
            )
        )

        text_response = response.text.strip()
        # Clean potential markdown fences
        if text_response.startswith("```json"):
            text_response = text_response[7:]
        if text_response.startswith("```"):
            text_response = text_response[3:]
        if text_response.endswith("```"):
            text_response = text_response[:-3]

        parsed = json.loads(text_response.strip())
        parsed["is_simulated"] = False
        return parsed

    except Exception as e:
        # If API quota or network fails, provide graceful simulation with notice
        simulated = get_simulated_diagnosis(crop_name, soil_type, growth_stage, weather_info, language_name)
        simulated["is_simulated"] = True
        simulated["simulation_reason"] = f"Live Gemini API note: {str(e)[:150]}"
        return simulated


def get_simulated_diagnosis(
    crop_name: str,
    soil_type: str,
    growth_stage: str,
    weather_info: Dict[str, Any],
    language_name: str
) -> Dict[str, Any]:
    """
    Curated high-accuracy agronomic knowledge base for offline or demo presentations.
    """
    crop_lower = crop_name.lower()
    
    if "tomato" in crop_lower:
        return {
            "crop_identified": "Tomato (Solanum lycopersicum)",
            "health_status": "Early Warning",
            "primary_diagnosis": "Early Blight & Nitrogen-Potassium Imbalance",
            "scientific_name": "Alternaria solani",
            "confidence_percentage": 94,
            "severity_level": "Low to Moderate",
            "early_warning_signals": [
                "Small dark concentric target-shaped spots emerging on lower, older leaves",
                "Faint yellow halo (chlorotic margin) surrounding necrotic lesions",
                "Slight downward curling of mid-tier foliage"
            ],
            "root_causes": [
                f"Elevated relative humidity ({weather_info.get('humidity_percent', 72)}%) combined with rain splashes",
                "Overcrowded canopy preventing laminar airflow",
                "Soil-borne fungal spores overwintering on organic debris"
            ],
            "fertilizer_prescription": {
                "recommended_fertilizer": "NPK 13:00:45 (Potassium Nitrate) + Mancozeb 75% WP",
                "dosage_per_acre": "500 grams Mancozeb + 1 kg Potassium Nitrate in 200 Liters of water per acre",
                "application_method": "Foliar Spray",
                "application_timing": "Early Morning (6:30 AM - 8:30 AM) before direct sunlight",
                "frequency": "2 sprays spaced 10 days apart"
            },
            "organic_eco_friendly_alternatives": [
                "Cold-pressed Neem Oil (10,000 ppm) @ 3.5 ml per liter with mild liquid soap emulsifier",
                "Trichoderma harzianum bio-fungicide drenching (5 grams/liter) around the root zone",
                "Sour buttermilk (Lactic acid + copper vessel aged) spray @ 50 ml/liter"
            ],
            "optimistic_farming_tips": [
                "Prune the bottom 25-30 cm of lower suckers to eliminate contact with splashing soil pathogens",
                "Apply paddy straw or dried mulch around the base to preserve moisture and suppress spore germination",
                "Potassium boost will strengthen the cell wall structure, resulting in firmer tomatoes with higher brix sweetness"
            ],
            "summary_for_farmer_audio": "Your tomato crop shows early signs of Early Blight spots and low potassium. Spray Potassium Nitrate with protective fungicide in the morning. Mulch the soil base to protect your yield and improve fruit quality.",
            "is_simulated": True
        }

    elif "rice" in crop_lower or "paddy" in crop_lower:
        return {
            "crop_identified": "Rice / Paddy (Oryza sativa)",
            "health_status": "Early Warning",
            "primary_diagnosis": "Incipient Blast & Zinc Deficiency (Khaira Disease)",
            "scientific_name": "Magnaporthe oryzae",
            "confidence_percentage": 91,
            "severity_level": "Low",
            "early_warning_signals": [
                "Elliptical spindle-shaped spots with grey centers on young leaf blades",
                "Rusty brown pigmentation starting on leaf surfaces due to zinc unavailability"
            ],
            "root_causes": [
                "Intermittent wet weather and cool nights creating extended dew duration",
                "Excessive un-split urea application rendering leaf cuticle softer to spore penetration",
                "Alkaline or waterlogged soil locking up zinc ions"
            ],
            "fertilizer_prescription": {
                "recommended_fertilizer": "Chelated Zinc (Zn-EDTA 12%) + Tricyclazole 75% WP",
                "dosage_per_acre": "Zinc EDTA 200g + Tricyclazole 120g per 150 liters water per acre",
                "application_method": "Foliar Spray",
                "application_timing": "Morning hours after dew has evaporated",
                "frequency": "Single targeted spray; inspect again in 7 days"
            },
            "organic_eco_friendly_alternatives": [
                "Pseudomonas fluorescens bio-agent @ 10g/liter foliar spray",
                "Application of 100 kg Neem cake per acre mixed with well-rotted farmyard manure"
            ],
            "optimistic_farming_tips": [
                "Adopt Alternate Wetting and Drying (AWD) water management to aerate roots and harden tillers",
                "Avoid single heavy doses of Urea; split nitrogen into 3 calibrated applications at tillering, panicle initiation, and boot leaf stage",
                "Zinc replenishment will accelerate chlorophyll synthesis and produce robust, golden panicles"
            ],
            "summary_for_farmer_audio": "Your paddy shows initial leaf blast spots and zinc deficiency. Apply Chelated Zinc with Tricyclazole as a morning foliar spray and manage water levels to secure high tiller counts.",
            "is_simulated": True
        }

    elif "potato" in crop_lower:
        return {
            "crop_identified": "Potato (Solanum tuberosum)",
            "health_status": "Diseased",
            "primary_diagnosis": "Late Blight Early Outbreak",
            "scientific_name": "Phytophthora infestans",
            "confidence_percentage": 93,
            "severity_level": "Moderate",
            "early_warning_signals": [
                "Water-soaked dark lesions near leaf tips and leaf margins",
                "Delicate white fungal down/mold visible on the underside of leaves during humid morning hours"
            ],
            "root_causes": [
                f"Continuous cool temperatures and relative humidity above 80%",
                "Poor soil aeration and microclimate stagnation"
            ],
            "fertilizer_prescription": {
                "recommended_fertilizer": "Cymoxanil 8% + Mancozeb 64% WP with Potassium Sulfate (0-0-50)",
                "dosage_per_acre": "600 grams of fungicide + 1.5 kg Potassium Sulfate per acre in 200L water",
                "application_method": "Foliar Spray with thorough underside leaf coverage",
                "application_timing": "Immediately in clear weather, avoid impending rainfall",
                "frequency": "2 applications at 7-day intervals"
            },
            "organic_eco_friendly_alternatives": [
                "Copper Oxychloride (COC 50% WP) @ 2.5g/L combined with Panchagavya (30ml/L)",
                "Bio-formulation of Bacillus subtilis drenching"
            ],
            "optimistic_farming_tips": [
                "Earth up the potato ridges to ensure tubers are buried at least 10 cm below surface, preventing spore wash into tubers",
                "Ensure row orientation allows sunlight penetration through the lower canopy",
                "Healthy potassium levels ensure uniform tuber sizing and prevent hollow-heart defect"
            ],
            "summary_for_farmer_audio": "Early Late Blight detected on your potatoes. Spray Cymoxanil-Mancozeb immediately and earth up soil ridges to safeguard the developing tubers.",
            "is_simulated": True
        }

    else:
        # Generic optimistic crop report
        return {
            "crop_identified": crop_name,
            "health_status": "Healthy & Thriving",
            "primary_diagnosis": "Optimal Vegetative Vigor with Minor Micro-Deficiency",
            "scientific_name": "None (Healthy Foliage)",
            "confidence_percentage": 96,
            "severity_level": "None",
            "early_warning_signals": [
                "Deep green foliage with active photosynthetic surface area",
                "Turgid stems with no active fungal lesions or pest punctures",
                "Very mild interveinal paling on newest growth (minor magnesium/iron requirement)"
            ],
            "root_causes": [
                "Good farm hygiene and favorable soil structure",
                "Normal micro-nutrient assimilation demand during rapid growth"
            ],
            "fertilizer_prescription": {
                "recommended_fertilizer": "Balanced NPK 19:19:19 + Magnesium Sulphate (Epsom Salt)",
                "dosage_per_acre": "NPK 19-19-19 @ 1 kg + Magnesium Sulphate @ 500g in 150L water per acre",
                "application_method": "Foliar Spray / Fertigation",
                "application_timing": "Late Afternoon (4:00 PM - 6:00 PM)",
                "frequency": "Once every 15 days during active growth"
            },
            "organic_eco_friendly_alternatives": [
                "Fermented Jeevamrutha foliar spray (200L/acre) filtered through muslin cloth",
                "Seaweed extract liquid @ 2.5 ml/L to enhance stress resilience"
            ],
            "optimistic_farming_tips": [
                "Maintain consistent soil moisture to prevent blossom-end drop or tip burn",
                "Encourage beneficial pollinator insects by inter-cropping marigolds or coriander along boundary rows",
                "Your crop is in prime condition—sticking to balanced nutrition now ensures maximum flowering conversion and bumper yield!"
            ],
            "summary_for_farmer_audio": f"Congratulations! Your {crop_name} is healthy and thriving. Give a balanced 19-19-19 foliar spray to boost flowering and secure a bumper harvest.",
            "is_simulated": True
        }
