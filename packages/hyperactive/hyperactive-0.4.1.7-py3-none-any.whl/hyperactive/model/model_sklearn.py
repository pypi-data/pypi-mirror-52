# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer


from .model import MachineLearningModel


class ScikitLearnModel(MachineLearningModel):
    def __init__(self, _config_, model_key):
        super().__init__(_config_)
        self.model_key = model_key
        self.model = self._get_model(model_key)

    def _create_model(self, para):
        return self.model(**para)

    def _cross_val_score(self, sklearn_model, X, y):
        scorer = make_scorer(self.metric_class)

        scores = cross_val_score(sklearn_model, X, y, scoring=scorer, cv=self.cv)
        return scores.mean(), sklearn_model
