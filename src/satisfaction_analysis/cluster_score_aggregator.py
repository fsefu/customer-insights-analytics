import pandas as pd
import matplotlib.pyplot as plt

class ClusterScoreAggregator:
    def __init__(self, user_data, cluster_column='cluster'):
        """
        Initialize the ClusterScoreAggregator class with user data and cluster column.
        
        Parameters:
        - user_data: DataFrame containing user data with scores and cluster labels.
        - cluster_column: The column name that contains cluster labels.
        """
        self.user_data = user_data
        self.cluster_column = cluster_column
    
    def aggregate_scores(self):
        """
        Aggregate the average satisfaction and experience scores per cluster.
        
        Returns:
        - DataFrame with average scores per cluster.
        """
        # Check if required columns are present
        if not all(col in self.user_data.columns for col in ['satisfaction_score', 'experience_score', self.cluster_column]):
            raise ValueError("DataFrame must contain 'satisfaction_score', 'experience_score', and cluster column")
        
        # Aggregate average scores per cluster
        cluster_scores = self.user_data.groupby(self.cluster_column).agg(
            average_satisfaction_score=('satisfaction_score', 'mean'),
            average_experience_score=('experience_score', 'mean')
        ).reset_index()
        
        return cluster_scores
    
    def plot_cluster_scores(self):
        """
        Plot the average satisfaction and experience scores per cluster.
        """
        # Aggregate scores
        cluster_scores_df = self.aggregate_scores()
        
        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))
        cluster_scores_df.plot(kind='bar', x=self.cluster_column, ax=ax, color=['#1f77b4', '#ff7f0e'])
        
        ax.set_title('Average Satisfaction and Experience Scores per Cluster')
        ax.set_xlabel('Cluster')
        ax.set_ylabel('Average Score')
        ax.legend(['Satisfaction Score', 'Experience Score'])
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()
