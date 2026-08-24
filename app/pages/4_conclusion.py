import streamlit as st


# ------------------------------------
# Page Config
# ------------------------------------

st.set_page_config(
    page_title="Conclusion",
    page_icon="✅",
    layout="wide"
)


st.title("✅ A/B Test Conclusion")


# ------------------------------------
# Check Results
# ------------------------------------

if "ab_results" not in st.session_state:

    st.warning(
        "Run the A/B Test first to generate results."
    )

    st.stop()


results = st.session_state["ab_results"]


# ------------------------------------
# Extract Values
# ------------------------------------

control_rate = results["control_rate"]

treatment_rate = results["treatment_rate"]

lift = results["relative_lift"]

p_value = results["p_value"]

significant = results["significant"]


# ------------------------------------
# KPI Cards
# ------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Control Conversion",
        f"{control_rate:.2%}"
    )


with col2:

    st.metric(
        "Treatment Conversion",
        f"{treatment_rate:.2%}"
    )


with col3:

    st.metric(
        "Relative Lift",
        f"{lift:.2f}%"
    )


with col4:

    st.metric(
        "P Value",
        f"{p_value:.5f}"
    )


# ------------------------------------
# Winner
# ------------------------------------

st.divider()

st.subheader("Experiment Result")


if significant:

    if treatment_rate > control_rate:

        winner = "Treatment"

        st.success(
            "🎉 Treatment group performed significantly better."
        )


    else:

        winner = "Control"

        st.error(
            "Control group performed significantly better."
        )


else:

    winner = "No clear winner"

    st.warning(
        "The difference is not statistically significant."
    )


# ------------------------------------
# Business Recommendation
# ------------------------------------

st.divider()

st.subheader("Business Recommendation")


if winner == "Treatment":

    st.write(
        """
        **Recommendation: Deploy the treatment version.**

        The experiment shows that the treatment increased
        the conversion rate with statistical confidence.

        Expected impact:
        - Higher conversions
        - Improved user experience
        - Potential revenue increase
        """
    )


elif winner == "Control":

    st.write(
        """
        **Recommendation: Keep the control version.**

        The treatment did not improve performance and
        the original version remains better.
        """
    )


else:

    st.write(
        """
        **Recommendation: Continue testing.**

        The experiment did not produce a statistically
        significant result.

        Possible actions:
        - Increase sample size
        - Run experiment longer
        - Test a stronger variation
        """
    )


# ------------------------------------
# Statistical Explanation
# ------------------------------------

st.divider()

st.subheader("Statistical Interpretation")


if significant:

    st.write(
        f"""
        Since the p-value ({p_value:.5f}) is less than 0.05,
        we reject the null hypothesis.

        The observed difference between groups is unlikely
        to be caused by random chance.
        """
    )

else:

    st.write(
        f"""
        Since the p-value ({p_value:.5f}) is greater than 0.05,
        we fail to reject the null hypothesis.

        There is insufficient evidence that the groups are
        different.
        """
    )


# ------------------------------------
# Experiment Summary
# ------------------------------------

st.divider()

st.subheader("Experiment Summary")

st.write(
    """
    This experiment compared two randomized groups to determine
    whether the treatment produced a measurable improvement.

    The analysis included:

    ✓ Conversion rate comparison

    ✓ Statistical significance testing

    ✓ Confidence interval analysis

    ✓ Effect size measurement

    ✓ Business recommendation
    """
)