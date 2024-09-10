import os
import sys
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Add necessary paths for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../databases'))

# Import modules
from cleaning.data_cleaning import DataCleaner
from data_loader.teleco_data_loader import TelecoDataLoader
from connections.database_connector import DatabaseConnection
from engagement_analysis.telecom_engagement_analysis import TelecomEngagementAnalysis
from engagement_analysis.user_engagement_analysis import UserEngagementAnalysis
from experience_analytics.experience_clustering import ExperienceClustering
from satisfaction_analysis.engagement_experience_scores import EngagementExperienceScores
from satisfaction_analysis.top_satifactions_analysis import TopSatisfactionAnalysis
from satisfaction_analysis.satisfaction_score_predictor import SatisfactionScorePredictor
from satisfaction_analysis.satisfaction_kmeans import SatisfactionKMeans
from satisfaction_analysis.cluster_score_aggregator import ClusterScoreAggregator


class FinalDataExporter:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def export_to_mysql(self, df, table_name):
        df.to_sql(name=table_name, con=self.db_connection.engine, if_exists='replace', index=False)
        print(f"Data exported to {table_name} in MySQL database.")

    def verify_export(self, table_name, limit=10):
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        result = self.db_connection.execute_query(query)
        if not result.empty:
            print(f"Data successfully inserted into {table_name}. Sample records:")
            print(result)
        else:
            print(f"No data found in {table_name}.")


def main():
    load_dotenv()

    # Initialize and connect to the database
    db_connection = DatabaseConnection(
        db_name=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    db_connection.connect()

    # Load and clean data
    data_loader = TelecoDataLoader(db_connection)
    raw_df = data_loader.load_data("xdr_data")

    data_cleaner = DataCleaner(raw_df)
    data_cleaner.clean_data()
    data_cleaner.convert_units_to_mb()
    data_cleaner.handle_missing_and_outliers()
    cleaned_df = data_cleaner.df

    # Engagement Analysis
    user_engagement = UserEngagementAnalysis(cleaned_df)
    engagement_metrics = user_engagement.aggregate_user_metrics()
    normalized_engagement_metrics = user_engagement.normalize_metrics(engagement_metrics)

    telecom_engagement_analysis = TelecomEngagementAnalysis(cleaned_df)
    telecom_engagement_analysis.aggregate_metrics_by_customer()
    telecom_engagement_analysis.normalize_metrics()
    engagement_data_with_clusters = telecom_engagement_analysis.k_means_clustering()

    # Experience Analysis
    experience_clustering = ExperienceClustering(df=cleaned_df)
    experience_clustering.run()
    experience_data = experience_clustering.df[['MSISDN/Number', 'Cluster']]

    # Merge engagement and experience data
    user_df = pd.merge(engagement_data_with_clusters, experience_data, on='MSISDN/Number', how='inner')
    user_df.rename(columns={'Cluster': 'experience_cluster'}, inplace=True)

    # Satisfaction Analysis
    engagement_clusters = telecom_engagement_analysis.kmeans  # Assuming this is the clustering model
    experience_clusters = experience_clustering.kmeans  # Assuming this is the clustering model

    satisfaction_analysis = EngagementExperienceScores(
        user_data=user_df,
        engagement_clusters=engagement_clusters,
        experience_clusters=experience_clusters
    )
    user_scores_df = satisfaction_analysis.assign_scores_to_users()

    # Top Satisfaction Analysis
    top_satisfaction_analysis = TopSatisfactionAnalysis(
        user_data=user_df,
        engagement_clusters=engagement_clusters,
        experience_clusters=experience_clusters
    )
    top_satisfied_customers = top_satisfaction_analysis.top_n_satisfied_customers(n=10)
    print(top_satisfied_customers)
    top_satisfaction_analysis.visualize_top_satisfaction(user_df)

    # Satisfaction Score Prediction
    satisfaction_predictor = SatisfactionScorePredictor(user_data=user_scores_df)
    satisfaction_predictor.build_regression_model()
    predicted_satisfaction = satisfaction_predictor.predict_satisfaction(engagement_score=50, experience_score=45)
    print(f"Predicted Satisfaction Score: {predicted_satisfaction:.2f}")

    # Satisfaction KMeans Clustering
    kmeans_analysis = SatisfactionKMeans(data=user_scores_df)
    kmeans_analysis.preprocess_data()
    clustered_data = kmeans_analysis.run_kmeans(k=2)
    kmeans_analysis.visualize_clusters()

    # Aggregate Cluster Scores
    score_aggregator = ClusterScoreAggregator(user_data=clustered_data)
    score_aggregator.plot_cluster_scores()

    # Export final data to MySQL
    exporter = FinalDataExporter(db_connection)
    exporter.export_to_mysql(user_scores_df, table_name='user_scores')
    exporter.verify_export('user_scores')
    # # Verify if the data is inserted
    # exporter = FinalDataExporter(db_connection)
    # exporter.verify_export('user_scores', limit=10)

    # Disconnect from the database
    db_connection.disconnect()


if __name__ == "__main__":
    main()
