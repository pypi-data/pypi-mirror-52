# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Dataset that supports streaming."""
from contextlib import contextmanager
from random import randint
from typing import Iterator, Optional

import azureml.dataprep as dprep
import numpy as np

from . import constants
from .dataflow_utilities import PickleableDataflow
from .datasets import DatasetBase
from .exceptions import DataException
from .problem_info import ProblemInfo


class StreamingDataset(DatasetBase):
    """Dataset that supports streaming data (data that may be too large to fit into memory)."""

    CLASS_LABELS_DONT_EXIST_ERROR = "Class labels only exist for classification datasets."
    MAX_ROWS_TO_SUBSAMPLE = 100000

    def __init__(self,
                 task: str,
                 training_data: dprep.Dataflow,
                 label_column_name: str,
                 weight_column_name: Optional[str] = None,
                 validation_data: Optional[dprep.Dataflow] = None):
        """
        Initialize a StreamingDataset.

        :param X: train data
        :param y: label
        :param weight: sample weights
        :param X_valid: validation data
        :param y_valid: validation label
        :param weight_valid: validation sample weights
        """
        self.training_data = training_data
        self.label_column_name = label_column_name
        self.weight_column_name = weight_column_name
        self.validation_data = validation_data

        self.task = task
        self.training_type = constants.TrainingType.TrainAndValidation
        if self.task == constants.Tasks.CLASSIFICATION:
            # this logic assumes that first MAX_ROWS_TO_SUBSAMPLE labels in train and test contain all labels.
            # note that this assumption MAY NOT ALWAYS HOLD TRUE. (for instance, a large dataset sorted by
            # label would invalidate this assumption.) if needed, a full set of labels could possibly be
            # extracted from the Dataflow's profile or the fit Nimbus pipeline
            self.train_class_labels = np.unique(self.get_y().head(StreamingDataset.MAX_ROWS_TO_SUBSAMPLE))
            valid_class_labels = np.unique(self.get_y_valid().head(StreamingDataset.MAX_ROWS_TO_SUBSAMPLE))
            self.class_labels = np.unique(np.concatenate((self.train_class_labels, valid_class_labels)))

    def _get_raw_data_snapshot_str(self):
        """Set the data snapshot for the raw data."""
        raise NotImplementedError

    def get_X(self) -> dprep.Dataflow:
        """Get the feature columns of the training dataset."""
        return self.training_data.drop_columns([self.label_column_name, self.weight_column_name])

    def get_y(self) -> dprep.Dataflow:
        """Get the label column of the training dataset."""
        return self.training_data.keep_columns([self.label_column_name])

    def get_weight(self) -> dprep.Dataflow:
        """Get the weight column of the training dataset."""
        return self.training_data.keep_columns([self.weight_column_name]) \
            if self.weight_column_name is not None else None

    def get_X_valid(self) -> dprep.Dataflow:
        """Get the feature columns of the validation dataset."""
        return self.validation_data.drop_columns([self.label_column_name, self.weight_column_name]) \
            if self.validation_data is not None else None

    def get_y_valid(self) -> dprep.Dataflow:
        """Get the label column of the validation dataset."""
        return self.validation_data.keep_columns([self.label_column_name]) \
            if self.validation_data is not None else None

    def get_weight_valid(self) -> dprep.Dataflow:
        """Get the weight column of the validation dataset."""
        return self.validation_data.keep_columns([self.weight_column_name]) \
            if self.validation_data is not None and self.weight_column_name is not None else None

    def get_class_labels(self) -> dprep.Dataflow:
        """Get the class labels for a classification task."""
        if self.task != constants.Tasks.CLASSIFICATION:
            raise DataException(StreamingDataset.CLASS_LABELS_DONT_EXIST_ERROR)
        return self.class_labels

    def get_is_sparse(self):
        """Dataset that supports streaming data (data that may be too large to fit into memory)."""
        return False

    def get_num_classes(self):
        """
        Get the number of classes in the dataset.

        :return:  number of classes
        """
        if self.task != constants.Tasks.CLASSIFICATION:
            raise DataException(StreamingDataset.CLASS_LABELS_DONT_EXIST_ERROR)
        return len(self.class_labels)

    def get_problem_info(self):
        """
        Get the ProblemInfo for the dataset.

        :return: _ProblemInfo
        """
        return ProblemInfo(is_sparse=False,
                           feature_column_names=self.get_X().head(1).columns.tolist(),
                           label_column_name=self.label_column_name,
                           use_incremental_learning=True)

    def get_subsampled_dataset(self, training_percent, random_state=None):
        """Get subsampled dataset."""
        # if random state is None, set it to an arbitrary fixed value. this ensures that
        # rows are consistent across sampled X, y, and weight Dataflow
        if random_state is None:
            random_state = randint(1, 1000)

        subsample_frac = training_percent / 100

        # subsample original data
        training_data = self.training_data.take_sample(subsample_frac, random_state)
        return StreamingDataset(
            self.task,
            training_data,
            self.label_column_name,
            self.weight_column_name,
            self.validation_data)

    def get_train_class_labels(self):
        """Get the class labels from training data for a classification task."""
        if self.task != constants.Tasks.CLASSIFICATION:
            raise DataException(StreamingDataset.CLASS_LABELS_DONT_EXIST_ERROR)
        return self.train_class_labels

    def get_train_set(self):
        """Get the training part of the dataset."""
        return self.get_X(), self.get_y(), self.get_weight()

    def get_training_type(self):
        """
        Get training type.

        :return: str: training type
        """
        return constants.TrainingType.TrainAndValidation

    def get_transformers(self):
        """
        Get the transformers.

        :return: dict of transformers if success, else none
        """
        return {}

    def get_raw_data_type(self):
        """Return the raw data type."""
        raise NotImplementedError

    def get_valid_set(self):
        """Get the validation part of the dataset."""
        return self.get_X_valid(), self.get_y_valid(), self.get_weight_valid()

    def get_y_transformer(self):
        """Get the y_transformer."""
        return None

    def has_test_set(self):
        """Return true if the given dataset has test set available."""
        return False

    def get_num_auto_cv_splits(self) -> Optional[int]:
        """Return the number of auto CV splits that are to be used for this dataset."""
        # No CV for streaming scenarios yet
        return None

    @contextmanager
    def open_dataset(self) -> Iterator[None]:
        """
        Load the dataset from the cache and then clean it up automatically (if cached).

        Note that any changes made to the dataset won't be reflected back. This is only intended for
        reading the underlying dataset, and caching it back to reduce memory consumption.
        Usage:
            with client_datasets.open_dataset():
                do_something_with_dataset()
        """
        yield

    def __getstate__(self):
        """Get a dictionary representing the object's current state (used for pickling)."""
        state = self.__dict__.copy()
        for key, value in state.items():
            if isinstance(value, dprep.Dataflow):
                state[key] = PickleableDataflow(value)
        return state

    def __setstate__(self, newstate):
        """Set the object's state based on a state dictionary (used for unpickling)."""
        for key, value in newstate.items():
            if isinstance(value, PickleableDataflow):
                newstate[key] = value.get_dataflow()
        self.__dict__.update(newstate)
