import pandas as pd
import pytest

from data_memory import reduce_memory, memory_usage


# Test case for the provided example
def test_reduce_memory_example():
    # Create a sample DataFrame
    data = {'A': [1, 2, 3], 'B': [1.1, 2.2, 3.3], 'C': ['foo', 'bar', 'baz']}
    df = pd.DataFrame(data)
    mem = memory_usage(df)
    # Ensure the function runs without errors
    reduce_memory(df, verbose=True, method="exact")
    print(df.dtypes)
    # Add assertions here based on the expected behavior of your function
    # For example, you can check if the memory usage has decreased as expected
    # You might need to adjust these assertions based on your specific use case
    assert mem > memory_usage(df)


def test_reduce_memory_invalid_method():
    with pytest.raises(ValueError, match="wrong argument specification"):
        df = pd.DataFrame()
        reduce_memory(df, method="invalid_method")


def test_reduce_memory_with_dates():
    # Create a sample DataFrame with a date column
    data = {'A': [1, 2, 3], 'B': [1.1, 2.2, 3.3],
            'Date': ['2022-01-01', '2022-02-01', '2022-03-01']}
    df = pd.DataFrame(data)
    initial_memory_usage = memory_usage(df)
    reduce_memory(df, verbose=True, dates=['Date'])
    assert pd.api.types.is_datetime64_any_dtype(df['Date'])
    assert memory_usage(df) < initial_memory_usage
