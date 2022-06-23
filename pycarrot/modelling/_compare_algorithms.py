from typing import List, Dict, Tuple, Optional

import pandas as pd

from ._train_model import train_model


def _get_available_algos() -> List[str]:
    """
    Returns a list of strings where each string is the
    abbreviation of an algorithm.
    """
    return [
        "lr",
        "dt",
        "extratree",
        "extratrees",
        "rf",
        "ridge",
        "perceptron",
        "passive-aggressive",
        "knn",
        "nb",
        "linearsvc",
        "rbfsvc",
    ]


def compare_algorithms(
    setup: dict,
    include: List[str] = _get_available_algos(),
    sort: Optional[str] = None,
    return_models: bool = False,
) -> Tuple[pd.DataFrame, Dict]:
    """
    Calculates various metrics for different machine learning
    algorithms.

    Parameters
    ----------
    setup : dict stemming from pc.modelling.prepare_data(...)

    include : optional list of strings
        declares what algorithms to compare

    sort : optional str
        defines how compare_df is sorted

    return_models: bool
        Flag for returning model instances trained on the
        entire training set. By default set to false to
        save on computational time.

    Returns
    -------
    compare_df : pd.DataFrame
        sorted overview of algorithm performance

    model_dict : dict
        keys: algorithms string abbreviation
        values: trained model instance
    """
    # Checking inputs
    _check_include(include)
    _check_sort(sort)

    # Preparing empty compare_df and model_dict
    # with populating occuring later
    compare_df = _prepare_compare_df()
    model_dict = {}

    # Training models
    for algorithm in include:
        model, metrics = train_model(
            algorithm,
            setup,
            return_models,
        )
        compare_df = pd.concat([compare_df, metrics])
        model_dict[algorithm] = model

    # Sort compare_df
    if sort:
        compare_df = compare_df.sort_values(
            by=[sort, "Fit time (s)"],
            ascending=[False, True],
        ).reset_index(drop=True)

    return compare_df, model_dict


def _prepare_compare_df() -> pd.DataFrame:
    """
    Creates compare_df dataframe with required columns,
    but no entries yet.

    Returns
    -------
    compare_df : pd.DataFrame
    """
    return pd.DataFrame(
        columns=[
            "algorithm",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "Fit time (s)",
        ]
    )


def _check_include(include: List[str]):
    available_algos = _get_available_algos()
    for entry in include:
        if entry not in available_algos:
            raise LookupError(
                f"'{entry}' was provided in the include parameter, but is not among the avaiable algorithms."
            )


def _check_sort(sort: Optional[str]):
    if sort not in [
        None,
        "algorithm",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]:
        raise LookupError(
            f"'{sort}' was provided as sort parameter, but is not among the avaiable metrics."
        )
