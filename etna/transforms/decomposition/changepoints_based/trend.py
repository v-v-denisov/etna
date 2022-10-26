from typing import List
from typing import Optional

import pandas as pd

from etna.transforms.base import FutureMixin
from etna.transforms.base import ReversiblePerSegmentWrapper
from etna.transforms.decomposition.changepoints_based.base import ChangePointsTransform
from etna.transforms.decomposition.changepoints_based.change_points_models import BaseChangePointsModelAdapter
from etna.transforms.decomposition.changepoints_based.detrend import _OneSegmentChangePointsTrendTransform
from etna.transforms.decomposition.changepoints_based.per_interval_models import PerIntervalModel
from etna.transforms.decomposition.changepoints_based.per_interval_models import SklearnPerIntervalModel


class _OneSegmentTrendTransform(_OneSegmentChangePointsTrendTransform):
    """_OneSegmentTrendTransform adds trend as a feature."""

    def __init__(
        self,
        in_column: str,
        out_column: str,
        change_point_model: BaseChangePointsModelAdapter,
        per_interval_model: PerIntervalModel,
    ):
        """Init _OneSegmentTrendTransform.

        Parameters
        ----------
        in_column:
            name of column to apply transform to
        out_column:
            name of added column
        change_point_model:
            model to get trend change points
        per_interval_model:
            model to get trend from data
        """
        self.out_column = out_column
        super().__init__(
            in_column=in_column,
            change_point_model=change_point_model,
            per_interval_model=per_interval_model,
        )

    def _apply_transformation(self, df: pd.DataFrame, transformed_series: pd.Series) -> pd.DataFrame:
        df.loc[:, self.out_column] = transformed_series
        return df

    def _apply_inverse_transformation(self, df: pd.DataFrame, transformed_series: pd.Series) -> pd.DataFrame:
        return df


class TrendTransform(ChangePointsTransform, ReversiblePerSegmentWrapper, FutureMixin):
    """TrendTransform adds trend as a feature.

    TrendTransform uses uses :py:class:`ruptures.detection.Binseg` model as a change point detection model
    in _TrendTransform.

    Warning
    -------
    This transform can suffer from look-ahead bias. For transforming data at some timestamp
    it uses information from the whole train part.
    """

    def __init__(
        self,
        in_column: str,
        change_points_model: BaseChangePointsModelAdapter,
        per_interval_model: Optional[PerIntervalModel] = None,
        out_column: Optional[str] = None,
    ):
        """Init TrendTransform.

        Parameters
        ----------
        in_column:
            name of column to apply transform to
        out_column:
            name of added column.
            If not given, use ``self.__repr__()``
        """
        self.in_column = in_column
        self.out_column = out_column
        self.per_interval_model = SklearnPerIntervalModel() if per_interval_model is None else per_interval_model
        self.change_points_model = change_points_model
        super().__init__(
            transform=_OneSegmentTrendTransform(
                in_column=in_column,
                out_column=self.out_column if self.out_column is not None else f"{self.__repr__()}",
                change_point_model=self.change_points_model,
                per_interval_model=self.per_interval_model,
            ),
            required_features=[in_column],
        )

    def get_regressors_info(self) -> List[str]:
        return [self.out_column]
