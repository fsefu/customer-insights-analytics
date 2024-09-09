import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

class SatisfactionKMeans:
    def __init__(self, data):
        """
        Initialize the SatisfactionKMeans class with user data.
        
        Parameters:
        - data: DataFrame containing user data with engagement and experience scores.
        """
        self.data = data
        self.scaled_data = None
        self.kmeans = None
        self.clustered_data = None
    
    def preprocess_data(self):
        """
        Preprocess the data by scaling the engagement and experience scores.
        """
        # Select engagement and experience scores for clustering
        features = ['engagement_score', 'experience_score']
        
        # Extract features for scaling
        X = self.data[features].values
        
        # Standardize features
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(X)
    
    def run_kmeans(self, k=2):
        """
        Run K-means clustering on the preprocessed data.
        
        Parameters:
        - k: Number of clusters.
        
        Returns:
        - DataFrame with assigned cluster labels.
        """
        # Initialize KMeans
        self.kmeans = KMeans(n_clusters=k, random_state=42)
        
        # Fit KMeans model
        self.data['cluster'] = self.kmeans.fit_predict(self.scaled_data)
        
        # Return the DataFrame with cluster labels
        self.clustered_data = self.data.copy()
        return self.clustered_data
    
    def visualize_clusters(self):
        """
        Visualize the clusters using a scatter plot.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=self.clustered_data,
            x='engagement_score',
            y='experience_score',
            hue='cluster',
            palette='viridis',
            marker='o',
            edgecolor='w',
            s=100
        )
        plt.title('K-Means Clustering of Engagement and Experience Scores')
        plt.xlabel('Engagement Score')
        plt.ylabel('Experience Score')
        plt.legend(title='Cluster')
        plt.grid(True)
        plt.show()

# # Example usage:
# if __name__ == "__main__":
#     # Load your user data with engagement and experience scores
#     user_scores_df = pd.read_csv('user_scores.csv')  # Replace with your data source
    
#     # Instantiate the SatisfactionKMeans class
#     kmeans_analysis = SatisfactionKMeans(data=user_scores_df)
    
#     # Preprocess data and run K-means
#     kmeans_analysis.preprocess_data()
#     clustered_data = kmeans_analysis.run_kmeans(k=2)
    
#     # Visualize the clusters
#     kmeans_analysis.visualize_clusters()
    
#     # Display the resulting DataFrame with cluster labels
#     print(clustered_data.head())
