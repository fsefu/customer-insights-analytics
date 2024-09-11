import os
import sys
import streamlit as st
import mlflow
import mlflow.sklearn
from dashboard_analytics.satisfaction_analysis import SatisfactionAnalytics
from dashboard_analytics.user_overview import UserOverview
from dashboard_analytics.experience_analytics import ExperienceAnalytics
from dashboard_analytics.engagement_analysis import EngagementAnalytics

# Ensure the correct paths are set
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../databases'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from load_env import load_environment
from connections.database_connector import DatabaseConnection
from data_loader.teleco_data_loader import TelecoDataLoader
from cleaning.data_cleaning import DataCleaner

class TellCoAnalyticsDashboard:
    def __init__(self):
        load_environment()  # Load environment variables
        self.db_connection = self.connect_to_database()
        self.df = self.load_and_clean_data()

    @staticmethod
    def connect_to_database():
        if os.getenv('STREAMLIT_ENV') == 'production':
            db_connection = DatabaseConnection(
                db_name=st.secrets["DB_NAME"],
                user=st.secrets["DB_USER"],
                password=st.secrets["DB_PASSWORD"],
                host=st.secrets["DB_HOST"],
                port=st.secrets["DB_PORT"]
            )
            db_connection.connect()
            return db_connection
        else:
            db_connection = DatabaseConnection(
                db_name=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            db_connection.connect()
            
            return db_connection

    def load_and_clean_data(self):
        data_loader = TelecoDataLoader(db_connection=self.db_connection)
        df = data_loader.load_data("xdr_data")
        self.db_connection.close()

        data_cleaner = DataCleaner(df)
        data_cleaner.clean_data()
        data_cleaner.convert_units_to_mb()
        data_cleaner.handle_missing_and_outliers()

        return data_cleaner.df

    def track_model(self, analysis_name, params, metrics):
        mlflow.set_experiment("TellCo_Model_Tracking")
        
        with mlflow.start_run(run_name=analysis_name):
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.log_artifact("xdr_data.csv")  # Example of logging artifacts

            st.write(f"Model tracking for {analysis_name} completed.")

    def run(self):
        st.title("TellCo User Analytics Dashboard")
        st.sidebar.header("Navigation")
        option = st.sidebar.selectbox(
            "Select an analysis", 
            ["User Overview", "Experience Analytics", "Engagement Analytics", "Satisfaction Analytics"]
        )

        if option == "User Overview":
            UserOverview(self.df).display()
            self.track_model("User Overview", params={"example_param": "value"}, metrics={"example_metric": 0.9})
        elif option == "Experience Analytics":
            ExperienceAnalytics(self.df).display()
            self.track_model("Experience Analytics", params={"example_param": "value"}, metrics={"example_metric": 0.85})
        elif option == "Engagement Analytics":
            EngagementAnalytics(self.df).display()
            self.track_model("Engagement Analytics", params={"example_param": "value"}, metrics={"example_metric": 0.8})
        elif option == "Satisfaction Analytics":
            SatisfactionAnalytics(self.df).display()
            self.track_model("Satisfaction Analytics", params={"example_param": "value"}, metrics={"example_metric": 0.95})

# Run the dashboard
if __name__ == '__main__':

    dashboard = TellCoAnalyticsDashboard()
    dashboard.run()
