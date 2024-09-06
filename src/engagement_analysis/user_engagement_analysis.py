# user_engagement_analysis.py
import pandas as pd

class UserEngagementAnalysis:
    def __init__(self, data):
        """
        Initialize the analysis with the dataset.
        Args:
            data (pd.DataFrame): The telecommunication dataset containing user sessions.
        """
        self.data = data

    def aggregate_user_metrics(self):
        """
        Aggregate the metrics for each user based on session frequency, duration, and traffic.
        Returns:
            pd.DataFrame: Aggregated user engagement metrics.
        """
        # Aggregating the required metrics per user (MSISDN/Number)
        engagement_metrics = self.data.groupby('MSISDN/Number').agg(
            sessions_frequency=('Bearer Id', 'count'), # Count of sessions
            total_session_duration=('Dur. (ms)', 'sum'), # Sum of session durations
            total_download=('Total DL (Bytes)', 'sum'), # Sum of download traffic
            total_upload=('Total UL (Bytes)', 'sum'), # Sum of upload traffic
        )

        # Add a total traffic column (DL + UL)
        engagement_metrics['total_traffic'] = engagement_metrics['total_download'] + engagement_metrics['total_upload']
        engagement_metrics = engagement_metrics.reset_index()

        return engagement_metrics

    def top_customers_by_engagement(self, metric, top_n=10):
        """
        Get the top customers based on the specified engagement metric.
        Args:
            metric (str): The engagement metric to rank the customers by.
            top_n (int): Number of top customers to retrieve.
        Returns:
            pd.DataFrame: Top customers ranked by the specified metric.
        """
        aggregated_metrics = self.aggregate_user_metrics()
        return aggregated_metrics.sort_values(by=metric, ascending=False).head(top_n)

    def normalize_metrics(self, metrics_df):
        """
        Normalize the metrics for clustering or further analysis.
        Args:
            metrics_df (pd.DataFrame): DataFrame containing the aggregated user metrics.
        Returns:
            pd.DataFrame: Normalized metrics.
        """
        normalized_df = metrics_df.copy()
        for column in ['sessions_frequency', 'total_session_duration', 'total_traffic']:
            normalized_df[column] = (metrics_df[column] - metrics_df[column].mean()) / metrics_df[column].std()
        
        return normalized_df
