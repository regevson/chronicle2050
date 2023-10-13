import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path = os.path.join(base_dir, '../../.env'))
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DOMAIN = os.environ.get('DB_DOMAIN')

def conn_to_db(db):
    encoded = quote_plus(DB_PASSWORD)
    db_url = f"mysql+mysqldb://root:{encoded}@{DB_DOMAIN}:2306/{db}"
    engine = create_engine(db_url)
    return engine

def download_df(db, table):
    return pd.read_sql_table(table, conn_to_db(db))

def upload_to_db(db, table, df):
    df.to_sql(table, conn_to_db(db), if_exists = 'replace')

def append_to_db(db, table, df, delete):
    df.to_sql(table, conn_to_db(db), if_exists = 'append')
