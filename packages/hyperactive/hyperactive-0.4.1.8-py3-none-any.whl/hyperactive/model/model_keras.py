# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np
from sklearn.model_selection import KFold
from importlib import import_module
from sklearn.model_selection import train_test_split


from .metrics import dl_scores, dl_losses
from .model import DeepLearningModel


class KerasModel(DeepLearningModel):
    def __init__(self, _config_):
        super().__init__(_config_)
        self.search_config = _config_.search_config

        self.scores = dl_scores
        self.losses = dl_losses
        # if no metric was passed
        # if isinstance(self.metric, str):
        #     self.metric_keras = [self.metric]

        self.layerStr_2_kerasLayer_dict = self._layer_dict(_config_.search_config)
        # self.n_layer = len(self.layerStr_2_kerasLayer_dict.keys())

        self._get_search_config_onlyLayers()

    def _get_search_config_onlyLayers(self):
        self.search_config_onlyLayers = dict(self.search_config)

        del self.search_config_onlyLayers["keras.compile.0"]
        del self.search_config_onlyLayers["keras.fit.0"]

        # elif list(self.search_config.keys())[0] == "keras.fit.0":
        #     del self.search_config_onlyLayers["keras.fit.0"]

    def _layer_dict(self, search_config):
        layerStr_2_kerasLayer_dict = {}

        for layer_key in search_config.keys():
            layer_str, nr = layer_key.rsplit(".", 1)

            # nr=0 are compile and fit _get_fit_parameter
            if nr != "0":
                layer = self._get_model(layer_str)
                layerStr_2_kerasLayer_dict[layer_key] = layer

        return layerStr_2_kerasLayer_dict

    def trafo_hyperpara_dict_lists(self, keras_para_dict):
        layers_para_dict = {}

        for layer_str_1 in list(self.search_config.keys()):

            layer_para_dict = {}
            for layer_key in keras_para_dict.keys():
                layer_str_2, para = layer_key.rsplit(".", 1)

                if layer_str_1 == layer_str_2:
                    layer_para_dict[para] = [keras_para_dict[layer_key]]

            layers_para_dict[layer_str_1] = layer_para_dict

        return layers_para_dict

    def _trafo_hyperpara_dict(self, keras_para_dict):
        layers_para_dict = {}

        for layer_str_1 in list(self.search_config.keys()):

            layer_para_dict = {}
            for layer_key in keras_para_dict.keys():
                layer_str_2, para = layer_key.rsplit(".", 1)

                if layer_str_1 == layer_str_2:
                    layer_para_dict[para] = keras_para_dict[layer_key]

            layers_para_dict[layer_str_1] = layer_para_dict

        return layers_para_dict

    def _create_model(self, layers_para_dict):

        from keras.models import Sequential

        model = Sequential()

        for layer_key in self.layerStr_2_kerasLayer_dict.keys():
            layer = self.layerStr_2_kerasLayer_dict[layer_key]

            model.add(layer(**layers_para_dict[layer_key]))

        return model

    def _get_compile_parameter(self, layers_para_dict):
        compile_para_dict = layers_para_dict[list(layers_para_dict.keys())[0]]

        compile_para_dict["metrics"] = [self.metric]

        return compile_para_dict

    def _get_fit_parameter(self, layers_para_dict):
        fit_para_dict = layers_para_dict[list(layers_para_dict.keys())[1]]

        return fit_para_dict

    def _cross_val_keras(self, model, X, y, fit_para_dict):
        scores = []

        kf = KFold(n_splits=self.cv, shuffle=True)
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]

            fit_para_dict["x"] = X_train
            fit_para_dict["y"] = y_train
            model.fit(**fit_para_dict)
            # y_pred = model.predict(X_test)
            # score = self.metric_class(y_test, y_pred)
            loss, score = model.evaluate(X_test, y_test, verbose=0)
            scores.append(score)

        return np.array(scores).mean()

    def train_model(self, keras_para_dict, X, y):
        layers_para_dict = self._trafo_hyperpara_dict(keras_para_dict)
        model = self._create_model(layers_para_dict)

        compile_para_dict = self._get_compile_parameter(layers_para_dict)
        fit_para_dict = self._get_fit_parameter(layers_para_dict)

        del layers_para_dict["keras.compile.0"]
        del layers_para_dict["keras.fit.0"]

        model.compile(**compile_para_dict)

        if self.cv > 1:
            score = self._cross_val_keras(model, X, y, fit_para_dict)
        elif self.cv < 1:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, train_size=self.cv
            )

            fit_para_dict["x"] = X_train
            fit_para_dict["y"] = y_train
            model.fit(**fit_para_dict)
            # y_pred = model.predict(X_test)
            # score = self.metric_class(y_test, y_pred)
            loss, score = model.evaluate(X_test, y_test, verbose=0)
        else:
            score = 0
            model.fit(X, y)

        if self.metric in self.scores:
            return score, model
        elif self.metric in self.losses:
            return -score, model
