# Copyright 2023 Eurobios
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.#

import numpy as np
import pandas as pd

INT_DATATYPE = ['uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16',
                'int32', 'int64']

FLOAT_DATATYPE = ['float16', 'float32', 'float64']


def memory_usage(df: pd.DataFrame):
    return df.memory_usage(deep=True).sum() / 1024 ** 2


def _reduce_float(df: pd.DataFrame, column, method):
    max_column = df[column].max()
    min_column = df[column].min()
    n0 = df[column].unique().__len__()
    for dtype in FLOAT_DATATYPE:
        c1 = min_column > np.finfo(dtype).min
        c2 = max_column < np.finfo(dtype).max
        if method == "approx":
            n = df[column].astype(dtype).unique().__len__()
            c3 = n * 1.01 > n0
            if c1 and c2 and c3:
                df[column] = df[column].astype(dtype)
                break

        elif method == "exact":
            if all(np.array(df[column] == df[column].astype(dtype))):
                df[column] = df[column].astype(dtype)
                break


def _reduce_int(df: pd.DataFrame, column, method):
    max_column = df[column].max()
    min_column = df[column].min()
    n0 = df[column].unique().__len__()
    for dtype in INT_DATATYPE:
        c1 = min_column > np.iinfo(dtype).min
        c2 = max_column < np.iinfo(dtype).max
        if method == "approx":
            n = df[column].astype(dtype).unique().__len__()
            c3 = n * 1.01 > n0
            if c1 and c2 and c3:
                df[column] = df[column].astype(dtype)
                break
        elif method == "exact":
            if all(np.array(df[column] == df[column].astype(dtype))):
                df[column] = df[column].astype(dtype)
                break


def reduce_memory(df: pd.DataFrame, verbose=False, dates=None,
                  method="approx"):
    """
    Reduce the memory usage of a Pandas DataFrame by optimizing the data types
    of its columns.

    Parameters:
    - df (pd.DataFrame): The input DataFrame to be memory-optimized.
    - verbose (bool, optional): If True, print memory usage information before
     and after optimization. Default is False.
    - dates (list, optional): List of column names to be treated as date columns.
     Default is None.
    - method (str, optional): The method used for optimization. Options are
     "approx" (default) or "exact". "approx" performs approximate memory
      reduction, while "exact" ensures exact reduction.

    Raises:
    - ValueError: If the specified method is not in ["approx", "exact"].

    Returns:
    None: The function modifies the input DataFrame in place.

    Example:
    ```python
    import pandas as pd

    # Create a sample DataFrame
    data = {'A': [1, 2, 3], 'B': [1.1, 2.2, 3.3], 'C': ['foo', 'bar', 'baz']}
    df = pd.DataFrame(data)

    # Reduce memory usage
    reduce_memory(df, verbose=True)
    ```
    """
    if method not in ["approx", "exact"]:
        raise ValueError("wrong argument specification")
    memory_before = 0
    if dates is None:
        dates = []
    if verbose:
        memory_before = memory_usage(df)
        print('Memory usage input: {:.2f} MB'.format(memory_before))
    n = len(df)
    for column in df.columns:
        column_type = str(df[column].dtypes)

        if 'int' in column_type:
            _reduce_int(df, column, method)

        elif 'float' in column_type:
            _reduce_float(df, column, method)

        elif 'object' in column_type:
            if column in dates:
                df[column] = pd.to_datetime(df[column],
                                            format='%Y-%m-%d')
            else:
                nb_unique = len(df[column].unique())
                if nb_unique / n < 0.5:
                    df[column] = df[column].astype('category')
    if verbose:
        memory_after = memory_usage(df)
        print('Memory usage output: {:.2f} MB'.format(memory_after))
        print('Decreased by: {:.2f} % '.format(
            100 * (memory_before - memory_after) / memory_before))
