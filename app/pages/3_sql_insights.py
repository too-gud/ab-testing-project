import streamlit as st
import pandas as pd
import plotly.express as px

from src.sql_util import (
    get_tables,
    get_columns,
    get_numeric_columns
)

from src.database import run_query


# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="SQL Insights",
    page_icon="📊",
    layout="wide"
)


st.title("📊 SQL Insights")


# ------------------------------------
# Check Database Connection
# ------------------------------------

try:

    tables = get_tables()

except Exception as e:

    st.error(f"Database connection failed: {e}")
    st.stop()


if len(tables) == 0:

    st.warning(
        "No tables found in PostgreSQL. Upload a dataset first."
    )

    st.stop()


# ------------------------------------
# Table Selection
# ------------------------------------

st.subheader("Select Dataset")

table = st.selectbox(
    "Choose Table",
    tables
)


# ------------------------------------
# Preview Data
# ------------------------------------

st.subheader("Dataset Preview")


preview_query = f"""
SELECT *
FROM "{table}"
LIMIT 10;
"""


preview_df = run_query(preview_query)


st.dataframe(
    preview_df,
    use_container_width=True
)

# ------------------------------------
# Analysis Selection
# ------------------------------------

st.divider()

st.subheader("Choose Analysis")


analysis_type = st.selectbox(
    "Analysis Type",
    [
        "Count by Category",
        "Aggregation",
        "Conversion Rate"
    ]
)


# ------------------------------------
# Get Columns
# ------------------------------------

columns = get_columns(table)

numeric_columns = get_numeric_columns(table)


# ------------------------------------
# Group Column
# ------------------------------------

group_col = st.selectbox(
    "Select Group Column",
    columns
)


# ------------------------------------
# Aggregation Options
# ------------------------------------

if analysis_type == "Aggregation":

    if len(numeric_columns) == 0:

        st.warning(
            "No numeric columns available for aggregation."
        )

        st.stop()


    metric_col = st.selectbox(
        "Select Numeric Metric",
        numeric_columns
    )


    aggregation = st.selectbox(
        "Select Aggregation",
        [
            "AVG",
            "SUM",
            "MIN",
            "MAX"
        ]
    )


# ------------------------------------
# Conversion Rate Options
# ------------------------------------

elif analysis_type == "Conversion Rate":

    outcome_col = st.selectbox(
        "Select Outcome Column",
        columns
    )


    positive_value = st.text_input(
        "Enter Successful Outcome Value",
        value="True"
    )

    # ------------------------------------
# Run Query
# ------------------------------------

st.divider()

if st.button("Run Analysis"):

    try:

        # -----------------------------
        # Count Analysis
        # -----------------------------

        if analysis_type == "Count by Category":

            from src.sql_util import count_query

            result_df = count_query(
                table,
                group_col
            )


        # -----------------------------
        # Aggregation Analysis
        # -----------------------------

        elif analysis_type == "Aggregation":

            from src.sql_util import aggregation_query

            result_df = aggregation_query(
                table,
                group_col,
                metric_col,
                aggregation
            )


        # -----------------------------
        # Conversion Rate Analysis
        # -----------------------------

        elif analysis_type == "Conversion Rate":

            from src.sql_util import conversion_rate_query

            # Convert text input to boolean/int where possible

            if positive_value.lower() == "true":

                positive_value = True

            elif positive_value.lower() == "false":

                positive_value = False


            result_df = conversion_rate_query(
                table,
                group_col,
                outcome_col,
                positive_value
            )


        # Store result

        st.session_state["sql_result"] = result_df


        st.success("Query executed successfully")


    except Exception as e:

        st.error(
            f"Query failed: {e}"
        )


# ------------------------------------
# Display Results
# ------------------------------------

if "sql_result" in st.session_state:

    result_df = st.session_state["sql_result"]

    st.subheader("Query Result")

    st.dataframe(
        result_df,
        use_container_width=True
    )