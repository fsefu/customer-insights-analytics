# utils/db_handler.py

import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../databases')))

from connections.database_connector import DatabaseConnection

# Load environment variables
load_dotenv()

class DbExporter:
    def __init__(self):
        """
        Initialize the PostgresExporter with PostgreSQL connection details from environment variables.
        """
        self.db_connection = DatabaseConnection(
            db_name=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.engine = self._create_engine()
        
    def _create_engine(self):
        """
        Create a SQLAlchemy engine using the DatabaseConnection class.
        """
        # Connect using the custom DatabaseConnection class
        self.db_connection.connect()
        return create_engine(
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

    def export_to_postgres(self, df, table_name='user_scores_test', if_exists='replace'):
        """
        Export a DataFrame to a PostgreSQL table.

        Parameters:
        - df: pd.DataFrame, the DataFrame to export.
        - table_name: str, name of the table in the database.
        - if_exists: str, behavior if the table already exists ('replace', 'append', etc.)
        """
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)
        print(f"Data exported to {table_name} table in PostgreSQL database.")
