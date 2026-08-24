import numpy as np
from scipy.stats import norm, ttest_ind


# -----------------------------------------------------
# Conversion Rate
# -----------------------------------------------------

def conversion_rate(conversions, total):
    return conversions / total


# -----------------------------------------------------
# Pooled Proportion
# -----------------------------------------------------

def pooled_proportion(c1, c2, n1, n2):
    return (c1 + c2) / (n1 + n2)


# -----------------------------------------------------
# Standard Error (Difference in Proportions)
# -----------------------------------------------------

def standard_error(p_pool, n1, n2):
    return np.sqrt(
        p_pool * (1 - p_pool) * ((1 / n1) + (1 / n2))
    )


# -----------------------------------------------------
# Z Statistic
# -----------------------------------------------------

def z_statistic(p1, p2, se):
    return (p2 - p1) / se


# -----------------------------------------------------
# P Value
# -----------------------------------------------------

def p_value(z, alternative="two-sided"):

    if alternative == "greater":
        return 1 - norm.cdf(z)

    elif alternative == "less":
        return norm.cdf(z)

    else:
        return 2 * (1 - norm.cdf(abs(z)))


# -----------------------------------------------------
# Confidence Interval
# -----------------------------------------------------

def confidence_interval(p1, p2, n1, n2, confidence=0.95):

    diff = p2 - p1

    se = np.sqrt(
        (p1 * (1 - p1) / n1)
        +
        (p2 * (1 - p2) / n2)
    )

    z = norm.ppf((1 + confidence) / 2)

    lower = diff - z * se
    upper = diff + z * se

    return lower, upper


# -----------------------------------------------------
# Absolute Lift
# -----------------------------------------------------

def absolute_lift(p1, p2):
    return p2 - p1


# -----------------------------------------------------
# Relative Lift
# -----------------------------------------------------

def relative_lift(p1, p2):
    return ((p2 - p1) / p1) * 100


# -----------------------------------------------------
# Cohen's h
# -----------------------------------------------------

def effect_size(p1, p2):

    return (
        2 * np.arcsin(np.sqrt(p2))
        -
        2 * np.arcsin(np.sqrt(p1))
    )


# -----------------------------------------------------
# Binary A/B Test
# -----------------------------------------------------

def perform_ab_test(conversions_control,
                    total_control,
                    conversions_treatment,
                    total_treatment):

    p1 = conversion_rate(conversions_control, total_control)
    p2 = conversion_rate(conversions_treatment, total_treatment)

    pooled = pooled_proportion(
        conversions_control,
        conversions_treatment,
        total_control,
        total_treatment
    )

    se = standard_error(
        pooled,
        total_control,
        total_treatment
    )

    z = z_statistic(
        p1,
        p2,
        se
    )

    p = p_value(z)

    ci = confidence_interval(
        p1,
        p2,
        total_control,
        total_treatment
    )

    return {

        "control_rate": p1,
        "treatment_rate": p2,

        "absolute_lift": absolute_lift(p1, p2),
        "relative_lift": relative_lift(p1, p2),

        "pooled_proportion": pooled,
        "standard_error": se,

        "z_statistic": z,
        "p_value": p,

        "confidence_interval": ci,

        "effect_size": effect_size(p1, p2),

        "significant": p < 0.05
    }


# -----------------------------------------------------
# Continuous Metrics (Revenue, Session Time)
# -----------------------------------------------------

def perform_t_test(control, treatment):

    t_stat, p = ttest_ind(
        treatment,
        control,
        equal_var=False
    )

    return {

        "control_mean": np.mean(control),
        "treatment_mean": np.mean(treatment),

        "mean_difference":
            np.mean(treatment) -
            np.mean(control),

        "t_statistic": t_stat,

        "p_value": p,

        "significant": p < 0.05
    }