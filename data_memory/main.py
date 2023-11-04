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


def memory_usage(data_frame):
    return data_frame.memory_usage(deep=True).sum() / 1024 ** 2


def _reduce_float(data_frame, col):
    subtype_float = ['float16', 'float32', 'float64']
    mx_col = data_frame[col].max()
    mn_col = data_frame[col].min()
    n0 = data_frame[col].unique().__len__()
    for ele in subtype_float:
        c1 = mn_col > np.finfo(ele).min
        c2 = mx_col < np.finfo(ele).max
        n = data_frame[col].astype(ele).unique().__len__()
        c3 = n * 1.1 > n0
        if c1 and c2 and c3:
            data_frame[col] = data_frame[col].astype(ele)
            break


def _reduce_int(data_frame, col):
    subtype_int = ['uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16',
                   'int32', 'int64']
    mx_col = data_frame[col].max()
    mn_col = data_frame[col].min()
    n0 = data_frame[col].unique().__len__()
    for ele in subtype_int:
        c1 = mn_col > np.iinfo(ele).min
        c2 = mx_col < np.iinfo(ele).max
        n = data_frame[col].astype(ele).unique().__len__()
        c3 = n * 1.1 > n0
        if c1 and c2 and c3:
            data_frame[col] = data_frame[col].astype(ele)
            break


def reduce_memory(data_frame, verbose=False, dates=None):
    if dates is None:
        dates = []
    if verbose:
        memory_before = memory_usage(data_frame)
        print('before: {:.2f} MB'.format(memory_before))

    for col in data_frame.columns:
        col_type = str(data_frame[col].dtypes)

        if 'int' in col_type:
            _reduce_int(data_frame, col)

        elif 'float' in col_type:
            _reduce_float(data_frame, col)

        elif 'object' in col_type:
            if col in dates:
                data_frame[col] = pd.to_datetime(data_frame[col],
                                                 format='%Y-%m-%d')
            else:
                numbr_of_unique = len(data_frame[col].unique())
                numbr_total = len(data_frame[col])
                if numbr_of_unique / numbr_total < 0.5:
                    data_frame[col] = data_frame[col].astype('category')
    if verbose:
        memory_after = memory_usage(data_frame)
        print('after:{:.2f} MB'.format(memory_after))
        print('Decreased by: {:.2f} % '.format(
            100 * (memory_before - memory_after) / memory_before))
