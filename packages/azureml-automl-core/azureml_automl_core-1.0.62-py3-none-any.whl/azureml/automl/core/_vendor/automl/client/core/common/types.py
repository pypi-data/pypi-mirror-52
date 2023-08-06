"""Convenience names for long types."""
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

import numpy as np
import pandas as pd
import scipy
from sklearn.base import TransformerMixin

import azureml.dataprep as dprep


T = TypeVar('T')

# Convenience type for general data input
DataInputType = Union[np.ndarray, pd.DataFrame, scipy.sparse.spmatrix, dprep.Dataflow]

# Convenience type for single column data input
DataSingleColumnInputType = Union[np.ndarray, pd.Series, dprep.Dataflow]

# Convenience type for function inputs to DataFrame.apply (either a function or the name of one)
DataFrameApplyFunction = Union['Callable[..., Optional[Any]]', str]

# Convenience type representing transformers
TransformerType = Tuple[Union[str, List[str]], List[TransformerMixin], Dict[str, str]]

# Convenience type for featurization summary
FeaturizationSummaryType = List[Dict[str, Optional[Any]]]

# Convenience type for grains
GrainType = Union[Tuple[str], str]
