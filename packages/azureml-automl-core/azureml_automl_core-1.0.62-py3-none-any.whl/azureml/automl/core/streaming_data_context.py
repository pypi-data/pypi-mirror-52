# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Holding the streaming data context classes."""
from typing import Any, Optional, Dict
import logging
import numpy as np
import os

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
import azureml.dataprep as dprep
from .data_context import BaseDataContext


class StreamingTransformedDataContext(BaseDataContext):
    """
    The user provided data with applied transformations.

    If there is no preprocessing this will be the same as the RawDataContext.
    This class will also hold the necessary transformers used for Streaming.
    """
    def __init__(self,
                 training_data: dprep.Dataflow,
                 label_column_name: str,
                 weight_column_name: Optional[str] = None,
                 validation_data: Optional[dprep.Dataflow] = None,
                 x_raw_column_names: np.ndarray = None,
                 logger: Any = logging.getLogger(__name__)):
        """
        Construct the StreamingTransformedDataContext class.

        :param training_data: Input training data.
        :type training_data: Dataflow or pandas.DataFrame
        :param label_column_name: Target column name.
        :type label_column_name: string
        :param weight_column_name: Weight column name.
        :type weight_column_name: string
        :param validation_data: Validation data.
        :type validation_data: Dataflow or pandas.DataFrame
        :params x_raw_column_names: raw feature names of X data.
        :type x_raw_column_names: numpy.ndarray
        :param logger: module logger
        :type logger: logger
        """
        X = training_data.drop_columns([label_column_name, weight_column_name])
        y = training_data.keep_columns(label_column_name)
        if weight_column_name is not None:
            sample_weight = training_data.keep_columns(weight_column_name)
        else:
            sample_weight = None

        if validation_data is not None:
            X_valid = validation_data.drop_columns([label_column_name, weight_column_name])
            y_valid = validation_data.keep_columns(label_column_name)
            if weight_column_name is not None:
                sample_weight_valid = validation_data.keep_columns(weight_column_name)
            else:
                sample_weight_valid = None

        super().__init__(X=X, y=y,
                         X_valid=X_valid,
                         y_valid=y_valid,
                         sample_weight=sample_weight,
                         sample_weight_valid=sample_weight_valid,
                         x_raw_column_names=x_raw_column_names,
                         training_data=training_data,
                         label_column_name=label_column_name,
                         weight_column_name=weight_column_name,
                         validation_data=validation_data)

        self.module_logger = logger
        if self.module_logger is None:
            self.module_logger = logging.getLogger(__name__)
            self.module_logger.propagate = False

        self._num_workers = os.cpu_count()
        self.transformers = {}  # type: Dict[str, Any]

    def _get_engineered_feature_names(self):
        """Get the enigneered feature names available in different transformer."""
        return self.x_raw_column_names

    def _clear_cache(self) -> None:
        """Clear the in-memory cached data to lower the memory consumption."""
        self.X = None
        self.y = None
        self.X_valid = None
        self.y_valid = None
        self.sample_weight = None
        self.sample_weight_valid = None
        self.x_raw_column_names = None
        self.transformers = {}
        self.dataset = None
        self.dataset_valid = None
