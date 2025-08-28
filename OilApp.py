import streamlit as st
import pandas as pd
import joblib
import calendar

df = pd.read_csv("oilwell_features_clean.csv")
# --- Load Model ---
@st.cache_resource
def load_model():
    """Load the trained model and feature names from disk."""
    model_file = "gradient_boosting_model.pkl"
    features_file = "features_names.pkl"

    mdl = joblib.load(model_file)
    feat_names = joblib.load(features_file)

    return mdl, feat_names

# --- Load Dataset for Thresholds ---
@st.cache_resource
def load_data():
    df = pd.read_csv("oilwell_features_clean.csv")   # <-- replace with your dataset path

    return df


# Calculate dynamic thresholds
water_cut_warn = df["water_cut_%"].quantile(0.75)  # 75th percentile
reservoir_pressure_low = df["reservoir_pressure_atm"].quantile(0.25) # 25th percentile


# Load model once
model, feature_names = load_model()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Oil Well Project 🛢️",
    page_icon="⛽",
    layout="wide"
)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Input Well Parameters")

# Inputs with validation
vol_liquid = st.sidebar.number_input(
    "Volume of liquid (m³/day) 🛢️", min_value=000.0, max_value=150.0, step=10.0,
    help="Enter the produced liquid volume per day"
)

water_volume = st.sidebar.number_input(
    "Water volume (m³/day) 💧", min_value=000.0, max_value=100.0, step=10.0,
    help="Enter the produced water volume per day"
)

water_cut = st.sidebar.slider(
    "Water cut (%) 💦", min_value=000, max_value=100, value=50,
    help="Percentage of water in the produced liquid"
)

working_hours = st.sidebar.number_input(
    "Working hours ⏱️", min_value=0, max_value=24, value=12,
    help="Enter the number of operating hours per day"
)

dyn_level = st.sidebar.number_input(
    "Dynamic level (m) 📏", min_value=0000.0, max_value=2500.0, step=100.0,
    help="Dynamic fluid level in meters"
)

reservoir_pressure = st.sidebar.number_input(
    "Reservoir pressure (atm) 🌡️", min_value=000.0, max_value=250.0, step=10.0,
    help="Reservoir pressure in atm"
)

# Date Inputs
year = st.sidebar.selectbox("Year 📅", list(range(2013, 2022)))
month = st.sidebar.number_input("Month (1-12)", min_value=1, max_value=12, step=1)
days_in_month = calendar.monthrange(year, month)[1]  # auto adjust for leap years
day = st.sidebar.number_input("Day of Month", min_value=1, max_value=days_in_month, step=1)

# --- MAIN PAGE ---
st.title("ML Powered Oil Well Monitoring Dashboard 🛢️⛽")
st.markdown("Welcome to the **ML Powered Oil Well Project Dashboard**. Monitor key parameters and run predictions on oil well performance using Ml model.")

# Display selected date
st.subheader("📅 Selected Date")
st.write(f"**{day}/{month}/{year}**")

# Show input summary
st.subheader("📊 Input Summary")
st.write(f"- Volume of liquid: **{vol_liquid} m³/day**")
st.write(f"- Water volume: **{water_volume} m³/day**")
st.write(f"- Water cut: **{water_cut}%**")
st.write(f"- Working hours: **{working_hours} hrs**")
st.write(f"- Dynamic level: **{dyn_level} m**")
st.write(f"- Reservoir pressure: **{reservoir_pressure} atm**")

# --- Prediction Section ---
if st.sidebar.button("🔮 Run Prediction"):
    # Prepare input data in same feature order as training
    input_data = pd.DataFrame([[
        vol_liquid, water_volume, water_cut,
        working_hours, dyn_level, reservoir_pressure,
        year, month, day
    ]], columns=feature_names)

    prediction = model.predict(input_data)[0]
    st.subheader("🔮 Prediction Result")
    st.success(f"Predicted Oil Well Output: **{prediction:.2f} m3/day**")

# --- Insights ---
st.subheader("🔍 Project Insights")
st.markdown("""
Oil wells are critical assets in petroleum production. Monitoring these parameters ensures 
efficient extraction and management of resources.  

- High **water cut** may indicate reservoir maturity or breakthrough.  
- **Dynamic level** changes can reflect well productivity.  
- **Reservoir pressure** monitoring helps optimize lifting techniques.  

⚡ Data-driven decisions can enhance oil recovery and extend field life.
""")

st.image(
    'https://imgs.search.brave.com/iEgWEIGbvjbCh1GSdaEjGP8ub4F6X5qgqYVaNruwt40/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzEwLzMzLzYxLzI2/LzM2MF9GXzEwMzM2/MTI2NjJfNm02MWVq/OHpaa3BrZ1dicTJk/QXFxdmI3OEc5Q1dy/NlQuanBn',
    caption="Offshore Oil Rig 🌊🛢️"
)

# Only show insights if values are actually entered
if water_cut and reservoir_pressure:
    if water_cut > water_cut_warn:
        st.warning(f"⚠️ High water cut detected! Current: {water_cut}% "
                   f"(above 75th percentile: {water_cut_warn:.1f}%).")
    elif reservoir_pressure < reservoir_pressure_low:
        st.error(f"❌ Low reservoir pressure! Current: {reservoir_pressure} atm "
                 f"(below 25th percentile: {reservoir_pressure_low:.1f} atm).")
    else:
        st.success("✅ Parameters within expected range. Well is performing optimally.")
