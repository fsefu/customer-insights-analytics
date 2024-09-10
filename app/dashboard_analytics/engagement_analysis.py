import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from engagement_analysis.user_engagement_analysis import UserEngagementAnalysis
from engagement_analysis.telecom_engagement_analysis import TelecomEngagementAnalysis

class EngagementAnalytics:
    def __init__(self, df):
        self.df = df

    def display(self):
        # User engagement analysis
        user_engagement = UserEngagementAnalysis(self.df)
        engagement_metrics = user_engagement.aggregate_user_metrics()

        st.subheader("Engagement Analytics")

        st.write("### Aggregated User Metrics")
        st.dataframe(engagement_metrics.head())

        st.write("### Top 5 Customers by Total Traffic")
        top_customers = user_engagement.top_customers_by_engagement(metric='total_traffic', top_n=5)
        st.dataframe(top_customers)

        st.write("### Aggregated Metrics Plot")
        st.pyplot(user_engagement.plot_aggregated_metrics())

        # Telecom engagement analysis
        telecom_engagement = TelecomEngagementAnalysis(self.df)
        agg_data = telecom_engagement.aggregate_metrics_by_customer()

        st.write("### Aggregated Metrics by Customer")
        st.dataframe(agg_data.head())

        st.write("### Top 10 Users by Application Traffic (YouTube)")
        top_users_youtube = telecom_engagement.top_users_by_application('Youtube DL (Bytes)', top_n=10)
        st.dataframe(top_users_youtube)

        st.write("### Top 3 Most Used Applications")
        st.pyplot(telecom_engagement.plot_top_applications(top_n=3))
