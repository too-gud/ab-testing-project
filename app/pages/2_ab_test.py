import streamlit as st
import pandas as pd
import plotly.express as px

from src.statistics import perform_ab_test

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="A/B Test",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 A/B Testing Results")

# -------------------------------------------------------
# Check Session
# -------------------------------------------------------

required = [
    "df",
    "group_col",
    "outcome_col",
    "control_group",
    "treatment_group",
    "positive_value"
]

for key in required:
    if key not in st.session_state:
        st.error("Please complete the Dashboard page first.")
        st.stop()

df = st.session_state["df"]

group_col = st.session_state["group_col"]
outcome_col = st.session_state["outcome_col"]

control_group = st.session_state["control_group"]
treatment_group = st.session_state["treatment_group"]

positive_value = st.session_state["positive_value"]

# -------------------------------------------------------
# Convert Outcome to Binary
# -------------------------------------------------------

temp = df.copy()

temp[outcome_col] = (
    temp[outcome_col] == positive_value
).astype(int)

# -------------------------------------------------------
# Split Groups
# -------------------------------------------------------

control = temp[temp[group_col] == control_group]

treatment = temp[temp[group_col] == treatment_group]

n_control = len(control)
n_treatment = len(treatment)

conv_control = control[outcome_col].sum()
conv_treatment = treatment[outcome_col].sum()

# -------------------------------------------------------
# Perform Test
# -------------------------------------------------------

results = perform_ab_test(
    conv_control,
    n_control,
    conv_treatment,
    n_treatment
)

st.session_state["ab_results"] = results
# -------------------------------------------------------
# Sample Information
# -------------------------------------------------------

st.header("Sample Information")

c1, c2 = st.columns(2)

with c1:
    st.metric("Control Users", n_control)
    st.metric("Conversions", conv_control)

with c2:
    st.metric("Treatment Users", n_treatment)
    st.metric("Conversions", conv_treatment)

# -------------------------------------------------------
# Results
# -------------------------------------------------------

st.header("Results")

a, b, c = st.columns(3)

with a:
    st.metric(
        "Control Conversion",
        f"{results['control_rate']:.2%}"
    )

with b:
    st.metric(
        "Treatment Conversion",
        f"{results['treatment_rate']:.2%}"
    )

with c:
    st.metric(
        "Relative Lift",
        f"{results['relative_lift']:.2f}%"
    )

# -------------------------------------------------------
# Statistical Metrics
# -------------------------------------------------------

st.header("Statistical Test")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Z Statistic",
        round(results["z_statistic"], 3)
    )

with col2:
    st.metric(
        "P Value",
        round(results["p_value"], 5)
    )

with col3:
    st.metric(
        "Effect Size",
        round(results["effect_size"], 3)
    )

# -------------------------------------------------------
# Confidence Interval
# -------------------------------------------------------

lower, upper = results["confidence_interval"]

st.write("### 95% Confidence Interval")

st.success(
    f"({lower:.4f}, {upper:.4f})"
)

# -------------------------------------------------------
# Decision
# -------------------------------------------------------

st.header("Decision")

if results["significant"]:

    st.success(
        "✅ Reject the Null Hypothesis\n\n"
        "The treatment produced a statistically significant change."
    )

else:

    st.warning(
        "❌ Fail to Reject the Null Hypothesis\n\n"
        "No statistically significant difference was detected."
    )

# -------------------------------------------------------
# Business Recommendation
# -------------------------------------------------------

st.header("Business Recommendation")

if (
    results["significant"]
    and
    results["treatment_rate"] > results["control_rate"]
):

    st.success(
        "Deploy the Treatment version. "
        "It significantly outperformed the Control."
    )

elif (
    results["significant"]
    and
    results["treatment_rate"] < results["control_rate"]
):

    st.error(
        "Do not deploy the Treatment version. "
        "The Control performed better."
    )

else:

    st.info(
        "Collect more data before making a business decision."
    )

# -------------------------------------------------------
# Visualization
# -------------------------------------------------------

st.header("Conversion Rate Comparison")

plot_df = pd.DataFrame({

    "Group": [
        control_group,
        treatment_group
    ],

    "Conversion Rate": [

        results["control_rate"],

        results["treatment_rate"]

    ]

})

fig = px.bar(

    plot_df,

    x="Group",

    y="Conversion Rate",

    text="Conversion Rate"

)

fig.update_traces(texttemplate="%{text:.2%}")

st.plotly_chart(
    fig,
    use_container_width=True
)