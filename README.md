# dataframe-memory project


This simple tools aims at providing simple solution to save memory when using pandas' data frame.
It is highly inspired from this [kaggle post](https://www.kaggle.com/gemartin/load-data-reduce-memory-usage).

> [!IMPORTANT]
> The very basic principle : 
>
> - this tool reduces int and float precision without generating duplicates
> - the data types are chosen so that the minimum and maximum values can be re-encoded

````python
from data_memory import reduce_memory
import numpy as np
import pandas as pd

df = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]] * 100),
                  columns=['a', 'b', 'c'])

reduce_memory(df, verbose=True)
print(df.info())
````
````text
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 300 entries, 0 to 299
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype
---  ------  --------------  -----
 0   a       300 non-null    uint8 <- best data type
 1   b       300 non-null    uint8
 2   c       300 non-null    uint8
dtypes: uint8(3)
memory usage: 1.0 KB
````

> [!WARNING]
> 1. This tool **destroys** information and **should not be applied automatically** to any dataframe but big ones
> 2. It preserves relative but not absolute information 

