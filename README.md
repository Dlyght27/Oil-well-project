# Oil-well-project
The Oil Well Monitoring App is an interactive dashboard built with Streamlit to track and analyze oil well performance. It uses a dataset of well parameters and applies percentile-based thresholds to detect anomalies in oil well. 
# 🛢️ Oil Well Monitoring App

A **Streamlit-based interactive dashboard** for monitoring oil well performance.  
The app provides real-time insights into key production parameters such as **water cut** and **reservoir pressure**, and raises warnings when values exceed safe thresholds.

---

## 🚀 Features
- 📊 **Data-driven insights** using percentiles (e.g., 75th percentile for water cut, 25th percentile for pressure).
- ⚠️ **Automated alerts**:
  - High **Water Cut** warning
  - Low **Reservoir Pressure** warning
- 🌍 **Interactive Streamlit dashboard** with visuals and embedded images.
- ✅ **Threshold-based health check** to ensure wells are performing optimally.

---

## 🗂️ Project Structure

Oil-Well-Project/
│
├── OilApp.py # Main Streamlit application
├── script.py # Data cleaning & preprocessing script
├── dataset.csv # Cleaned dataset (with renamed columns)
├── requirements.txt # Python dependencies
└── README.md # Project documentation
