-- ==========================================================
-- analysis_queries.sql
--
-- Purpose:
-- Generic SQL query templates used in A/B Testing analysis.
--
-- NOTE:
-- These queries are examples/documentation.
-- The Streamlit application generates equivalent SQL
-- dynamically using sql_utils.py.
-- ==========================================================


-------------------------------------------------------------
-- 1. Sample Size by Group
-------------------------------------------------------------

SELECT

    group_column,

    COUNT(*) AS sample_size

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 2. Average Metric by Group
-------------------------------------------------------------

SELECT

    group_column,

    AVG(metric_column) AS average_value,

    MIN(metric_column) AS minimum_value,

    MAX(metric_column) AS maximum_value

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 3. Sum of Metric by Group
-------------------------------------------------------------

SELECT

    group_column,

    SUM(metric_column) AS total_value

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 4. Conversion Rate
-------------------------------------------------------------

SELECT

    group_column,

    COUNT(*) AS users,

    AVG(

        CASE

            WHEN outcome_column = positive_value

            THEN 1

            ELSE 0

        END

    ) AS conversion_rate

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 5. Distribution of Categories
-------------------------------------------------------------

SELECT

    category_column,

    COUNT(*) AS frequency

FROM table_name

GROUP BY category_column

ORDER BY frequency DESC;



-------------------------------------------------------------
-- 6. Ranking Groups (Window Function)
-------------------------------------------------------------

SELECT

    group_column,

    AVG(metric_column) AS average_metric,

    RANK() OVER(

        ORDER BY AVG(metric_column) DESC

    ) AS ranking

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 7. Percentage Distribution
-------------------------------------------------------------

SELECT

    group_column,

    COUNT(*) AS total,

    COUNT(*) * 100.0 /

    SUM(COUNT(*)) OVER()

    AS percentage

FROM table_name

GROUP BY group_column;



-------------------------------------------------------------
-- 8. Cumulative Metric
-------------------------------------------------------------

SELECT

    date_column,

    SUM(metric_column) AS daily_total,

    SUM(

        SUM(metric_column)

    ) OVER(

        ORDER BY date_column

    ) AS cumulative_total

FROM table_name

GROUP BY date_column;