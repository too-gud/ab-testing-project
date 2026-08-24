from src.database import run_query

import pandas as pd

def get_numeric_columns(table):

    df = run_query(f'SELECT * FROM "{table}" LIMIT 100')

    return list(df.select_dtypes(include="number").columns)
# ------------------------------------
# Get Column Names
# ------------------------------------

def get_columns(table_name):

    query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position;
    """

    df = run_query(query)

    return df["column_name"].tolist()

def get_tables():

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    ORDER BY table_name;
    """

    df = run_query(query)

    return df["table_name"].tolist()

# ------------------------------------
# Generic Aggregation Query
# ------------------------------------

def aggregation_query(
    table,
    group_col,
    metric_col,
    aggregation
):

    query = f"""
    SELECT

        "{group_col}" AS category,

        {aggregation}("{metric_col}") AS value

    FROM "{table}"

    GROUP BY "{group_col}"

    ORDER BY value DESC;
    """

    return run_query(query)


# ------------------------------------
# Count Query
# ------------------------------------

def count_query(
    table,
    group_col
):

    query = f"""
    SELECT

        "{group_col}" AS category,

        COUNT(*) AS count

    FROM "{table}"

    GROUP BY "{group_col}"

    ORDER BY count DESC;
    """

    return run_query(query)


# ------------------------------------
# Conversion Rate Query
# ------------------------------------

def conversion_rate_query(
    table,
    group_col,
    outcome_col,
    positive_value
):

    if isinstance(positive_value, str):

        value = f"'{positive_value}'"

    else:

        value = positive_value

    query = f"""
    SELECT

        "{group_col}" AS category,

        AVG(

            CASE

                WHEN "{outcome_col}" = {value}

                THEN 1

                ELSE 0

            END

        ) AS conversion_rate

    FROM "{table}"

    GROUP BY "{group_col}"

    ORDER BY conversion_rate DESC;
    """

    return run_query(query)