import pandas as pd


def load_data(file):
    """
    Load a CSV file into a DataFrame.
    """
    return pd.read_csv(file)


def clean_data(df):
    """
    Perform general data cleaning that works for most datasets.
    """

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows where every value is missing
    df = df.dropna(how="all")

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Remove leading/trailing spaces from string values
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Convert object columns to numeric when possible
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # Reset index
    df.reset_index(drop=True, inplace=True)

    return df


def dataset_summary(df):
    """
    Return useful dataset statistics.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicates": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
        "column_names": list(df.columns)
    }


def missing_value_summary(df):
    """
    Return missing values per column.
    """

    return df.isnull().sum()


def numeric_columns(df):
    return df.select_dtypes(include="number").columns.tolist()


def categorical_columns(df):
    return df.select_dtypes(include="object").columns.tolist()