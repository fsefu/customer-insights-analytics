import psycopg2

class DatabaseConnection:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            print(f"Error connecting to PostgreSQL DB: {e}")
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")
    
    def get_connection(self):
        if self.connection is None:
            raise Exception("No database connection. Please call connect() first.")
        return self.connection
