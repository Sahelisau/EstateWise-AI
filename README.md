# EstateWise AI

EstateWise AI is a CSE570 project for exploring residential property data and predicting prices with supervised regression. The model, recommendation tools, and any market analysis will be built from the inspected dataset; the app will not invent listings or train a model on startup.

## Project folders

- `data/raw/` — original datasets as received. Keep these unchanged.
- `data/processed/` — cleaned data created by project scripts.
- `models/` — trained model pipeline and its metadata.
- `notebooks/` — guided exploration and analysis.
- `src/` — data loading, preprocessing, training, evaluation, and prediction code.
- `ui/` — modular Streamlit pages, charts, shared components, and theme.
- `reports/figures/` — charts saved for the report.
- `reports/` — evaluation results and the project report.
- `app.py` — Streamlit application entry point.

## Dataset status

The primary source is [House Price (India) by Juhi Bhojani on Kaggle](https://www.kaggle.com/datasets/juhibhojani/house-price). The original ZIP is expected at `data/raw/india_property_listings_81_cities.zip`; it is not included in the repository while the source-page license remains unverified. Download it from Kaggle and leave the archive unchanged. The secondary archive has no verified source or license and its geography does not match India. See [data/README.md](data/README.md) for the source description, attribution, fields, and data-handling rules.

Raw archives, cleaned listing-level rows, model binaries, and per-record prediction exports are ignored by Git. This keeps source data out of a public repository until licensing is verified and means a fresh clone needs the primary dataset and a trained model before launching the app.

## Setup

Use Python 3.11 or newer. From this folder, create and activate a virtual environment in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Training happens separately from launching the app. It is never triggered by the prediction interface.

## Data cleaning and exploration

Run the current cleaning and EDA workflow:

```powershell
python -m src.eda
```

It writes `data/processed/cleaned_properties.csv`, data summaries under `reports/`, and PNG figures under `reports/figures/`.

## Train and evaluate

Train the models after cleaning the data:

```powershell
python -m src.train
```

Evaluate the saved model on the held-out test split:

```powershell
python -m src.evaluate
```

Training saves the complete preprocessing and prediction pipeline in `models/property_price_model.pkl`, the fitted transformer separately in `models/preprocessing_pipeline.pkl`, and model details in `models/model_metadata.json`. The comparison and evaluation results are saved under `reports/`.

## Run the application

Start Streamlit from the project folder:

```powershell
streamlit run app.py
```

The app loads the saved model and never retrains on startup. If the model artifact is missing, train it first with `python -m src.train`. Forecasting and buy-vs-wait scenarios stay unavailable until dated market data is added and validated.

The interface includes Overview, Property Predictor, Explore Locations, Recommendations, Market Insights, Future Forecast, Buy vs Wait, Model Performance, and About EstateWise. City profiles and recommendations use the cleaned historical dataset; they are not current sale listings. The forecast and buy-vs-wait pages explain which dated market and financing data is missing instead of displaying invented results.

## Project architecture

- `src/data_loader.py` and `src/preprocessing.py` load and clean the source archive.
- `src/eda.py` creates the cleaned dataset, exploratory charts, summaries, and location statistical comparison.
- `src/model_utils.py`, `src/train.py`, and `src/evaluate.py` prepare splits, train and compare regressors, tune the Random Forest, and write held-out evaluation outputs.
- `src/predict.py` validates supported inputs and loads the saved model for inference.
- `ui/` contains the Streamlit pages, shared presentation components, charts, theme, and data loaders.
- `tests/test_project.py` provides repeatable smoke checks for data, prediction, evaluation, and recommendation functions.

## Model results

The saved Random Forest was selected using three-fold validation RMSE and evaluated on a held-out 20% split. Current results are MAE **₹2,883,725**, RMSE **₹10,405,736**, and R² **0.620**. These results describe this historical dataset and are not a current home valuation. See `reports/model_training_summary.md` and `reports/model_comparison.csv` for details.

## Screenshots

Screenshots are not included yet. Run the app using the instructions above, then add verified desktop and narrow-screen captures under `docs/screenshots/` before publishing and link them here. Do not use mock data in screenshots.

## Known limitations

- The source contains historical asking prices without listing dates, so the app does not show current listings, price appreciation, or future forecasts.
- It covers flats only and does not include structured localities, property age, or a complete amenities field.
- The secondary archive is excluded because its location and source license are unverified.
- The test RMSE is high relative to the MAE, which indicates a small number of large prediction errors. Model estimates should not be treated as official valuations or investment advice.
- The source dataset license must be verified on Kaggle before publishing source or modified listing records. More details are in `data/README.md`.

## Future improvements

- Verify the primary dataset license and add a documented download procedure for a new clone.
- Add independently sourced, dated city price indices before implementing forecasting or buy-vs-wait scenarios.
- Add locality-level and property-type data if a reliable source becomes available.
- Add screenshots and a simple automated GitHub Actions test workflow after the repository is created.

## GitHub repository

Repository URL: **not published yet**. This project has not been pushed to GitHub. The code license is MIT in `LICENSE`; it does not change the separate terms governing third-party datasets. See `data/README.md` before adding any dataset files.

After creating an empty GitHub repository, connect and push the local `main` branch:

```powershell
git remote add origin https://github.com/<your-username>/EstateWise-AI.git
git push -u origin main
```

For later changes, use a feature branch, commit the change, push that branch, and open a pull request against `main`:

```powershell
git switch -c docs/describe-your-change
git add README.md
git commit -m "docs: describe project change"
git push -u origin docs/describe-your-change
```

Review `git status` before every commit to ensure local archives and generated record-level files are not staged. No remote repository has been created or modified in this phase.

## Test the project

After installing `requirements.txt`, run the smoke tests from the project folder:

```powershell
python -m unittest discover -s tests -v
```

The tests load and clean the supplied data, check the train/test split, load the saved model, verify predictions and invalid-input handling, check recommendation filters and metrics, and confirm the app load path does not train or overwrite the model. The suite should report eight passing tests.

Phase 6 verification also ran `python -m src.eda` and `python -m src.evaluate` in a clean virtual environment. EDA returned 63,108 cleaned rows across 81 city labels; held-out metrics were MAE ₹2,883,725, RMSE ₹10,405,736 and R² 0.620. The clean-environment Streamlit app started and served the Overview page.

## Current status

Phases 0–7 local preparation are complete. The trained Random Forest and preprocessing pipeline are saved locally in `models/`; training and evaluation results are in `reports/`. The responsive dark Streamlit interface is organized in `ui/`, and model training remains separate from app startup. Eight Phase 6 smoke tests passed in a clean environment. The project has not been pushed to GitHub; the source data license check must be completed before deciding whether any data files can be published.
