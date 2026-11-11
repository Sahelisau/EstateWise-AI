import hashlib
import json
import math
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np

from src.data_loader import DEFAULT_DATA, ROOT, load_properties
from src.evaluate import metrics
from src.predict import load_artifacts, known_categories, predict_price
from src.preprocessing import clean_properties
from src.model_utils import load_split
from ui.recommendations import find_profiles


class ProjectSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, cls.metadata = load_artifacts()
        cls.categories = known_categories(cls.model)

    def sample(self, city=None, **changes):
        values = {
            "city": city or self.categories["city"][0],
            "area_sqft": 1_000,
            "area_basis": self.categories["area_basis"][0],
            "bedrooms": 2,
            "bathrooms": 2,
            "balconies": 1,
            "furnishing": self.categories["furnishing"][0],
            "facing": self.categories["facing"][0],
            "overlooking": self.categories["overlooking"][0],
            "ownership": self.categories["ownership"][0],
            "transaction": self.categories["transaction"][0],
        }
        return {**values, **changes}

    def test_raw_dataset_load_and_cleaning(self):
        raw = load_properties(DEFAULT_DATA)
        cleaned, summary = clean_properties(raw)
        self.assertGreater(len(raw), 100_000)
        self.assertEqual(len(cleaned), summary["clean_rows"])
        self.assertGreater(len(cleaned), 60_000)
        self.assertEqual(cleaned.city.nunique(), 81)
        self.assertTrue(cleaned.price_inr.gt(0).all())

    def test_training_split_is_80_20_and_disjoint(self):
        data, x_train, x_test, y_train, y_test = load_split()
        self.assertEqual(len(x_train) + len(x_test), len(data))
        self.assertEqual(len(x_test), math.ceil(len(data) * .2))
        self.assertTrue(set(x_train.index).isdisjoint(x_test.index))
        self.assertEqual(len(y_train), len(x_train))
        self.assertEqual(len(y_test), len(x_test))

    def test_saved_model_predicts_two_supported_profiles(self):
        examples = [
            self.sample(area_sqft=750, bedrooms=1),
            self.sample(city=self.categories["city"][-1], area_sqft=2_000, bedrooms=4),
        ]
        estimates = [predict_price(self.model, row) for row in examples]
        self.assertTrue(all(math.isfinite(value) and value > 0 for value in estimates))
        self.assertNotEqual(estimates[0], estimates[1])

    def test_prediction_rejects_invalid_inputs(self):
        cases = [
            self.sample(area_sqft=0),
            self.sample(area_sqft=-25),
            self.sample(bedrooms=-1),
            self.sample(bathrooms=float("nan")),
            self.sample(balconies=float("inf")),
            self.sample(city="unsupported-city"),
        ]
        for values in cases:
            with self.subTest(values=values):
                with self.assertRaises(ValueError):
                    predict_price(self.model, values)
        incomplete = self.sample()
        incomplete.pop("city")
        with self.assertRaisesRegex(ValueError, "required property details"):
            predict_price(self.model, incomplete)

    def test_metadata_schema_is_checked_before_model_load(self):
        with TemporaryDirectory() as folder:
            metadata_path = Path(folder) / "metadata.json"
            metadata_path.write_text(json.dumps({"features": ["wrong"], "target": "price_inr"}), encoding="utf-8")
            with patch("src.predict.METADATA_PATH", metadata_path):
                with self.assertRaisesRegex(ValueError, "feature schema"):
                    load_artifacts()

    def test_evaluation_metrics(self):
        result = metrics(np.array([10, 20, 30]), np.array([12, 18, 30]))
        self.assertEqual(result["mae"], 4 / 3)
        self.assertAlmostEqual(result["rmse"], math.sqrt(8 / 3))
        self.assertAlmostEqual(result["r2"], .96)

    def test_recommendation_filters_real_cleaned_records(self):
        data = __import__("pandas").read_csv(ROOT / "data" / "processed" / "cleaned_properties.csv")
        profiles = find_profiles(data, "All cities", 10_000_000, 900, 3)
        self.assertFalse(profiles.empty)
        self.assertTrue(profiles.median_price_inr.le(10_000_000).all())

    def test_app_load_path_never_trains_or_changes_artifact(self):
        artifact = ROOT / "models" / "property_price_model.pkl"
        before = hashlib.sha256(artifact.read_bytes()).hexdigest()
        app_source = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn("return load_artifacts()", app_source)
        self.assertNotIn("from src.train", app_source)
        self.assertNotIn("train()", app_source)
        load_artifacts()
        after = hashlib.sha256(artifact.read_bytes()).hexdigest()
        self.assertEqual(before, after, "App startup changed the trained model artifact.")


if __name__ == "__main__":
    unittest.main()
