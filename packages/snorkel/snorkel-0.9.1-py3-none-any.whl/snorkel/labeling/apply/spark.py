from typing import Tuple

import numpy as np
from pyspark import RDD

from snorkel.types import DataPoint

from .core import BaseLFApplier, RowData, apply_lfs_to_data_point


class SparkLFApplier(BaseLFApplier):
    r"""LF applier for a Spark RDD.

    Data points are stored as ``Row``\s in an RDD, and a Spark
    ``map`` job is submitted to execute the LFs. A common
    way to obtain an RDD is via a PySpark DataFrame. For an
    example usage with AWS EMR instructions, see
    ``test/labeling/apply/lf_applier_spark_test_script.py``.
    """

    def apply(self, data_points: RDD) -> np.ndarray:
        """Label PySpark RDD of data points with LFs.

        Parameters
        ----------
        data_points
            PySpark RDD containing data points to be labeled by LFs

        Returns
        -------
        np.ndarray
            Matrix of labels emitted by LFs
        """

        def map_fn(args: Tuple[DataPoint, int]) -> RowData:
            return apply_lfs_to_data_point(*args, lfs=self._lfs)

        labels = data_points.zipWithIndex().map(map_fn).collect()
        return self._numpy_from_row_data(labels)
