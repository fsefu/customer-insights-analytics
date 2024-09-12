

from satisfaction_analysis.engagement_experience_scores import EngagementExperienceScores
import matplotlib.pyplot as plt
import seaborn as sns

class TopSatisfactionAnalysis(EngagementExperienceScores):
    def __init__(self, user_data, engagement_clusters, experience_clusters):
        """
        Initialize the SatisfactionAnalysis class by extending EngagementExperienceScores.
        
        Parameters:
        - user_data: DataFrame containing user data for analysis.
        - engagement_clusters: Clustering model for user engagement.
        - experience_clusters: Clustering model for user experience.
        """
        super().__init__(user_data, engagement_clusters, experience_clusters)

    def calculate_satisfaction_score(self):
        """
        Calculate the satisfaction score as the average of engagement and experience scores for each user.
        
        Returns:
        - DataFrame with an additional column 'satisfaction_score'.
        """
        # Ensure engagement and experience scores are assigned
        self.user_data = self.assign_scores_to_users()
        
        # Calculate satisfaction score as the mean of engagement and experience scores
        self.user_data['satisfaction_score'] = self.user_data[['engagement_score', 'experience_score']].mean(axis=1)
        
        return self.user_data

    def top_n_satisfied_customers(self, n=10):
        """
        Retrieve the top N satisfied customers based on the satisfaction score.
        
        Parameters:
        - n: Number of top satisfied customers to retrieve (default is 10).
        
        Returns:
        - DataFrame containing the top N satisfied customers.
        """
        # Calculate satisfaction scores
        satisfied_customers = self.calculate_satisfaction_score()
        
        # Sort users by satisfaction score in descending order
        top_customers = satisfied_customers.sort_values(by='satisfaction_score', ascending=False).head(n)
        
        return top_customers[['MSISDN/Number', 'satisfaction_score']]
    def satisfied_customers(self):
        """
        Retrieve the top N satisfied customers based on the satisfaction score.
        
        Parameters:
        - n: Number of top satisfied customers to retrieve (default is 10).
        
        Returns:
        - DataFrame containing the top N satisfied customers.
        """
        # Calculate satisfaction scores
        satisfied_customers = self.calculate_satisfaction_score()
        
   
        return satisfied_customers[['MSISDN/Number', 'satisfaction_score']]

    def visualize_top_satisfaction(self, user_scores_df):
        """
        Visualize the satisfaction scores and top satisfied customers.

        Parameters:
        - user_scores_df: DataFrame containing user engagement, experience, and satisfaction scores.
        """
        # Calculate the satisfaction score
        user_scores_df['satisfaction_score'] = (user_scores_df['engagement_score'] + user_scores_df['experience_score']) / 2
        
        # 1. Distribution of satisfaction scores
        plt.figure(figsize=(10, 6))
        sns.histplot(user_scores_df['satisfaction_score'], kde=True, bins=30, color='blue')
        plt.title('Distribution of Satisfaction Scores', fontsize=16)
        plt.xlabel('Satisfaction Score', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.grid(True)
        plt.show()
        
        # 2. Top 10 satisfied customers
        top_10_customers = user_scores_df.nlargest(10, 'satisfaction_score')
        plt.figure(figsize=(10, 6))
        sns.barplot(x='MSISDN/Number', y='satisfaction_score', data=top_10_customers, palette='viridis')
        plt.title('Top 10 Satisfied Customers', fontsize=16)
        plt.xlabel('Customer (MSISDN/Number)', fontsize=14)
        plt.ylabel('Satisfaction Score', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        # 3. Scatter plot of engagement vs experience scores
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='engagement_score', y='experience_score', data=user_scores_df, hue='satisfaction_score', palette='coolwarm')
        plt.title('Engagement Score vs Experience Score', fontsize=16)
        plt.xlabel('Engagement Score', fontsize=14)
        plt.ylabel('Experience Score', fontsize=14)
        plt.colorbar(label='Satisfaction Score')
        plt.grid(True)
        plt.show()


# # Example usage:
# # Assuming you have already initialized engagement and experience clusters and merged data

# satisfaction_analysis = SatisfactionAnalysis(
#     user_data=user_df,
#     engagement_clusters=engagement_clusters,
#     experience_clusters=experience_clusters
# )

# # Calculate satisfaction scores and get top 10 satisfied customers
# top_satisfied_customers = satisfaction_analysis.top_n_satisfied_customers(n=10)

# # Display top satisfied customers
# print(top_satisfied_customers)
