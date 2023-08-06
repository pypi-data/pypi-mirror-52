# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods and classes used during an AutoML experiment to sweep through column purposes."""
from typing import Optional, Type

from azureml.automl.core.constants import FeatureType as _FeatureType


class ColumnPurposeSweeper:
    """Methods and classes used during an AutoML experiment to sweep through column purposes."""

    # Possible safe conversions between types
    _SAFE_COLUMN_TYPE_CONVERSIONS = {_FeatureType.Hashes: _FeatureType.Text}

    @classmethod
    def safe_convert_column_type(cls: Type["ColumnPurposeSweeper"], current_column_purpose: str) -> Optional[str]:
        """
        Provide possible safe type column conversion options.

        :param current_column_purpose: Column purpose of the current column.
        :return: Possible column purposes that are compatible and safe to use.
        """
        return cls._SAFE_COLUMN_TYPE_CONVERSIONS[current_column_purpose] \
            if current_column_purpose in cls._SAFE_COLUMN_TYPE_CONVERSIONS else None
