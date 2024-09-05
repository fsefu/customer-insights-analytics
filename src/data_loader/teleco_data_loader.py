import pandas as pd

class TelecoDataLoader:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def load_data(self, table_name):
        connection = self.db_connection.get_connection()
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, connection)
        return df
