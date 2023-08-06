"""
@file
@brief Rewrites some of the converters implemented in
:epkg:`sklearn-onnx`.
"""
from skl2onnx.common._registration import _converter_pool
from ..converters64.ada_boost import convert_sklearn_ada_boost_regressor
from ..converters64.tree_converters import (
    convert_sklearn_decision_tree_regressor,
    convert_sklearn_gradient_boosting_regressor,
    convert_sklearn_random_forest_regressor_converter,
)


_overwritten_operators = {
    'SklearnAdaBoostRegressor': convert_sklearn_ada_boost_regressor,
    'SklearnDecisionTreeRegressor': convert_sklearn_decision_tree_regressor,
    'SklearnGradientBoostingRegressor': convert_sklearn_gradient_boosting_regressor,
    'SklearnRandomForestRegressor': convert_sklearn_random_forest_regressor_converter,
    'SklearnExtraTreesRegressor': convert_sklearn_random_forest_regressor_converter,
}


def register_rewritten_operators(new_values=None):
    """
    Registers modified operators and returns the old values.

    @param      new_values      operators to rewrite or None
                                to rewrite default ones
    @return                      old values
    """
    if new_values is None:
        for rew in _overwritten_operators:
            if rew not in _converter_pool:
                raise KeyError(
                    "skl2onnx was not imported and '{}' was not registered.".format(rew))
        old_values = {k: _converter_pool[k] for k in _overwritten_operators}
        _converter_pool.update(_overwritten_operators)
        return old_values
    else:
        for rew in new_values:
            if rew not in _converter_pool:
                raise KeyError(
                    "skl2onnx was not imported and '{}' was not registered.".format(rew))
        old_values = {k: _converter_pool[k] for k in new_values}
        _converter_pool.update(new_values)
        return old_values
