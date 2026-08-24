import streamlit as st
import pandas as pd

from src.data_processing import load_data, clean_data

from src.database import upload_dataframe



# -------------------- Page Config -------------------- #
st.set_page_config(
    page_title="A/B Testing Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------- Title -------------------- #
st.title("📊 A/B Testing Analytics Dashboard")

st.markdown("""
Welcome!

This dashboard allows you to:

- Upload any A/B testing dataset
- Analyze the dataset
- Perform hypothesis testing
- Visualize results
- Run SQL analysis
- Generate business insights

**Supported File Format:** CSV
""")

st.divider()

# -------------------- File Upload -------------------- #
uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)



if uploaded_file is not None:

    df = load_data(uploaded_file)
    df = clean_data(df)

    st.session_state["df"] = df

    st.success("Dataset uploaded successfully!")

    st.dataframe(df.head())

else:
    st.info("Please upload a CSV file.")

if st.button("Upload to PostgreSQL"):
    upload_dataframe(df)
    st.success("Dataset uploaded successfully!")

if uploaded_file is not None:

    try:
        df = pd.read_csv(uploaded_file)

        # Save dataframe globally
        st.session_state["df"] = df

        st.success("✅ Dataset uploaded successfully!")

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

        st.subheader("Dataset Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        st.subheader("Columns")

        st.write(df.columns.tolist())

        st.info(
            "➡️ Navigate to **Dashboard** from the left sidebar to map your columns and begin the analysis."
        )

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.warning("Please upload a CSV file to continue.")