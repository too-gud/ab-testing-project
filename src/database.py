import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------
# Database Configuration
# -------------------------------

DB_USER = "postgres"
DB_PASSWORD = "vK27652475"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ab_test"

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# -------------------------------
# Test Connection
# -------------------------------

def test_connection():
    """
    Test PostgreSQL connection.
    """

    try:

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return True

    except Exception as e:
        print(e)
        return False


# -------------------------------
# Upload DataFrame
# -------------------------------

def upload_dataframe(df, table_name="marketing_data"):
    """
    Upload DataFrame to PostgreSQL.
    """

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )


# -------------------------------
# Execute SELECT Query
# -------------------------------

def run_query(query):

    return pd.read_sql(query, engine)


# -------------------------------
# Execute INSERT/UPDATE/DELETE
# -------------------------------

def execute_query(query):

    with engine.begin() as conn:

        conn.execute(text(query))


# -------------------------------
# Get Table Names
# -------------------------------

def get_tables():

    query = """

    SELECT table_name

    FROM information_schema.tables

    WHERE table_schema='public';

    """

    return pd.read_sql(query, engine)


# -------------------------------
# Read Whole Table
# -------------------------------

def read_table(table_name):

    return pd.read_sql(

        f"SELECT * FROM {table_name}",

        engine

    )