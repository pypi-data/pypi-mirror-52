# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

from .model_sklearn import ScikitLearnModel


class XGBoostModel(ScikitLearnModel):
    def __init__(self, _config_, model_key):
        super().__init__(_config_, model_key)
