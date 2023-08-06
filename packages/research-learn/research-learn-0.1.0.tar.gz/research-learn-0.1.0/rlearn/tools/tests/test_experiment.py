"""
Test the imbalanced_analysis module.
"""

from os import remove
from pickle import load

import pytest
import pandas as pd
from sklearn.model_selection import ParameterGrid

from rlearn.tools.tests import DATASETS, OVERSAMPLERS, CLASSIFIERS
from rlearn.tools.experiment import (
    combine_experiments,
    ImbalancedExperiment,
    GROUP_KEYS,
)


def test_combine_experiments():
    """Test the combination of experiments."""
    experiment1 = ImbalancedExperiment(
        'test_experiment1',
        DATASETS,
        OVERSAMPLERS[0:2],
        CLASSIFIERS,
        scoring=None,
        n_splits=3,
        n_runs=3,
        random_state=0,
    ).run()
    experiment2 = ImbalancedExperiment(
        'test_experiment2',
        DATASETS,
        OVERSAMPLERS[2:3],
        CLASSIFIERS,
        scoring=None,
        n_splits=3,
        n_runs=3,
        random_state=0,
    ).run()
    experiment = combine_experiments('test_experiment', experiment1, experiment2)
    assert experiment.name == 'test_experiment'
    assert (
        experiment.datasets_names_
        == experiment1.datasets_names_
        == experiment2.datasets_names_
    )
    assert experiment.oversamplers_names_ == tuple([name for name, *_ in OVERSAMPLERS])
    assert (
        experiment.classifiers_names_
        == experiment1.classifiers_names_
        == experiment2.classifiers_names_
    )
    assert (
        experiment.scoring_cols_
        == experiment1.scoring_cols_
        == experiment2.scoring_cols_
    )
    assert experiment.n_splits == experiment1.n_splits == experiment2.n_splits
    assert experiment.n_runs == experiment1.n_runs == experiment2.n_runs
    assert (
        experiment.random_state == experiment1.random_state == experiment2.random_state
    )
    pd.testing.assert_frame_equal(
        experiment.results_, pd.concat([experiment1.results_, experiment2.results_])
    )


@pytest.mark.parametrize(
    'scoring,n_runs', [(None, 2), ('accuracy', 3), (['accuracy', 'recall'], 2)]
)
def test_experiment_initialization(scoring, n_runs):
    """Test the initialization of experiment's parameters."""
    experiment = ImbalancedExperiment(
        'test_experiment',
        DATASETS,
        OVERSAMPLERS,
        CLASSIFIERS,
        scoring=scoring,
        n_splits=3,
        n_runs=n_runs,
        random_state=0,
    )
    experiment.run()
    if not isinstance(scoring, list):
        assert experiment.scoring_cols_ == ['mean_test_score']
    else:
        assert experiment.scoring_cols_ == [
            'mean_test_%s' % scorer for scorer in scoring
        ]
    assert experiment.datasets_names_ == ('A', 'B', 'C')
    assert experiment.oversamplers_names_ == ('random', 'smote', 'adasyn')
    assert experiment.classifiers_names_ == ('knn', 'dtc')
    assert len(experiment.estimators_) == len(OVERSAMPLERS) * len(CLASSIFIERS)


def test_results():
    """Test the results of experiment."""
    experiment = ImbalancedExperiment(
        'test_experiment',
        DATASETS,
        OVERSAMPLERS,
        CLASSIFIERS,
        scoring=None,
        n_splits=3,
        n_runs=3,
        random_state=0,
    ).run()

    # Results
    assert (
        experiment.results_.reset_index().columns.get_level_values(0).tolist()[:-2]
        == GROUP_KEYS
    )
    assert (
        len(experiment.results_)
        == len(DATASETS)
        * len(ParameterGrid(experiment.param_grids_))
        // experiment.n_runs
    )

    # Optimal results
    assert set(experiment.optimal_.Dataset.unique()) == set(experiment.datasets_names_)
    assert set(experiment.optimal_.Oversampler.unique()) == set(
        experiment.oversamplers_names_
    )
    assert set(experiment.optimal_.Classifier.unique()) == set(
        experiment.classifiers_names_
    )
    assert len(experiment.optimal_) == len(DATASETS) * len(OVERSAMPLERS) * len(
        CLASSIFIERS
    )

    # Wide optimal results
    assert set(experiment.wide_optimal_.Dataset.unique()) == set(
        experiment.datasets_names_
    )
    assert set(experiment.wide_optimal_.Classifier.unique()) == set(
        experiment.classifiers_names_
    )
    assert set(experiment.oversamplers_names_).issubset(
        experiment.wide_optimal_.columns
    )
    assert len(experiment.wide_optimal_) == len(DATASETS) * len(CLASSIFIERS)


def test_dump():
    """Test the dump method."""
    experiment = ImbalancedExperiment(
        'test_experiment',
        DATASETS,
        OVERSAMPLERS,
        CLASSIFIERS,
        scoring=None,
        n_splits=3,
        n_runs=3,
        random_state=0,
    ).run()
    experiment.dump()
    file_name = f'{experiment.name}.pkl'
    with open(file_name, 'rb') as file:
        experiment = load(file)
        attr_names = [
            attr_name for attr_name in vars(experiment).keys() if attr_name[-1] == '_'
        ]
        for attr_name in attr_names:
            attr1, attr2 = (
                getattr(experiment, attr_name),
                getattr(experiment, attr_name),
            )
            if isinstance(attr1, pd.core.frame.DataFrame):
                pd.testing.assert_frame_equal(attr1, attr2)
    remove(file_name)
