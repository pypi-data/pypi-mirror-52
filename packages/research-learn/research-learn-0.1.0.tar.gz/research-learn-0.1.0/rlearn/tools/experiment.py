"""
It supports the design and execution of
machine learning experiments.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

from os.path import join
from pickle import dump
from itertools import chain

from tqdm import tqdm
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from ..utils import check_datasets, check_oversamplers_classifiers
from ..model_selection import ModelSearchCV

GROUP_KEYS = ['Dataset', 'Oversampler', 'Classifier', 'params']


def combine_experiments(name, *experiments):
    """Combines the results of multiple experiments into a single one."""

    # Check experiments compatibility
    for attr_name in (
        'datasets_names_',
        'classifiers_names_',
        'scoring_cols_',
        'n_splits',
        'n_runs',
        'random_state',
    ):
        attributes = []
        for experiment in experiments:
            if attr_name != 'scoring_cols_':
                attributes.append(getattr(experiment, attr_name))
            else:
                attributes.append(tuple(getattr(experiment, attr_name)))
        if len(set(attributes)) > 1:
            raise ValueError(
                f'Experiments not compatible. Attribute `{attr_name}` differs.'
            )

    # Combine results
    oversamplers = list(chain(*[experiment.oversamplers for experiment in experiments]))
    combined_experiment = ImbalancedExperiment(
        name,
        experiments[0].datasets,
        oversamplers,
        experiments[0].classifiers,
        experiments[0].scoring,
        experiments[0].n_splits,
        experiments[0].n_runs,
        experiments[0].random_state,
    )
    combined_experiment._initialize(-1, 0)
    combined_experiment.results_ = pd.concat(
        [experiment.results_ for experiment in experiments]
    )

    # Create attributes
    combined_experiment._calculate_optimal_results()._calculate_wide_optimal_results()

    return combined_experiment


class ImbalancedExperiment:
    """Define a classification experiment on multiple imbalanced datasets."""

    def __init__(
        self,
        name,
        datasets,
        oversamplers,
        classifiers,
        scoring,
        n_splits,
        n_runs,
        random_state,
    ):
        self.name = name
        self.datasets = datasets
        self.oversamplers = oversamplers
        self.classifiers = classifiers
        self.scoring = scoring
        self.n_splits = n_splits
        self.n_runs = n_runs
        self.random_state = random_state

    def _initialize(self, n_jobs, verbose):
        """Initialize experiment's parameters."""

        # Check oversamplers and classifiers
        self.estimators_, self.param_grids_ = check_oversamplers_classifiers(
            self.oversamplers, self.classifiers, self.random_state, self.n_runs
        )

        # Scoring columns
        if isinstance(self.scoring, list):
            self.scoring_cols_ = ['mean_test_%s' % scorer for scorer in self.scoring]
        else:
            self.scoring_cols_ = ['mean_test_score']

        # Datasets, oversamplers and classifiers
        self.datasets_names_, _ = zip(*self.datasets)
        self.oversamplers_names_, *_ = zip(*self.oversamplers)
        self.classifiers_names_, *_ = zip(*self.classifiers)

        # Create model search cv
        self.mscv_ = ModelSearchCV(
            self.estimators_,
            self.param_grids_,
            scoring=self.scoring,
            refit=False,
            cv=StratifiedKFold(
                n_splits=self.n_splits, shuffle=True, random_state=self.random_state
            ),
            return_train_score=False,
            n_jobs=n_jobs,
            verbose=verbose,
        )

    def _calculate_results(self, results):
        """"Calculate aggregated results across runs."""
        scoring_mapping = {
            scorer_name: [np.mean, np.std] for scorer_name in self.scoring_cols_
        }
        results['params'] = results['params'].apply(
            lambda param_grid: str(
                {
                    param: val
                    for param, val in param_grid.items()
                    if 'random_state' not in param
                }
            )
        )
        self.results_ = results.groupby(GROUP_KEYS).agg(scoring_mapping)
        return self

    def _calculate_optimal_results(self):
        """"Calculate optimal results across hyperparameters for any
        combination of datasets, overamplers, classifiers and metrics."""

        # Select mean scores
        optimal = self.results_[
            [(score, 'mean') for score in self.scoring_cols_]
        ].reset_index()

        # Flatten columns
        optimal.columns = optimal.columns.get_level_values(0)

        # Calculate maximum score per gorup key
        agg_measures = {score: max for score in self.scoring_cols_}
        optimal = optimal.groupby(GROUP_KEYS[:-1]).agg(agg_measures).reset_index()

        # Format as long table
        optimal = optimal.melt(
            id_vars=GROUP_KEYS[:-1],
            value_vars=self.scoring_cols_,
            var_name='Metric',
            value_name='Score',
        )

        # Cast to categorical columns
        optimal_cols = GROUP_KEYS[:-1] + ['Metric']
        names = [
            self.datasets_names_,
            self.oversamplers_names_,
            self.classifiers_names_,
            self.scoring_cols_,
        ]
        for col, name in zip(optimal_cols, names):
            optimal[col] = pd.Categorical(optimal[col], name)

        # Sort values
        self.optimal_ = optimal.sort_values(optimal_cols).reset_index(drop=True)

        return self

    def _calculate_wide_optimal_results(self):
        """Calculate optimal results in wide format."""

        # Format as wide table
        wide_optimal = self.optimal_.pivot_table(
            index=['Dataset', 'Classifier', 'Metric'],
            columns=['Oversampler'],
            values='Score',
        )
        wide_optimal.columns = wide_optimal.columns.tolist()
        wide_optimal.reset_index(inplace=True)

        # Transform metric column
        if isinstance(self.scoring, list):
            wide_optimal['Metric'] = wide_optimal['Metric'].replace(
                'mean_test_', '', regex=True
            )
        elif isinstance(self.scoring, str):
            wide_optimal['Metric'] = self.scoring
        else:
            wide_optimal['Metric'] = (
                'accuracy'
                if self.mscv_.estimator._estimator_type == 'classifier'
                else 'r2'
            )

        # Cast column
        wide_optimal['Metric'] = pd.Categorical(
            wide_optimal['Metric'],
            categories=self.scoring if isinstance(self.scoring, list) else None,
        )

        self.wide_optimal_ = wide_optimal

        return self

    def run(self, n_jobs=-1, verbose=0):
        """Run experiment."""

        self._initialize(n_jobs, verbose)

        # Define empty results
        results = []

        # Populate results table
        datasets = check_datasets(self.datasets)
        for dataset_name, (X, y) in tqdm(datasets, desc='Datasets'):

            # Fit model search
            self.mscv_.fit(X, y)

            # Get results
            result = pd.DataFrame(self.mscv_.cv_results_).loc[
                :, ['models', 'params'] + self.scoring_cols_
            ]

            # Append dataset name column
            result = result.assign(Dataset=dataset_name)

            # Append result
            results.append(result)

        # Split models
        results = pd.concat(results, ignore_index=True)
        results.loc[:, 'models'] = results.loc[:, 'models'].apply(
            lambda model: model.split('|')
        )
        results[['Oversampler', 'Classifier']] = pd.DataFrame(
            results.models.values.tolist()
        )

        # Drop models columns
        results.drop(columns='models', inplace=True)

        # Calculate results in various formats
        self._calculate_results(
            results
        )._calculate_optimal_results()._calculate_wide_optimal_results()

        return self

    def dump(self, path='.'):
        """Dump the experiment object."""
        with open(join(path, f'{self.name}.pkl'), 'wb') as file:
            dump(self, file)
