import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

class ExperienceClustering:
    def __init__(self, df):
        """
        Initialize the class with the dataframe.
        """
        self.df = df
        self.features = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 
                         'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 
                         'TCP UL Retrans. Vol (Bytes)']
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)

    def preprocess_data(self):
        """
        Preprocess the data by selecting relevant features and scaling them.
        """
        self.scaled_features = self.scaler.fit_transform(self.df[self.features])
    
    def perform_clustering(self):
        """
        Apply K-Means clustering on the preprocessed data and store the cluster labels.
        """
        self.df['Cluster'] = self.kmeans.fit_predict(self.scaled_features)
    
    def visualize_clusters(self):
        """
        Visualize the clusters using PCA for dimensionality reduction.
        """
        # Reduce dimensions to 2 using PCA
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(self.scaled_features)

        # Create a DataFrame with the principal components and the cluster labels
        pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
        pca_df['Cluster'] = self.df['Cluster']

        # Plot the clusters
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='PC1', y='PC2', hue='Cluster', palette='viridis', data=pca_df, s=100)

        # Enhance the plot with titles and labels
        plt.title('K-Means Clustering of User Experience Metrics', fontsize=16)
        plt.xlabel('Principal Component 1', fontsize=12)
        plt.ylabel('Principal Component 2', fontsize=12)
        plt.legend(title='Cluster')
        plt.grid(True)

        # Show the plot
        plt.show()
    
    def describe_clusters(self):
        """
        Describe the characteristics of each cluster based on the centroids.
        """
        # Get the centroids of the clusters
        centroids = self.scaler.inverse_transform(self.kmeans.cluster_centers_)
        centroid_df = pd.DataFrame(centroids, columns=self.features)

        # Print the centroid characteristics
        for i in range(3):
            print(f"Cluster {i} characteristics:\n{centroid_df.iloc[i]}\n")
    
    def get_clustered_data(self):
        """
        Return the DataFrame with the cluster labels.
        """
        return self.df[['MSISDN/Number', 'Cluster']]

    def run(self):
        """
        Run the entire clustering process: preprocessing, clustering, visualization, and description.
        """
        self.preprocess_data()
        self.perform_clustering()
        self.visualize_clusters()
        self.describe_clusters()