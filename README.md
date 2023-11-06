# dataframe-memory project


This simple tools aims at providing simple solution to save memory when using pandas' data frame.
It is highly inspired from this [kaggle post](https://www.kaggle.com/gemartin/load-data-reduce-memory-usage).

> [!IMPORTANT]
> The very basic principle : 
>
> - this tool reduces int and float precision without generating duplicates
> - the data types are chosen so that the minimum and maximum values can be re-encoded

### Usage

````python
from data_memory import reduce_memory
import numpy as np
import pandas as pd

df = pd.DataFrame(
    np.array(
        [[1, 2, "aaa"],
         [4, 5, "bbb"],
         [7, 8, "ccc"]] * 10000),
    columns=['a', 'b', 'c'])

reduce_memory(df, verbose=True)
````
Yields the following decrease of memory
````text
Memory usage input: 5.04 MB
Memory usage output: 0.09 MB
Decreased by: 98.28 % 
````
````python
df.info()
````

````text
 #   Column  Non-Null Count  Dtype   
---  ------  --------------  -----   
 0   a       30000 non-null  category
 1   b       30000 non-null  category
 2   c       30000 non-null  category
````

> [!WARNING]
> 1. This tool **destroys** information and **should not be applied automatically** to any dataframe but big ones
> 2. It preserves relative but not absolute information 

