import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

class ExperienceClustering:
    def __init__(self, df):
        self.df = df
        self.preprocessed_df = None
        self.cluster_centers = None
        self.labels = None
    
    def preprocess_data(self):
        # Select relevant columns for clustering
        experience_metrics = [
            'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 
            'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)',
            # Add more relevant columns if needed
        ]
        
        self.preprocessed_df = self.df[experience_metrics]
        
        # Handling missing values (mean for numerical columns)
        imputer = SimpleImputer(strategy='mean')
        self.preprocessed_df = pd.DataFrame(imputer.fit_transform(self.preprocessed_df), columns=experience_metrics)
        
        # Scaling the data
        scaler = StandardScaler()
        self.preprocessed_df = pd.DataFrame(scaler.fit_transform(self.preprocessed_df), columns=experience_metrics)
    
    def fit_kmeans(self, n_clusters=3):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.labels = kmeans.fit_predict(self.preprocessed_df)
        self.cluster_centers = kmeans.cluster_centers_
    
    def describe_clusters(self):
        cluster_description = {}
        for i, center in enumerate(self.cluster_centers):
            cluster_description[f'Cluster {i+1}'] = dict(zip(self.preprocessed_df.columns, center))
        return cluster_description

# # Load your dataset
# df = pd.read_csv('path_to_your_data.csv')

# # Create an instance of the ExperienceClustering class
# clustering = ExperienceClustering(df)

# # Preprocess the data
# clustering.preprocess_data()

# # Fit the K-means clustering model
# clustering.fit_kmeans(n_clusters=3)

# # Describe the clusters
# cluster_descriptions = clustering.describe_clusters()

# # Output the cluster descriptions
# for cluster, description in cluster_descriptions.items():
#     print(f"{cluster}:")
#     for metric, value in description.items():
#         print(f"  {metric}: {value}")
#     print()
