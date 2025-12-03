# agri_streamlit.py
import streamlit as st
from experta import *
from agrisense import AgriSenseEngine, Crop, Soil, Lab, Symptoms, Weather, PestPresence

# Page style
st.set_page_config(page_title="AgriSense - Crop Advisor", layout="wide")
st.markdown("<h1 style='text-align:center;'>🌱 AgriSense: Smart Crop Advisory System</h1>", unsafe_allow_html=True)
st.write("---")

# -------------------------------------------------------------------
# 1) Layout: Multi-column Inputs
# -------------------------------------------------------------------
st.header("📥 Input Section")

# ---- Crop Info ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌾 Crop Information")
    crop_name = st.selectbox("Select Crop", ["tomato", "wheat", "maize", "rice"])
    crop_stage = st.selectbox("Growth Stage", ["vegetative", "flowering", "fruiting"])

with col2:
    st.subheader("🧪 Soil Information")
    soil_type = st.selectbox("Soil Type", ["loam", "clay", "sandy"])
    soil_ph = st.number_input("Soil pH", 4.0, 9.0, 6.5)
    soil_moisture = st.selectbox("Soil Moisture", ["low", "adequate", "high"])

# ---- Lab Values ----
st.write("---")
col3, col4, col5 = st.columns(3)

with col3:
    st.subheader("⚗️ Nitrogen")
    N = st.number_input("Nitrogen (ppm)", 0, 500, 50)

with col4:
    st.subheader("🧫 Phosphorus")
    P = st.number_input("Phosphorus (ppm)", 0, 500, 50)

with col5:
    st.subheader("🧯 Potassium")
    K = st.number_input("Potassium (ppm)", 0, 500, 50)

# ---- Weather ----
st.write("---")
st.subheader("⛅ Weather Conditions")
colW1, colW2, colW3 = st.columns(3)

with colW1:
    temp = st.number_input("Temperature (°C)", -10, 50, 25)

with colW2:
    humidity = st.number_input("Humidity (%)", 0, 100, 70)

with colW3:
    recent_rain = st.number_input("Recent Rain Days", 0, 30, 3)

# ---- Symptoms ----
st.write("---")
st.subheader("🩺 Symptoms Observed")

colS1, colS2, colS3 = st.columns(3)

with colS1:
    leaf_spots = st.checkbox("🔵 Leaf Spots")
    yellowing = st.checkbox("🟡 Yellowing")
    wilting = st.checkbox("🟤 Wilting")

with colS2:
    stem_lesions = st.checkbox("🟥 Stem Lesions")
    mosaic = st.checkbox("🟢 Mosaic Pattern")
    powdery_white = st.checkbox("⚪ Powdery White")

with colS3:
    black_sooty = st.checkbox("⚫ Black Sooty Mold")
    st.write("")

# ---- Pests ----
st.write("---")
st.subheader("🐛 Pest Presence")

colP1, colP2, colP3, colP4 = st.columns(4)
with colP1:
    aphids = st.checkbox("🪲 Aphids")
with colP2:
    mites = st.checkbox("🕷️ Mites")
with colP3:
    caterpillars = st.checkbox("🐛 Caterpillars")
with colP4:
    whiteflies = st.checkbox("🦟 Whiteflies")

# -------------------------------------------------------------------
# 2) Run the Expert System
# -------------------------------------------------------------------
st.write("---")
center = st.container()
with center:
    st.markdown("<h3 style='text-align:center;'>🔍 Analyze Inputs & Generate Recommendations</h3>", unsafe_allow_html=True)
    run_btn = st.button("🚀 Run AgriSense Expert System", use_container_width=True)

if run_btn:
    engine = AgriSenseEngine()
    engine.reset()

    # Declare collected facts
    engine.declare(Crop(name=crop_name, stage=crop_stage))
    engine.declare(Soil(type=soil_type, moisture=soil_moisture, ph=soil_ph))
    engine.declare(Lab(N=N, P=P, K=K, ph=soil_ph))
    engine.declare(Symptoms(
        leaf_spots=leaf_spots,
        yellowing=yellowing,
        wilting=wilting,
        stem_lesions=stem_lesions,
        mosaic=mosaic,
        powdery_white=powdery_white,
        black_sooty=black_sooty
    ))
    engine.declare(Weather(temp=temp, humidity=humidity, recent_rain_days=recent_rain))
    engine.declare(PestPresence(
        aphids=aphids, mites=mites,
        caterpillars=caterpillars, whiteflies=whiteflies
    ))

    engine.run()
    diagnoses, recs = engine.get_results()

    # -------------------------------------------------------------------
    # 3) Display Results using Cards
    # -------------------------------------------------------------------
    st.write("---")
    st.markdown("<h2 style='text-align:center;'>📊 Results</h2>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    # Diagnoses
    with colA:
        st.subheader("🩺 Diagnoses")
        if diagnoses:
            for d in diagnoses:
                st.success(f"**Disease:** {d.get('disease')}")
                st.write(f"**Confidence:** {d.get('confidence')}")
                st.info(d.get("notes"))
        else:
            st.info("No disease detected or insufficient data.")

    # Recommendations
    with colB:
        st.subheader("💡 Recommendations")
        if recs:
            for r in recs:
                if "treatment" in r:
                    st.warning(f"**Treatment:** {r['treatment']}")
                if "stage_advice" in r:
                    st.info(f"**Stage Advice:** {r['stage_advice']}")
                if "fertilizer_recommendations" in r:
                    st.success("**Fertilizer Recommendations:**")
                    for f in r["fertilizer_recommendations"]:
                        st.write(f"🌱 {f}")
        else:
            st.info("No recommendations available.")

# Footer
st.write("---")
st.markdown("<p style='text-align:center;'>🌾 Built with ❤️ using Streamlit & Experta</p>", unsafe_allow_html=True)
