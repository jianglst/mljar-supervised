import unittest
import tempfile
import json
import numpy as np
import pandas as pd

from numpy.testing import assert_almost_equal
from sklearn import datasets
from supervised.automl import AutoML
from supervised.metric import Metric


class AutoMLTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X, cls.y = datasets.make_classification(
            n_samples=200,
            n_features=5,
            n_informative=5,
            n_redundant=0,
            n_classes=2,
            n_clusters_per_class=1,
            n_repeated=0,
            shuffle=False,
            random_state=0,
        )
        cls.X = pd.DataFrame(cls.X, columns=["f0", "f1", "f2", "f3", "f4"])
        #cls.y = pd.DataFrame(cls.y)

    def test_fit_and_predict(self):
        metric = Metric({"name": "logloss"})

        automl = AutoML(total_time_limit=10, algorithms=["Xgboost"],
                        start_random_models=5,
                        hill_climbing_steps=0)
        automl.fit(self.X, self.y)

        y_predicted = automl.predict(self.X)
        self.assertTrue(y_predicted is not None)
        loss = metric(self.y, y_predicted)
        self.assertTrue(loss < 0.5)

        params = automl.to_json()
        automl2 = AutoML()
        automl2.from_json(params)

        y_predicted2 = automl2.predict(self.X)
        self.assertTrue(y_predicted2 is not None)
        loss2 = metric(self.y, y_predicted2)
        self.assertTrue(loss2 < 0.5)


if __name__ == "__main__":
    unittest.main()
