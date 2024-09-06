import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class TelecomEngagementAnalysis:
    def __init__(self, data):
        """Initialize the class with the dataset."""
        self.data = data
    
    def aggregate_metrics_by_customer(self):
        """Aggregate metrics per MSISDN (customer ID) and calculate total engagement metrics."""
        agg_columns = {
            'Dur. (ms)': 'sum',
            'Avg RTT DL (ms)': 'mean',
            'Avg RTT UL (ms)': 'mean',
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'Total DL (Bytes)': 'sum',
            'Total UL (Bytes)': 'sum'
        }
        self.agg_data = self.data.groupby('MSISDN/Number').agg(agg_columns).reset_index()
        return self.agg_data
    
    def top_customers_by_metric(self, metric, top_n=10):
        """Return the top N customers based on a specific metric."""
        # Check if the metric exists in the aggregated data
        if metric not in self.agg_data.columns:
            raise ValueError(f"Metric {metric} not found in aggregated data columns.")
        
        # Sort the data based on the metric and select the top N customers
        top_customers = self.agg_data[['MSISDN/Number', metric]].nlargest(top_n, metric)
        
        # Return the DataFrame (which can be displayed directly without print)
        return top_customers

    
    def normalize_metrics(self):
        """Normalize engagement metrics for clustering."""
        scaler = StandardScaler()
        self.normalized_data = pd.DataFrame(
            scaler.fit_transform(self.agg_data.drop(columns=['MSISDN/Number'])),
            columns=self.agg_data.columns[1:]
        )
        return self.normalized_data
    
    def k_means_clustering(self, n_clusters=3):
        """Run K-Means clustering on the normalized data."""
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        self.agg_data['Cluster'] = kmeans.fit_predict(self.normalized_data)
        return self.agg_data
    
    def compute_cluster_statistics(self):
        """Compute min, max, average & total of the non-normalized metrics for each cluster."""
        cluster_stats = self.agg_data.groupby('Cluster').agg(
            min_rtt_dl=('Avg RTT DL (ms)', 'min'),
            max_rtt_dl=('Avg RTT DL (ms)', 'max'),
            avg_rtt_dl=('Avg RTT DL (ms)', 'mean'),
            total_dl=('Total DL (Bytes)', 'sum'),
            total_ul=('Total UL (Bytes)', 'sum')
        )
        return cluster_stats
    
    def elbow_method(self, max_k=10):
        """Use the Elbow Method to find the optimized value of k."""
        distortions = []
        for k in range(1, max_k+1):
            kmeans = KMeans(n_clusters=k, random_state=0)
            kmeans.fit(self.normalized_data)
            distortions.append(kmeans.inertia_)
        
        plt.figure(figsize=(10,6))
        plt.plot(range(1, max_k+1), distortions, marker='o')
        plt.title('Elbow Method for Optimal K')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Distortion')
        plt.show()
    
    def aggregate_traffic_by_application(self):
        """Aggregate total traffic per application and derive the top 10 most engaged users."""
        application_columns = [
            'Social Media DL (Bytes)', 'Social Media UL (Bytes)',
            'Google DL (Bytes)', 'Google UL (Bytes)',
            'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
            'Netflix DL (Bytes)', 'Netflix UL (Bytes)'
        ]
        app_traffic = self.data.groupby('MSISDN/Number')[application_columns].sum().reset_index()
        return app_traffic
    
    def top_users_by_application(self, application, top_n=10):
        """Return the top N users by total traffic for a specific application."""
        app_traffic = self.aggregate_traffic_by_application()
        top_users = app_traffic.nlargest(top_n, application)
        return top_users[['MSISDN/Number', application]]
    
    def plot_top_applications(self, top_n=3):
        """Plot the top N most used applications."""
        app_traffic = self.aggregate_traffic_by_application()
        app_totals = app_traffic.sum().drop('MSISDN/Number').sort_values(ascending=False)
        top_apps = app_totals.head(top_n)
        
        plt.figure(figsize=(10,6))
        sns.barplot(x=top_apps.index, y=top_apps.values)
        plt.title(f'Top {top_n} Most Used Applications by Data Traffic')
        plt.xlabel('Application')
        plt.ylabel('Total Traffic (Bytes)')
        plt.xticks(rotation=45)
        plt.show()

