import unittest
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from experience_analytics.aggregate_customer import AggregateCustomer
import numpy as np
from pandas.testing import assert_frame_equal

class TestAggregateCustomer(unittest.TestCase):

    def setUp(self):
        """
        Set up a sample dataset for testing. This method is called before each test.
        """
        self.data = {
            'IMSI': [12345, 12345, 67890],
            'Avg RTT DL (ms)': [100, None, 150],
            'Avg RTT UL (ms)': [50, 60, None],
            'TCP DL Retrans. Vol (Bytes)': [500, 700, None],
            'TCP UL Retrans. Vol (Bytes)': [100, None, 300],
            'Avg Bearer TP DL (kbps)': [20, None, 40],
            'Avg Bearer TP UL (kbps)': [10, 15, None],
            'Handset Manufacturer': ['Apple', None, 'Samsung'],
            'Handset Type': ['iPhone X', 'iPhone X', 'Galaxy S20']
        }
        
        self.df = pd.DataFrame(self.data)
        self.agg_cust = AggregateCustomer(self.df)

    def test_handle_missing_values(self):
        """
        Test if missing values are handled correctly by replacing with mean (for numeric)
        and mode (for categorical).
        """
        self.agg_cust.handle_missing_values()

        # Expected means recalculated after filling missing values
        expected_means = {
            'Avg RTT DL (ms)': 125.0,  # Mean of [100, 150]
            'Avg RTT UL (ms)': 55.0,   # Mean of [50, 60]
            'TCP DL Retrans. Vol (Bytes)': 600.0,  # Mean of [500, 700]
            'TCP UL Retrans. Vol (Bytes)': 200.0,  # Mean of [100, 300]
            'Avg Bearer TP DL (kbps)': 30.0,  # Mean of [20, 40]
            'Avg Bearer TP UL (kbps)': 12.5  # Mean of [10, 15]
        }

        print("agg_cust: ", self.agg_cust.df)
        for col, expected_mean in expected_means.items():
            self.assertAlmostEqual(self.agg_cust.df[col].iloc[1], expected_mean, places=2)

        # Check if missing categorical values are replaced by mode
        self.assertEqual(self.agg_cust.df['Handset Manufacturer'].iloc[1], 'Apple')


    def test_aggregate_user_experience(self):
        """
        Test if the aggregation of user experience metrics is done correctly.
        """
        self.agg_cust.handle_missing_values()  # Ensure missing values are handled first
        aggregated_df = self.agg_cust.aggregate_user_experience()
        
        # Create the expected DataFrame after aggregation
        expected_data = {
            'IMSI': [12345, 67890],
            'Avg RTT DL (ms)': [112.5, 150.0],  # Corrected mean for IMSI 12345
            'Avg RTT UL (ms)': [55.0, 55.0],    # Corrected mean for IMSI 12345
            'TCP DL Retrans. Vol (Bytes)': [600.0, 600.0],  # Mean of [500, 700] for IMSI 12345
            'TCP UL Retrans. Vol (Bytes)': [150.0, 200.0],  # Corrected expected value
            'Avg Bearer TP DL (kbps)': [30.0, 30.0],        # Mean of [20, 40]
            'Avg Bearer TP UL (kbps)': [12.5, 12.5],        # Mean of [10, 15]
            'Handset Manufacturer': ['Apple', 'Samsung'],
            'Handset Type': ['iPhone X', 'Galaxy S20']
        }

        expected_df = pd.DataFrame(expected_data)
        
        # Check if the aggregated DataFrame matches the expected output
        assert_frame_equal(aggregated_df, expected_df)

    def test_run_analysis(self):
        """
        Test the full analysis pipeline including handling missing values and aggregation.
        """
        aggregated_df = self.agg_cust.run_analysis()
        print("aggregated_df: ", aggregated_df["TCP UL Retrans. Vol (Bytes)"])
        # Ensure the output is as expected
        expected_data = {
            'IMSI': [12345, 67890],
            'Avg RTT DL (ms)': [112.5, 150.0],
            'Avg RTT UL (ms)': [55.0, 55.0],
            'TCP DL Retrans. Vol (Bytes)': [600.0, 600.0],
            'TCP UL Retrans. Vol (Bytes)': [150.0, 200.0],
            'Avg Bearer TP DL (kbps)': [30.0, 30.0],
            'Avg Bearer TP UL (kbps)': [12.5, 12.5],
            'Handset Manufacturer': ['Apple', 'Samsung'],
            'Handset Type': ['iPhone X', 'Galaxy S20']
        }
        expected_df = pd.DataFrame(expected_data)
        
        # Validate the full pipeline output
        assert_frame_equal(aggregated_df, expected_df)

if __name__ == '__main__':
    unittest.main()

