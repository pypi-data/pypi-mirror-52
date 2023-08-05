# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import pickle
import multiprocessing

from importlib import import_module
from functools import partial

from .base_positioner import BasePositioner
from .config import Config
from .opt_args import Arguments
from .sub_packages import MetaLearn
from .util import initialize_search, finish_search_, sort_for_best


class BaseOptimizer:
    def __init__(self, *args, **kwargs):

        """

        Parameters
        ----------

        search_config: dict
            A dictionary providing the model and hyperparameter search space for the
            optimization process.
        n_iter: int
            The number of iterations the optimizer performs.
        metric: string, optional (default: "accuracy")
            The metric the model is evaluated by.
        n_jobs: int, optional (default: 1)
            The number of searches to run in parallel.
        cv: int, optional (default: 5)
            The number of folds for the cross validation.
        verbosity: int, optional (default: 1)
            Verbosity level. 1 prints out warm_start points and their scores.
        random_state: int, optional (default: None)
            Sets the random seed.
        warm_start: dict, optional (default: False)
            Dictionary that definies a start point for the optimizer.
        memory: bool, optional (default: True)
            A memory, that saves the evaluation during the optimization to save time when
            optimizer returns to position.
        scatter_init: int, optional (default: False)
            Defines the number n of random positions that should be evaluated with 1/n the
            training data, to find a better initial position.

        Returns
        -------
        None

        """

        self._config_ = Config(*args, **kwargs)
        self._arg_ = Arguments(**kwargs)

        if self._config_.meta_learn:
            self._meta_ = MetaLearn(self._config_.search_config)

        self.search_config = self._config_.search_config
        self.n_iter = self._config_.n_iter

        if self._config_.get_search_path:
            self.pos_list = []
            self.score_list = []

    def _hill_climb_iteration(self, _cand_, _p_, X, y):
        _p_.pos_new = _p_.move_climb(_cand_, _p_.pos_current)
        _p_.score_new = _cand_.eval_pos(_p_.pos_new, X, y)

        if _p_.score_new > _cand_.score_best:
            _cand_, _p_ = self._update_pos(_cand_, _p_)

        return _cand_, _p_

    def _init_base_positioner(self, _cand_, positioner=None, pos_para={}):
        if positioner:
            _p_ = positioner(**pos_para)
        else:
            _p_ = BasePositioner(**pos_para)

        _p_.pos_current = _cand_.pos_best
        _p_.score_current = _cand_.score_best

        return _p_

    def _update_pos(self, _cand_, _p_):
        _cand_.pos_best = _p_.pos_new
        _cand_.score_best = _p_.score_new

        _p_.pos_current = _p_.pos_new
        _p_.score_current = _p_.score_new

        return _cand_, _p_

    def search(self, nth_process, X, y):
        self._config_, _cand_ = initialize_search(self._config_, nth_process, X, y)
        _p_ = self._init_opt_positioner(_cand_, X, y)

        for i in range(self._config_.n_iter):
            _cand_ = self._iterate(i, _cand_, _p_, X, y)
            self._config_.update_p_bar(1)

            if self._config_.get_search_path:
                if isinstance(_p_, list):
                    for p in _p_:
                        self.pos_list.append(p.pos_new)
                        self.score_list.append(p.score_new)
                else:
                    self.pos_list.append(_p_.pos_new)
                    self.score_list.append(_p_.score_new)

        _cand_ = finish_search_(self._config_, _cand_, X, y)

        return _cand_, _p_

    def _search_multiprocessing(self, X, y):
        """Wrapper for the parallel search. Passes integer that corresponds to process number"""
        pool = multiprocessing.Pool(self._config_.n_jobs)
        search = partial(self.search, X=X, y=y)

        _cand_list, _p_list = pool.map(search, self._config_._n_process_range)

        return _cand_list

    def _run_one_job(self, X, y):
        _cand_, _p_ = self.search(0, X, y)
        if self._config_.meta_learn:
            self._meta_.collect(X, y, _cand_list=[_cand_])

        self.model_best = _cand_.model
        self.score_best = _cand_.score_best
        start_point = _cand_._get_warm_start()

        if self._config_.verbosity:
            print("\n", self._config_.metric, self.score_best)
            print("start_point =", start_point)

        if self._config_.get_search_path:
            self._p_ = _p_

    def _run_multiple_jobs(self, X, y):
        _cand_list = self._search_multiprocessing(X, y)

        start_point_list = []
        score_best_list = []
        model_best_list = []
        for _cand_ in _cand_list:
            model_best = _cand_.model
            score_best = _cand_.score_best
            start_point = _cand_._get_warm_start()

            start_point_list.append(start_point)
            score_best_list.append(score_best)
            model_best_list.append(model_best)

        start_point_sorted, score_best_sorted = sort_for_best(
            start_point_list, score_best_list
        )

        model_best_sorted, score_best_sorted = sort_for_best(
            model_best_list, score_best_list
        )

        if self._config_.verbosity:
            print("\nList of start points (best first):")
            for start_point, score_best in zip(start_point_sorted, score_best_sorted):
                print("\n", self._config_.metric, score_best)
                print("start_point =", start_point)

        self.score_best = score_best_sorted[0]
        self.model_best = model_best_sorted[0]

    def fit(self, X, y):
        """Public method for starting the search with the training data (X, y)

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]

        y : array-like, shape = [n_samples] or [n_samples, n_outputs]

        Returns
        -------
        None
        """
        X, y = self._config_._check_data(X, y)

        if self._config_.model_type == "keras":
            self._config_.n_jobs = 1

        if self._config_.n_jobs == 1:
            self._run_one_job(X, y)

        else:
            self._run_multiple_jobs(X, y)

    def predict(self, X_test):
        """Returns the prediction of X_test after a model was searched by `fit`

        Parameters
        ----------
        X_test : array-like or sparse matrix of shape = [n_samples, n_features]

        Returns
        -------
        (unnamed array) : array-like, shape = [n_samples] or [n_samples, n_outputs]
        """
        return self.model_best.predict(X_test)

    def score(self, X_test, y_true):
        """Returns the score calculated from the prediction of X_test and the true values from y_test

        Parameters
        ----------
        X_test : array-like or sparse matrix of shape = [n_samples, n_features]

        y_true : array-like, shape = [n_samples] or [n_samples, n_outputs]

        Returns
        -------
        (unnamed float) : float
        """
        if self._config_.model_type in ["sklearn", "xgboost", "lightgbm", "catboost"]:
            module = import_module("sklearn.metrics")
            metric_class = getattr(module, self._config_.metric)

            y_pred = self.model_best.predict(X_test)
            return metric_class(y_true, y_pred)
        elif self._config_.model_type in ["keras"]:
            loss, score = self.model_best.evaluate(X_test, y_true, verbose=0)
            return score

        """
        y_pred = self.model_best.predict(X_test)

        metric_type = list(self._config_.metric.keys())[0]
        metric_class = self._config_.metric[metric_type]

        return metric_class(y_true, y_pred)
        """

    def export(self, filename):
        """Exports the best model, that was found by the optimizer during `fit`

        Parameters
        ----------
        filename : string or path

        Returns
        -------
        None
        """
        if self.model_best:
            pickle.dump(self.model_best, open(filename, "wb"))
