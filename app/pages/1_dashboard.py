import streamlit as st
import pandas as pd

# -------------------- Page Config -------------------- #
st.set_page_config(
    page_title="Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Dataset Dashboard")

# -------------------- Check Dataset -------------------- #

if "df" not in st.session_state:
    st.error("Please upload a dataset from the Home page first.")
    st.stop()

df = st.session_state["df"]

# -------------------- Dataset Overview -------------------- #

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Missing Values", int(df.isnull().sum().sum()))

st.divider()

# -------------------- Column Mapping -------------------- #

st.header("Column Mapping")

columns = df.columns.tolist()

group_col = st.selectbox(
    "Select the Group Column",
    columns,
    help="Column containing Control and Treatment groups."
)

outcome_col = st.selectbox(
    "Select the Outcome Column",
    columns,
    help="Column containing conversions or outcomes."
)

# -------------------- Group Selection -------------------- #

groups = sorted(df[group_col].dropna().unique())

control_group = st.selectbox(
    "Select Control Group",
    groups
)

treatment_group = st.selectbox(
    "Select Treatment Group",
    groups,
    index=1 if len(groups) > 1 else 0
)

# Prevent same selection
if control_group == treatment_group:
    st.warning("Control and Treatment groups cannot be the same.")
    st.stop()

# -------------------- Outcome Type -------------------- #

st.header("Outcome Mapping")

unique_values = sorted(df[outcome_col].dropna().unique())

if len(unique_values) == 2:

    positive_value = st.selectbox(
        "Which value represents a Conversion?",
        unique_values
    )

else:

    st.error(
        "Outcome column must contain only two unique values (binary outcome)."
    )
    st.stop()

# -------------------- Save Session -------------------- #

st.session_state["group_col"] = group_col
st.session_state["outcome_col"] = outcome_col
st.session_state["control_group"] = control_group
st.session_state["treatment_group"] = treatment_group
st.session_state["positive_value"] = positive_value
st.session_state["table_name"] = "marketing_data"

# -------------------- Preview -------------------- #

st.divider()

st.subheader("Mapped Dataset Preview")

preview = df[[group_col, outcome_col]].copy()

st.dataframe(
    preview.head(10),
    use_container_width=True
)

# -------------------- Summary -------------------- #

st.divider()

st.success("Configuration Saved Successfully!")

st.write("### Selected Configuration")

st.write(f"**Group Column:** `{group_col}`")
st.write(f"**Outcome Column:** `{outcome_col}`")
st.write(f"**Control Group:** `{control_group}`")
st.write(f"**Treatment Group:** `{treatment_group}`")
st.write(f"**Conversion Value:** `{positive_value}`")

st.info(
    "You can now proceed to the **A/B Test** page to perform statistical analysis."
)