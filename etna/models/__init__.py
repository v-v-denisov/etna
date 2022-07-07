from etna import SETTINGS
from etna.models.autoarima import AutoARIMAModel
from etna.models.base import BaseAdapter
from etna.models.base import BaseModel
from etna.models.base import Model
from etna.models.base import PerSegmentModel
from etna.models.catboost import CatBoostModelMultiSegment
from etna.models.catboost import CatBoostModelPerSegment
from etna.models.catboost import CatBoostMultiSegmentModel
from etna.models.catboost import CatBoostPerSegmentModel
from etna.models.holt_winters import HoltModel
from etna.models.holt_winters import HoltWintersModel
from etna.models.holt_winters import SimpleExpSmoothingModel
from etna.models.linear import ElasticMultiSegmentModel
from etna.models.linear import ElasticPerSegmentModel
from etna.models.linear import LinearMultiSegmentModel
from etna.models.linear import LinearPerSegmentModel
from etna.models.moving_average import MovingAverageModel
from etna.models.naive import NaiveModel
from etna.models.sarimax import SARIMAXModel
from etna.models.seasonal_ma import SeasonalMovingAverageModel
from etna.models.sklearn import SklearnMultiSegmentModel
from etna.models.sklearn import SklearnPerSegmentModel
from etna.models.tbats import BATSModel
from etna.models.tbats import TBATSModel

if SETTINGS.prophet_required:
    from etna.models.prophet import ProphetModel
