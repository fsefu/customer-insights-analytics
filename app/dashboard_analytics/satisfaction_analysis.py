import streamlit as st
import pandas as pd

import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from experience_analytics.experience_clustering import ExperienceClustering
from engagement_analysis.telecom_engagement_analysis import TelecomEngagementAnalysis
from satisfaction_analysis.engagement_experience_scores import EngagementExperienceScores
from satisfaction_analysis.top_satifactions_analysis import TopSatisfactionAnalysis
from satisfaction_analysis.satisfaction_score_predictor import SatisfactionScorePredictor
from satisfaction_analysis.satisfaction_kmeans import SatisfactionKMeans
from satisfaction_analysis.cluster_score_aggregator import ClusterScoreAggregator

class SatisfactionAnalytics:
    def __init__(self, df):
        self.df = df

    def display(self):
        st.subheader("Satisfaction Analytics")
        
        # Run engagement and experience analysis
        engagement_analysis = TelecomEngagementAnalysis(self.df)
        engagement_data = engagement_analysis.aggregate_metrics_by_customer()
        normalized_data = engagement_analysis.normalize_metrics()
        engagement_data_with_clusters = engagement_analysis.k_means_clustering(n_clusters=3)

        experience_clustering = ExperienceClustering(df=self.df)
        experience_clustering.run()
        experience_data = experience_clustering.df[['MSISDN/Number', 'Cluster']]
        experience_data.rename(columns={'Cluster': 'experience_cluster'}, inplace=True)

        # Merge engagement and experience data
        user_df = pd.merge(engagement_data_with_clusters, experience_data, on='MSISDN/Number', how='inner')

        # Satisfaction Score Analysis
        engagement_clusters = engagement_analysis.kmeans
        experience_clusters = experience_clustering.kmeans
        satisfaction_analysis = EngagementExperienceScores(
            user_data=user_df,
            engagement_clusters=engagement_clusters,
            experience_clusters=experience_clusters
        )
        user_scores_df = satisfaction_analysis.assign_scores_to_users()

        st.write("### Engagement and Experience Scores")
        st.dataframe(user_scores_df.head())

        # Top satisfaction analysis
        top_satisfaction_analysis = TopSatisfactionAnalysis(
            user_data=user_df,
            engagement_clusters=engagement_clusters,
            experience_clusters=experience_clusters
        )
        top_satisfied_customers = top_satisfaction_analysis.top_n_satisfied_customers(n=10)
        st.write("### Top 10 Satisfied Customers")
        st.dataframe(top_satisfied_customers)

        st.write("### Satisfaction Score Prediction")
        satisfaction_predictor = SatisfactionScorePredictor(user_data=user_scores_df)
        satisfaction_predictor.build_regression_model()
        predicted_satisfaction = satisfaction_predictor.predict_satisfaction(engagement_score=50, experience_score=45)
        st.write(f"Predicted Satisfaction Score for Engagement=50, Experience=45: {predicted_satisfaction:.2f}")

        # K-Means Analysis
        kmeans_analysis = SatisfactionKMeans(data=user_scores_df)
        kmeans_analysis.preprocess_data()
        clustered_data = kmeans_analysis.run_kmeans(k=2)
        st.write("### Satisfaction K-Means Clustering")
        st.dataframe(clustered_data.head())

        # Cluster Score Aggregation
        score_aggregator = ClusterScoreAggregator(user_data=clustered_data)
        st.write("### Cluster Score Aggregation")
        score_aggregator.plot_cluster_scores()
