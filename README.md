# 🌱 AgriSense  
### **A Rule-Based Expert System for Crop Disease Diagnosis & Fertilizer Recommendation**

AgriSense is an intelligent agricultural advisory system built using **Python**, **Experta**, and **Streamlit**.  
The system uses **rule-based reasoning** to diagnose crop diseases, suggest treatments, and recommend fertilizers based on soil, weather, crop growth stage, symptoms, pests, and lab test values.

---

## 🚀 Features

- ✔ Rule-based reasoning using **Experta (PyKnow)**
- ✔ Easy-to-use web interface powered by **Streamlit**
- ✔ Diagnoses crop diseases based on symptoms
- ✔ Provides fertilizer recommendations using NPK and soil data
- ✔ Weather-based risk alerts
- ✔ Pest-based advisory
- ✔ Growth-stage specific insights
- ✔ Supports multiple crops (Tomato, Wheat, Maize, Rice, etc.)

---

## 📁 Project Structure

agrisense-expert-system/
│
├── agrisense.py # Expert System Rules & Facts
├── agri_streamlit.py # Streamlit Web UI
└── README.md # Documentation



---

## ⚙️ Installation

## Clone the repository:

```bash
git clone https://github.com/<your-username>/agrisense-expert-system.git
cd agrisense-expert-system


### ▶️ Running the App Locally

To launch the Streamlit app:

streamlit run agri_streamlit.py


This will open the web interface in your browser.

🌐 Deployment (Streamlit Cloud)

To deploy on Streamlit Community Cloud:

Push this repository to GitHub

Go to: https://share.streamlit.io

Click New App

Choose:

Repository: agrisense-expert-system

Branch: main

File: agri_streamlit.py

Click Deploy



🧠 How the Expert System Works

AgriSense uses Facts and Rules under the Expert System paradigm:

Facts include:

Crop type & growth stage

Soil type, pH, moisture

Lab NPK values

Weather conditions

Symptoms observed

Pest presence

Rules perform:

Disease matching

Weather-based disease risk

Fertilizer deficiency detection

Crop-stage recommendations

Pest-specific treatment advice

The system outputs:

Disease diagnosis

Treatment recommendation

Fertilizer advisory

Stage-wise crop management tips
