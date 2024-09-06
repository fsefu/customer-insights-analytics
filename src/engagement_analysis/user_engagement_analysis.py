import pandas as pd
import matplotlib.pyplot as plt

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
    
    def plot_aggregated_metrics(self):
        """
        Plot a multi-series line chart to display aggregated user metrics.
        Metrics displayed: session frequency, session duration, total download, total upload.
        """
        # Get aggregated user metrics
        metrics_df = self.aggregate_user_metrics()

        # Sort data by session frequency to have a meaningful X-axis
        metrics_df = metrics_df.sort_values(by='sessions_frequency', ascending=False).head(20)  # limit to top 20 for clarity

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each metric as a separate line
        ax.plot(metrics_df['MSISDN/Number'], metrics_df['sessions_frequency'], label='Session Frequency', marker='o')
        ax.plot(metrics_df['MSISDN/Number'], metrics_df['total_session_duration'], label='Session Duration (ms)', marker='o')
        ax.plot(metrics_df['MSISDN/Number'], metrics_df['total_download'], label='Total Download (Bytes)', marker='o')
        ax.plot(metrics_df['MSISDN/Number'], metrics_df['total_upload'], label='Total Upload (Bytes)', marker='o')

        # Set titles and labels
        ax.set_title('Aggregated Metrics Across Users')
        ax.set_xlabel('User (MSISDN/Number)')
        ax.set_ylabel('Metrics Value')
        ax.legend()

        # Rotate X-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Adjust layout
        plt.tight_layout()
        plt.show()

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
