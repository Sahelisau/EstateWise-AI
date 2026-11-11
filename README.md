# 🏡 EstateWise-AI: Real Estate Valuation & Market Intelligence

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

End-to-end machine learning solution for predicting property valuations and analyzing housing market trends using Python.

---

## 🚀 Project Overview

**EstateWise-AI** is an advanced, Streamlit-powered web application designed to estimate residential flat asking prices and explore historical property data across Indian real estate markets. 

This repository is structured so that development is **incremental**: every workflow stage is organized into clean Jupyter notebooks and modular scripts, allowing you to track data exploration, preprocessing, feature engineering, model training, and evaluation individually.

---

## ✨ Key Features

* **Interactive Price Prediction:** User-friendly Streamlit interface allowing users to input property features (location, size, bedrooms, amenities) and get instant valuation estimates.
* **Exploratory Data Analysis (EDA):** Comprehensive notebooks covering correlation heatmaps, price distributions, and geospatial trend insights.
* **Robust Machine Learning Pipelines:** Built with optimized regression models (Random Forest, XGBoost) featuring rigorous cross-validation.
* **Visual Performance Tracking:** Automated generation of residual plots, RMSE, and $R^2$ performance metrics.

---

## 🛠️ Tech Stack & Libraries

* **Core Language:** Python 3.10+
* **Data Manipulation & Analysis:** Pandas, NumPy, SciPy
* **Machine Learning:** Scikit-Learn, Joblib
* **Data Visualization:** Matplotlib, Seaborn, Plotly
* **Web Application UI:** Streamlit, OpenPyXL

---

## 📂 Project Architecture & Rubric Coverage

| Section / Stage | Description | Key Artifact / File |
| :--- | :--- | :--- |
| **Problem Statement & Dataset** | Housing market data ingestion & initial inspection | `data/` + `README.md` |
| **Data Cleaning & Preprocessing** | Handling missing values, outliers, and scaling | `02_data_cleaning_and_eda.ipynb` |
| **EDA & Statistical Analysis** | Correlation heatmaps, price distributions, and feature insights | `reports/figures/correlation_heatmap.png` |
| **Model Development & Training** | Training regression models (Random Forest, XGBoost) | `03_model_training.ipynb` |
| **Model Evaluation & Testing** | Residual analysis, RMSE, and $R^2$ performance metrics | `04_model_evaluation.ipynb` |
| **Deployment / App** | Interactive Streamlit interface for property predictions | `app.py` |

---

## 🔄 Project Workflow / Run Order

These notebooks and scripts should be run **in order** because each stage reads the output file of the previous stage:
1. `01_data_exploration.ipynb` — Initial data profile and inspection.
2. `02_data_cleaning_and_eda.ipynb` — Data cleansing and visual charts generation.
3. `03_model_training.ipynb` — Training baseline and optimized ML models.
4. `04_model_evaluation.ipynb` — Assessing model accuracy and generating performance plots.

---

## 💻 Installation & Running Locally

Follow these steps to set up and run the project on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Sahelisau/EstateWise-AI.git](https://github.com/Sahelisau/EstateWise-AI.git)
   cd EstateWise-AI