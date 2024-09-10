import numpy as np
import pandas as pd

class EngagementExperienceScores:
    def __init__(self, user_data, engagement_clusters, experience_clusters):
        """
        Initialize the EngagementExperienceScores class with user data, engagement, and experience clusters.
        
        Parameters:
        - user_data: DataFrame containing user data for analysis.
        - engagement_clusters: Clustering model for user engagement.
        - experience_clusters: Clustering model for user experience.
        """
        self.user_data = user_data
        self.engagement_clusters = engagement_clusters
        self.experience_clusters = experience_clusters
        
        # Get cluster centroids (make sure they match the feature dimensions)
        self.least_engaged_centroid = self._find_cluster_centroid(self.engagement_clusters, cluster_label=0)
        self.worst_experience_centroid = self._find_cluster_centroid(self.experience_clusters, cluster_label=0)
    
    def _find_cluster_centroid(self, clusters, cluster_label):
        """
        Private method to find the centroid of a specified cluster.
        
        Parameters:
        - clusters: Clustering model containing cluster centroids.
        - cluster_label: The label of the cluster for which the centroid is required.
        
        Returns:
        - Centroid of the specified cluster as a numpy array.
        """
        return clusters.cluster_centers_[cluster_label]

    def _validate_columns(self, user_features, required_columns):
        """
        Validate if the required columns exist in the user features.
        
        Parameters:
        - user_features: DataFrame or Series containing user features.
        - required_columns: List of columns that should be present.
        
        Returns:
        - DataFrame with only the valid columns, missing columns will be filled with NaN.
        """
        missing_columns = [col for col in required_columns if col not in user_features.index]
        if missing_columns:
            print(f"Warning: Missing columns - {missing_columns}")
        
        # Add missing columns with NaN values
        for col in missing_columns:
            user_features[col] = np.nan
        
        return user_features

    def calculate_engagement_score(self, user_features):
        """
        Calculate the engagement score as the Euclidean distance from the user's features 
        to the least engaged cluster centroid.
        
        Parameters:
        - user_features: Feature vector representing the user's engagement data.
        
        Returns:
        - Euclidean distance (engagement score).
        """
        # Ensure the features match the centroid's length
        required_columns = ['Total DL (Bytes)', 'Total UL (Bytes)', 'Dur. (ms)']
        valid_features = self._validate_columns(user_features, required_columns)
        
        # Ensure that the number of columns matches the centroid
        valid_features = valid_features[required_columns].values  # Convert to numpy array
        return np.linalg.norm(valid_features - self.least_engaged_centroid[:len(valid_features)])

    def calculate_experience_score(self, user_features):
        """
        Calculate the experience score as the Euclidean distance from the user's features 
        to the worst experience cluster centroid.
        
        Parameters:
        - user_features: Feature vector representing the user's experience data.
        
        Returns:
        - Euclidean distance (experience score).
        """
        required_columns = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']
        valid_features = self._validate_columns(user_features, required_columns)
        
        # Ensure that the number of columns matches the centroid
        valid_features = valid_features[required_columns].values  # Convert to numpy array
        return np.linalg.norm(valid_features - self.worst_experience_centroid[:len(valid_features)])

    def assign_scores_to_users(self):
        """
        Assign engagement and experience scores to each user in the dataset.
        
        Returns:
        - DataFrame with user engagement and experience scores.
        """
        # Select relevant columns for engagement and experience features
        engagement_features = self.user_data[['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)']]
        experience_features = self.user_data[['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']]
        
        # Calculate scores for each user based on engagement and experience features
        self.user_data['engagement_score'] = engagement_features.apply(
            lambda x: self.calculate_engagement_score(x), axis=1
        )
        self.user_data['experience_score'] = experience_features.apply(
            lambda x: self.calculate_experience_score(x), axis=1
        )
        
        return self.user_data
