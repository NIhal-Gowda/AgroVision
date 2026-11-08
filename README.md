# 🌾 AgroVision

> **Built for Google Cloud: Meet the Builders**  
> Early Crop Disease Detection, Microclimate Risk Forecasting & Precision Fertilizer Recommender Powered by **Google Vertex AI** and **Gemini Multimodal**.

---

## 🌟 What Problem Does AgroVision Solve?

Most smallholder farmers only detect crop diseases after necrosis, fungal rot, or severe wilting sets in—when 30% to 70% of potential yield is already lost. Furthermore, improper fertilizer usage (over-applying Nitrogen/Urea and under-applying micronutrients) degrades soil biology and wastes money.

**AgroVision** solves this by:
1. **Early Pathogen & Deficiency Detection:** Uses Gemini Multimodal AI to detect subtle early symptoms (marginal chlorosis, pinpoint spots, leaf curl) before visible destruction spreads.
2. **Microclimate Context Fusion:** Correlates real-time weather telemetry (humidity, rain, temperature) with pathogen proliferation models to alert farmers *before* fungal spores multiply.
3. **Precision Fertilizer & Treatment Prescription:** Calculates exact dosages (NPK, micronutrients) and provides eco-friendly, organic alternatives (Neem, Trichoderma, Jeevamrutha).
4. **Rural Accessibility with Regional Voice:** Generates localized audio advisories in regional languages (Hindi, Kannada, Telugu, Tamil, Marathi, Bengali, Spanish, English) for farmers who prefer audio guidance.

---

## ☁️ Google Cloud Architecture

```
┌────────────────────────────────────────────────────────┐
│               Farmer Interface (Mobile / PWA)          │
│   - Field Camera Scan & Live Diagnostic Dashboard      │
│   - Regional Audio Guidance (Voice Synthesis)          │
└───────────────────────────┬────────────────────────────┘
                            │ (HTTPS)
                            ▼
┌────────────────────────────────────────────────────────┐
│            Google Cloud Run (Serverless Host)          │
│   - Scalable container with zero idle-cost             │
│   - Weather & Telemetry Risk Aggregator Engine         │
│   - NPK Precision Optimization Service                 │
└────────────┬─────────────────────────────┬─────────────┘
             │                             │
             ▼                             ▼
┌─────────────────────────┐   ┌──────────────────────────┐
│   Google Vertex AI /    │   │  Cloud Storage & Data    │
│    Gemini Multimodal    │   │  - GCS for leaf images   │
│ - Sub-second diagnosis  │   │  - Firestore for farm    │
│ - Agronomic reasoning   │   │    records & alerts      │
└─────────────────────────┘   └──────────────────────────┘
```

---

## 🚀 Quickstart (Local Run)

### 1. Prerequisites
- Python 3.10+
- (Optional) Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 2. Installation
```bash
cd agrovision
pip install -r requirements.txt
```

### 3. Run the App
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

> **Note:** If no Gemini API key is configured, AgroVision runs in **Demo Mode**, using built-in high-accuracy agronomic simulation data so judges can test without setup friction.

---

## 🚢 Deploy to Google Cloud Run

Deploy directly from your terminal with one command:

```bash
# Set your Google Cloud project
gcloud config set project YOUR_PROJECT_ID

# Deploy container directly to Cloud Run
gcloud run deploy agrovision \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GEMINI_API_KEY="YOUR_KEY_HERE"
```

---

## 📂 Project Structure

```
agrovision/
├── app.py               # Streamlit application UI with 4 feature tabs
├── analyzer.py          # Vertex AI & Gemini multimodal crop diagnostic engine
├── weather_service.py   # Microclimate risk analysis & Open-Meteo telemetry
├── audio_service.py     # Multilingual voice advisory generator (gTTS)
├── config.py            # Crop types, soil profiles, and NPK baseline data
├── Dockerfile           # Production container for Google Cloud Run
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
└── README.md            # Project documentation & pitch guide
```
