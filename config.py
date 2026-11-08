# AgroVision - Google Cloud: Meet the Builders
# Configuration & Master Data

SUPPORTED_CROPS = [
    "Tomato",
    "Potato",
    "Rice (Paddy)",
    "Wheat",
    "Maize (Corn)",
    "Cotton",
    "Soybean",
    "Chilli / Pepper",
    "Sugarcane",
    "Onion",
    "Banana",
    "Coffee",
    "Tea",
    "Apple",
    "Grapes",
    "Groundnut / Peanut",
    "Areca Nut (Betel Nut)",
    "Coconut"
]

SOIL_TYPES = [
    "Alluvial Soil (River basin / Loamy)",
    "Black Cotton Soil (Regur / Heavy Clay)",
    "Red & Yellow Soil (Iron-rich)",
    "Laterite Soil (Acidic / Leached)",
    "Sandy Loam (Well-drained)",
    "Clay Loam (Moisture-retentive)"
]

GROWTH_STAGES = [
    "Germination / Seedling Stage",
    "Vegetative Growth Stage",
    "Flowering & Budding Stage",
    "Fruit / Pod Formation Stage",
    "Maturation / Pre-Harvest Stage"
]

SUPPORTED_LANGUAGES = {
    "English": {"code": "en", "native": "English"},
    "Hindi": {"code": "hi", "native": "हिंदी"},
    "Kannada": {"code": "kn", "native": "ಕನ್ನಡ"},
    "Telugu": {"code": "te", "native": "తెలుగు"},
    "Tamil": {"code": "ta", "native": "தமிழ்"},
    "Marathi": {"code": "mr", "native": "मराठी"},
    "Bengali": {"code": "bn", "native": "বাংলা"},
    "Spanish": {"code": "es", "native": "Español"}
}

# Standard NPK Baselines (kg/acre) for Calculator
CROP_NPK_REQUIREMENTS = {
    "Tomato": {"N": 40, "P": 25, "K": 35, "organic_base": "Vermicompost 2 tons/acre"},
    "Potato": {"N": 50, "P": 30, "K": 45, "organic_base": "Well-rotted Farmyard Manure (FYM) 4 tons/acre"},
    "Rice (Paddy)": {"N": 45, "P": 20, "K": 20, "organic_base": "Green Manure (Dhaincha) incorporation"},
    "Wheat": {"N": 48, "P": 24, "K": 16, "organic_base": "FYM 3 tons/acre + Azotobacter"},
    "Maize (Corn)": {"N": 48, "P": 24, "K": 20, "organic_base": "Poultry manure 1.5 tons/acre"},
    "Cotton": {"N": 35, "P": 18, "K": 18, "organic_base": "Castor cake 400 kg/acre"},
    "Chilli / Pepper": {"N": 40, "P": 20, "K": 30, "organic_base": "Neem cake 250 kg/acre"},
    "Soybean": {"N": 12, "P": 32, "K": 16, "organic_base": "Rhizobium inoculation + Compost"},
    "Areca Nut (Betel Nut)": {"N": 50, "P": 20, "K": 70, "organic_base": "Compost 12 kg/palm + Neem cake 1 kg/palm"},
    "Coconut": {"N": 35, "P": 22, "K": 84, "organic_base": "50 kg Farmyard Manure (FYM) + Sunnhemp green manure/palm"}
}
