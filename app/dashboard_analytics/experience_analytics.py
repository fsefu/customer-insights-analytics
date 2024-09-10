import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from experience_analytics.aggregate_customer import AggregateCustomer
from experience_analytics.network_parameter_analyzer import NetworkParameterAnalyzer
from experience_analytics.distribution_analysis import DistributionAnalysis
from experience_analytics.experience_clustering import ExperienceClustering

class ExperienceAnalytics:
    def __init__(self, df):
        self.df = df

    def display(self):
        # Aggregate data per customer
        aggregate_customer = AggregateCustomer(self.df)
        customer_data = aggregate_customer.run_analysis()

        # Network parameter analysis
        analyzer = NetworkParameterAnalyzer(self.df)
        tcp_stats = analyzer.compute_tcp_stats()

        # Distribution analysis
        distribution_analysis = DistributionAnalysis(self.df)
        distribution_report = distribution_analysis.generate_report()

        # Clustering analysis
        clustering = ExperienceClustering(self.df)
        clustering.run()

        st.subheader("Experience Analytics")

        st.write("### Aggregated Customer Data")
        st.dataframe(customer_data.head())

        st.write("### TCP Retransmission Stats")
        st.dataframe(tcp_stats)

        st.write("### Distribution Analysis Report")
        st.dataframe(distribution_report)

        st.write("### Clustering Analysis")
        st.text("Clustering results have been generated.")
