import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))
from over_view_analysis.telecom_data_anlyzer import TelecomDataAnalyzer
from over_view_analysis.user_over_view_analysis import UserOverviewAnalysis

class UserOverview:
    def __init__(self, df):
        self.df = df

    def display(self):
        analyzer = TelecomDataAnalyzer(self.df)
        recommendations = analyzer.generate_recommendations()
        user_analysis = UserOverviewAnalysis(self.df)
        user_overview = user_analysis.aggregate_user_data()

        st.subheader("User Overview Analysis")
        st.write("### Top 10 Handsets")
        st.dataframe(recommendations['Top 10 Handsets'])
        st.pyplot(analyzer.plot_top_10_handsets())

        st.write("### Top 3 Manufacturers")
        st.dataframe(recommendations['Top 3 Manufacturers'])
        st.pyplot(analyzer.plot_top_3_manufacturers())

        st.write("### Top 5 Handsets per Manufacturer")
        st.dataframe(recommendations['Top 5 Handsets per Manufacturer'])
        st.pyplot(analyzer.plot_top_5_handsets_per_top_3_manufacturers())

        st.write("### Aggregated User Data")
        st.dataframe(user_overview)
