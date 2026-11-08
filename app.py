"""
AgroVision - Intelligent Crop Health & Precision Agronomy System
Built for Google Cloud: Meet the Builders
"""

import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

# Load local environment if present
load_dotenv()

from config import (
    SUPPORTED_CROPS,
    SOIL_TYPES,
    GROWTH_STAGES,
    SUPPORTED_LANGUAGES,
    CROP_NPK_REQUIREMENTS
)
from weather_service import fetch_farm_weather
from analyzer import analyze_crop_image
from audio_service import generate_voice_advisory

# Page Configuration
st.set_page_config(
    page_title="AgroVision | Google Cloud Meet the Builders",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Theme Accents */
    :root {
        --agri-green: #2e7d32;
        --agri-light: #e8f5e9;
        --gcp-blue: #4285f4;
        --gcp-yellow: #fbbc05;
        --gcp-red: #ea4335;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #388e3c 100%);
        padding: 24px 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .gcp-tag {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    .metric-box {
        background: #f9fbe7;
        border-left: 4px solid #7cb342;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    
    .fert-box {
        background: #e3f2fd;
        border-left: 4px solid #1e88e5;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .organic-box {
        background: #f1f8e9;
        border-left: 4px solid #43a047;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 10px;
    }
    
    .optimism-box {
        background: #fffde7;
        border-left: 4px solid #fbc02d;
        padding: 14px 18px;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image("https://www.gstatic.com/devrel-devsite/prod/v2b6c934b1c2b53648a7b97330c6a51268ee7f070bf5f14e4bdf00f34deab5d20/cloud/images/cloud-logo.svg", width=180)
    st.markdown("### 🚜 **AgroVision Settings**")
    
    # API Key Configuration
    env_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini / Vertex AI Key",
        value=env_key,
        type="password",
        help="Enter your Google AI Studio or Vertex AI Key. Leave blank to run in Demo Simulation Mode."
    )
    
    active_api_key = api_key_input.strip() if api_key_input else None
    
    if not active_api_key:
        st.info("💡 **Demo Mode Active**: Running on high-precision agronomic models. Add an API key for live Gemini 2.5 Flash analysis.")
    else:
        st.success("⚡ **Live Gemini Connected**")

    st.markdown("---")
    st.markdown("#### 🌾 **Farm Profile**")
    
    selected_location = st.text_input("Farm Location / District", value="Bengaluru, India")
    selected_crop = st.selectbox("Crop Type", SUPPORTED_CROPS, index=0)
    selected_soil = st.selectbox("Soil Type", SOIL_TYPES, index=0)
    selected_stage = st.selectbox("Current Growth Stage", GROWTH_STAGES, index=1)
    
    selected_lang_name = st.selectbox(
        "Advisory Voice & Language", 
        list(SUPPORTED_LANGUAGES.keys()),
        index=0
    )
    lang_info = SUPPORTED_LANGUAGES[selected_lang_name]

    st.markdown("---")
    # Fetch and show live weather context
    with st.spinner("Fetching microclimate telemetry..."):
        weather = fetch_farm_weather(selected_location)
    
    st.markdown("#### 🌦️ **Microclimate Telemetry**")
    col_w1, col_w2 = st.columns(2)
    col_w1.metric("Temperature", f"{weather['temperature_c']} °C")
    col_w2.metric("Humidity", f"{weather['humidity_percent']} %")
    
    st.markdown(
        f"<div style='background-color: {weather['risk_badge_color']}22; "
        f"border-left: 4px solid {weather['risk_badge_color']}; padding: 8px 12px; border-radius: 6px;'>"
        f"<strong>Fungal Pressure:</strong> {weather['pathogen_risk']}<br>"
        f"<small>{weather['risk_summary']}</small></div>",
        unsafe_allow_html=True
    )

    st.markdown("<br><small style='color: #888;'>Google Cloud Meet the Builders 2026</small>", unsafe_allow_html=True)


# ------------------ MAIN HEADER ------------------
st.markdown(f"""
<div class="main-header">
    <span class="gcp-tag">🚀 GOOGLE CLOUD: MEET THE BUILDERS</span>
    <h1 style="margin: 0; padding: 0; font-size: 2.2rem; font-weight: 700;">🌾 AgroVision</h1>
    <p style="margin: 6px 0 0 0; opacity: 0.95; font-size: 1.05rem;">
        Early Crop Disease Prediction & Precision Fertilizer Recommender Powered by <b>Google Vertex AI</b> & <b>Gemini</b>
    </p>
</div>
""", unsafe_allow_html=True)


# ------------------ APP TABS ------------------
tab_scan, tab_fert, tab_outbreak, tab_arch = st.tabs([
    "📸 Crop Scanner & AI Diagnosis",
    "🧪 Precision Fertilizer Calculator",
    "⛈️ Disease Outbreak Predictor",
    "☁️ Google Cloud Architecture"
])


# ==========================================
# TAB 1: CROP SCANNER & AI DIAGNOSIS
# ==========================================
with tab_scan:
    st.markdown("### 🔍 **Upload or Capture Crop Leaf Image**")
    st.write("Scan early discoloration, wilting, or spot patterns to identify disease before it spreads across your field.")

    col_input1, col_input2 = st.columns([1, 1])
    
    image_to_analyze = None
    
    with col_input1:
        input_mode = st.radio("Choose Input Method:", ["Upload Image File", "Use Camera"], horizontal=True)
        
        if input_mode == "Upload Image File":
            uploaded_file = st.file_uploader(
                "Upload a close-up photo of the crop leaf/stem (JPG, PNG)", 
                type=["jpg", "jpeg", "png"]
            )
            if uploaded_file:
                image_to_analyze = Image.open(uploaded_file)
        else:
            camera_file = st.camera_input("Capture live photo from field camera")
            if camera_file:
                image_to_analyze = Image.open(camera_file)

    with col_input2:
        if image_to_analyze:
            st.image(image_to_analyze, caption="Selected Crop Specimen", use_container_width=True)
        else:
            st.info("👆 Upload an image or take a photo to initiate early disease detection.")

    st.markdown("---")
    
    analyze_btn = st.button("🚀 Analyze Crop with Google Cloud AI", type="primary", use_container_width=True)
    
    if analyze_btn:
        if not image_to_analyze:
            # Load a fallback sample if user clicked without uploading
            st.warning("⚠️ No image was uploaded. Running analysis on sample field specimen for the selected crop profile...")
            # Create a simple mock image canvas for demonstration
            image_to_analyze = Image.new("RGB", (400, 400), color=(100, 160, 60))

        with st.spinner("🤖 Vertex AI / Gemini inspecting leaf cellular structure and microclimate risk..."):
            result = analyze_crop_image(
                image=image_to_analyze,
                crop_name=selected_crop,
                soil_type=selected_soil,
                growth_stage=selected_stage,
                weather_info=weather,
                language_name=selected_lang_name,
                api_key=active_api_key
            )

        # Store in session state
        st.session_state["latest_result"] = result

    # Display Analysis Results
    if "latest_result" in st.session_state:
        res = st.session_state["latest_result"]
        
        # Status banner color
        status = res.get("health_status", "Healthy")
        if status in ["Healthy", "Optimal Healthy Crop"]:
            status_color = "#2e7d32"
            status_bg = "#e8f5e9"
            status_icon = "✅"
        elif status in ["Early Warning", "Nutrient Deficient"]:
            status_color = "#f57c00"
            status_bg = "#fff3e0"
            status_icon = "⚠️"
        else:
            status_color = "#c62828"
            status_bg = "#ffebee"
            status_icon = "🚨"

        st.markdown(f"""
        <div style="background-color: {status_bg}; border: 2px solid {status_color}; border-radius: 12px; padding: 18px 24px; margin: 20px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="color: {status_color}; margin: 0; font-size: 1.6rem;">{status_icon} {res.get('primary_diagnosis', 'Diagnosed Issue')}</h2>
                    <p style="margin: 4px 0 0 0; color: #555; font-style: italic;">Scientific: {res.get('scientific_name', 'N/A')}</p>
                </div>
                <div style="text-align: right;">
                    <span style="background-color: {status_color}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.95rem;">
                        {res.get('health_status', 'Status')}
                    </span>
                    <p style="margin: 6px 0 0 0; font-size: 0.85rem; color: #444;">Confidence: <b>{res.get('confidence_percentage', 90)}%</b> | Severity: <b>{res.get('severity_level', 'Low')}</b></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if res.get("is_simulated"):
            st.caption("ℹ️ *Agronomic Diagnostic Engine: Demo Simulation Mode (Add your Gemini API key in sidebar for custom image models)*")

        # Audio Voice Advisory Section
        audio_text = res.get("summary_for_farmer_audio", "")
        if audio_text:
            st.markdown(f"#### 🔊 **Voice Advisory ({selected_lang_name})**")
            st.write(f"💬 *\"{audio_text}\"*")
            
            with st.spinner("Generating local language voice advisory..."):
                audio_bytes = generate_voice_advisory(audio_text, lang_code=lang_info["code"])
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")

        st.markdown("---")

        # Two-column detailed breakdown
        col_res1, col_res2 = st.columns([1, 1])

        with col_res1:
            st.markdown("### 🔬 **Pathology & Early Warning Signs**")
            
            st.markdown("**Observable Early Symptoms:**")
            for symptom in res.get("early_warning_signals", []):
                st.markdown(f"- 🔎 {symptom}")
            
            st.markdown("<br>**Root Environmental / Biological Causes:**", unsafe_allow_html=True)
            for cause in res.get("root_causes", []):
                st.markdown(f"- 🌧️ {cause}")

            st.markdown("---")
            st.markdown("### 🌟 **Optimistic Agronomist Advisory**")
            st.write("Forward-looking practices to boost resilience and maximize yield:")
            for tip in res.get("optimistic_farming_tips", []):
                st.markdown(f"""
                <div class="optimism-box">
                    💡 {tip}
                </div>
                """, unsafe_allow_html=True)

        with col_res2:
            st.markdown("### 🧪 **Precision Fertilizer & Treatment Prescription**")
            
            fert = res.get("fertilizer_prescription", {})
            st.markdown(f"""
            <div class="fert-box">
                <h4 style="margin-top: 0; color: #0d47a1;">🎯 Recommended Nutrition / Formulation</h4>
                <p style="font-size: 1.15rem; font-weight: bold; color: #1565c0; margin: 4px 0;">{fert.get('recommended_fertilizer', 'Balanced NPK')}</p>
                <hr style="margin: 8px 0; border: 0.5px solid #bbdefb;">
                <p><b>📏 Dosage:</b> {fert.get('dosage_per_acre', 'Consult agronomist')}</p>
                <p><b>🚜 Method:</b> {fert.get('application_method', 'Foliar Spray')}</p>
                <p><b>⏰ Timing:</b> {fert.get('application_timing', 'Early morning')}</p>
                <p><b>🔄 Frequency:</b> {fert.get('frequency', 'Every 10 days')}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>#### 🌿 **Organic & Eco-Friendly Alternatives**", unsafe_allow_html=True)
            for org in res.get("organic_eco_friendly_alternatives", []):
                st.markdown(f"""
                <div class="organic-box">
                    🌱 <b>Bio-Solution:</b> {org}
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# TAB 2: PRECISION FERTILIZER CALCULATOR
# ==========================================
with tab_fert:
    st.markdown("### 📐 **Precision N-P-K & Manure Calculator**")
    st.write("Calculate the exact chemical and organic fertilizer dosage tailored to your farm acreage to prevent nutrient waste and soil acidity.")

    col_fc1, col_fc2 = st.columns([1, 1])
    
    with col_fc1:
        calc_crop = st.selectbox("Select Crop for Nutrition Plan", list(CROP_NPK_REQUIREMENTS.keys()), key="calc_crop")
        farm_size = st.number_input("Farm Area (in Acres)", min_value=0.25, max_value=500.0, value=2.0, step=0.5)
        application_type = st.radio("Farming Preference", ["Integrated (Chemical + Organic)", "100% Organic / Regenerative"])
        soil_fertility = st.select_slider("Current Soil Organic Carbon / Fertility Status", options=["Low", "Medium", "High"], value="Medium")

    crop_needs = CROP_NPK_REQUIREMENTS.get(calc_crop, {"N": 40, "P": 20, "K": 20, "organic_base": "Compost 2 tons/acre"})
    
    # Fertility factor
    factor = 1.15 if soil_fertility == "Low" else (0.9 if soil_fertility == "High" else 1.0)
    
    total_n = round(crop_needs["N"] * farm_size * factor, 1)
    total_p = round(crop_needs["P"] * farm_size * factor, 1)
    total_k = round(crop_needs["K"] * farm_size * factor, 1)
    
    # Urea (46% N), DAP (18% N, 46% P2O5), MOP (60% K2O)
    dap_bags_50kg = round((total_p / 0.46) / 50, 1)
    n_from_dap = dap_bags_50kg * 50 * 0.18
    remaining_n = max(0, total_n - n_from_dap)
    urea_bags_50kg = round((remaining_n / 0.46) / 50, 1)
    mop_bags_50kg = round((total_k / 0.60) / 50, 1)

    with col_fc2:
        st.markdown(f"#### 📊 **Calculated Nutrition Requirements ({farm_size} Acres)**")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Nitrogen (N)", f"{total_n} kg")
        m2.metric("Phosphorus (P)", f"{total_p} kg")
        m3.metric("Potassium (K)", f"{total_k} kg")
        
        st.markdown("---")
        
        if application_type == "Integrated (Chemical + Organic)":
            st.markdown("##### 📦 **Commercial Fertilizer Schedule (50kg Bags)**")
            st.write(f"- 🟦 **Urea (46% N):** `{urea_bags_50kg} bags` (Apply in 2-3 split doses)")
            st.write(f"- 🟩 **DAP (18-46-0):** `{dap_bags_50kg} bags` (Apply full dose as basal application)")
            st.write(f"- 🟧 **MOP / Potash (60% K):** `{mop_bags_50kg} bags` (Apply 50% basal, 50% flowering)")
            st.write(f"- 🟫 **Organic Basal Foundation:** `{crop_needs.get('organic_base', 'Compost')}`")
        else:
            st.markdown("##### 🌿 **100% Organic & Regenerative Prescription**")
            st.write(f"- 🟫 **Enriched Vermicompost:** `{round(farm_size * 2.5, 1)} Tons`")
            st.write(f"- 🍃 **Neem Cake powder:** `{round(farm_size * 200)} kg` (Prevents nematodes & slow releases N)")
            st.write(f"- 🧪 **Bio-fertilizers (Azotobacter + PSB):** `{round(farm_size * 4)} kg` mixed with compost")
            st.write(f"- 💧 **Fermented Jeevamrutha:** `200 Liters / acre` applied every 15 days via irrigation")


# ==========================================
# TAB 3: DISEASE OUTBREAK PREDICTOR
# ==========================================
with tab_outbreak:
    st.markdown("### ⛈️ **Microclimate Pathogen Proliferation Forecast**")
    st.write("AgroVision cross-references regional humidity, dew point, and temperature trends to flag outbreak vulnerabilities 3 to 5 days ahead.")

    col_ob1, col_ob2 = st.columns([1, 1])
    
    with col_ob1:
        st.markdown(f"#### 📍 Farm Location: **{weather['location']}**")
        st.metric("Live Ambient Temp", f"{weather['temperature_c']} °C")
        st.metric("Relative Humidity", f"{weather['humidity_percent']} %")
        st.metric("Precipitation Probability", f"{weather['rain_probability']} %")
        st.metric("Wind Speed", f"{weather['wind_kmh']} km/h")

    with col_ob2:
        st.markdown("#### 🛡️ **Predictive Pathogen Vulnerability Matrix**")
        
        st.markdown(f"""
        <div style="background-color: {weather['risk_badge_color']}15; border: 2px solid {weather['risk_badge_color']}; border-radius: 10px; padding: 16px;">
            <h4 style="color: {weather['risk_badge_color']}; margin-top: 0;">Calculated Risk Index: {weather['pathogen_risk']}</h4>
            <p>{weather['risk_summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>##### 📅 **Actionable Preventative Measures for Next 72 Hours:**", unsafe_allow_html=True)
        if weather['pathogen_risk'] in ["HIGH", "MODERATE"]:
            st.write("1. 🚫 **Avoid overhead sprinkler irrigation** in late afternoons to prevent damp foliage overnight.")
            st.write("2. 🛡️ **Apply preventative bio-agent** (Trichoderma or Bacillus) before the next rain event.")
            st.write("3. ✂️ **Inspect dense canopies** and perform moderate pruning to facilitate airflow.")
        else:
            st.write("1. ✅ **Favorable growing window** - ideal timing for scheduled foliar nutrition or fertigation.")
            st.write("2. 🔍 **Conduct routine scouting** for early sucking pests like thrips and whiteflies.")


# ==========================================
# TAB 4: GOOGLE CLOUD ARCHITECTURE
# ==========================================
with tab_arch:
    st.markdown("### ☁️ **AgroVision on Google Cloud Platform**")
    st.write("Designed and engineered for scalability, low-latency edge accessibility, and cost efficiency in the Google Cloud ecosystem.")

    st.markdown("""
    ```
    ┌────────────────────────────────────────────────────────────────────────┐
    │                        FARMER INTERFACE (Edge / PWA)                   │
    │  - Mobile / Tablet Camera Inspection                                   │
    │  - Regional Voice Synthesis (Tamil, Telugu, Kannada, Hindi, etc.)      │
    └───────────────────────────────────┬────────────────────────────────────┘
                                        │ (HTTPS / REST)
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                      GOOGLE CLOUD RUN (Backend)                        │
    │  - Serverless Container Autoscaling                                    │
    │  - Microclimate Telemetry Aggregator                                   │
    │  - Precision Fertilizer Optimization Engine                            │
    └──────────┬────────────────────────┬───────────────────────┬────────────┘
               │                        │                       │
               ▼                        ▼                       ▼
    ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐
    │   GOOGLE VERTEX AI   │ │ GOOGLE CLOUD STORAGE │ │   CLOUD FIRESTORE    │
    │   (Gemini 2.5 Flash) │ │        (GCS)         │ │                      │
    │ - Multimodal Vision  │ │ - Secure Leaf Scans  │ │ - Farm Soil Records  │
    │ - Symptom Extraction │ │ - Field Datasets     │ │ - Scan History Log   │
    │ - Agronomic Advisory │ │ - Signed Upload URLs │ │ - Outbreak Alert Map │
    └──────────────────────┘ └──────────────────────┘ └──────────────────────┘
    ```
    """)

    st.markdown("---")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    with col_g1:
        st.markdown("#### 🧠 **Vertex AI & Gemini**")
        st.write("Gemini 2.5 Flash processes leaf imagery with sub-second latency and grounds diagnostic output with microclimate weather data for accurate preventative advice.")

    with col_g2:
        st.markdown("#### 🚀 **Google Cloud Run**")
        st.write("Zero-cost idle compute with instant autoscaling to handle seasonal surges when regional crop outbreaks strike thousands of farmers simultaneously.")

    with col_g3:
        st.markdown("#### 🗄️ **Storage & Firestore**")
        st.write("Cloud Storage retains high-resolution crop imagery for continuous model retraining, while Firestore tracks regional outbreak hotspots across districts.")

    st.markdown("---")
    st.markdown("### 🏆 **Why AgroVision Stands Out for Meet the Builders**")
    st.write("""
    1. **Early Prevention vs. Post-Damage Detection:** Traditional tools only tell farmers their crop is dead. AgroVision spots early micro-symptoms and links them with weather patterns to save crops *before* irreversible yield loss.
    2. **Accessible to Rural Farmers:** Regional voice readout ensures farmers who cannot read technical chemical labels still get clear, spoken guidance in their native language.
    3. **Eco-Conscious Precision Farming:** Provides organic alternatives alongside chemical formulas to protect soil biodiversity and eliminate fertilizer over-application.
    """)
