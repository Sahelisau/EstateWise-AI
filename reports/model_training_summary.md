# Model training results

- Selected model: Random Forest
- Training records: 50,486; held-out test records: 12,622
- Split: 80:20, random state 42; model comparison used shuffled 3-fold cross-validation on training data.
- Preprocessing is inside each model pipeline, so imputers and encoders are fitted separately within each training fold.
- Selection used validation RMSE. Selected CV RMSE: ₹8,468,140; tuned forest CV RMSE: ₹8,628,888.
- Held-out test MAE: ₹2,883,725; RMSE: ₹10,405,736; R²: 0.620.
- Compared with the median dummy baseline, test MAE was 52.9% lower and test RMSE was 39.8% lower.
- The tuned forest had a lower test MAE (₹2,760,104) but higher CV RMSE than the selected forest; selection followed the predeclared CV RMSE criterion.
- The decision tree's test RMSE (₹10,289,718) was slightly lower than the selected forest's, while its CV RMSE was higher. The test set was kept for final reporting rather than model selection.

## Cross-validation and test comparison

- Random Forest: CV MAE ₹2,902,412, CV RMSE ₹8,468,140, CV R² 0.670; test MAE ₹2,883,725, test RMSE ₹10,405,736, test R² 0.620.
- Random Forest (tuned): CV MAE ₹2,786,760, CV RMSE ₹8,628,888, CV R² 0.658; test MAE ₹2,760,104, test RMSE ₹10,888,483, test R² 0.584.
- Decision Tree: CV MAE ₹3,264,508, CV RMSE ₹9,476,427, CV R² 0.585; test MAE ₹3,220,523, test RMSE ₹10,289,718, test R² 0.629.
- Gradient Boosting: CV MAE ₹3,827,333, CV RMSE ₹11,213,572, CV R² 0.423; test MAE ₹3,870,738, test RMSE ₹13,531,886, test R² 0.358.
- Dummy median baseline: CV MAE ₹6,067,790, CV RMSE ₹15,206,454, CV R² -0.062; test MAE ₹6,127,721, test RMSE ₹17,277,988, test R² -0.047.
- Linear Regression: CV MAE ₹4,361,309, CV RMSE ₹61,418,998, CV R² -18.611; test MAE ₹5,867,842, test RMSE ₹180,280,724, test R² -112.940.

## Feature importance

The selected tree model's largest impurity-based importance values were `numeric__area_sqft` (62.8%), `numeric__bathrooms` (8.5%), `category__city_mumbai` (5.5%), `category__city_new-delhi` (3.6%), `category__city_gurgaon` (2.4%). These scores describe how the forest used transformed features; they do not show cause and can favor continuous features with many possible split points.

## Reading the result

The model improves substantially on the dummy baseline, but the held-out RMSE remains large because a few high-price errors count heavily. The MAE is the more direct typical absolute-error summary. This is a listing-price estimate from an older dataset, not a current valuation. The cross-city dataset has no structured locality feature and covers flats only.

Model comparison is in `reports/model_comparison.csv`; held-out predictions and error slices are in `reports/`; model details and the data fingerprint are in `models/model_metadata.json`.
