import pandas as pd
import numpy as np

class AggregateCustomer:
    def __init__(self, df):
        self.df = df
    def handle_missing_values(self):
        """
        Handles missing values by replacing them with the mean for numeric columns
        and the mode for categorical columns.
        """
        numeric_cols = [
            'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 
            'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
            'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)'
        ]
        categorical_cols = ['Handset Manufacturer', 'Handset Type']

        # Replace missing values in numeric columns with the mean
        for col in numeric_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mean())

        # Replace missing values in categorical columns with the mode (if there is at least one non-null value)
        for col in categorical_cols:
            if not self.df[col].isnull().all():
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

    def aggregate_user_experience(self):
        aggregation = {
            'Avg RTT DL (ms)': 'mean',
            'Avg RTT UL (ms)': 'mean',
            'TCP DL Retrans. Vol (Bytes)': 'mean',
            'TCP UL Retrans. Vol (Bytes)': 'mean',
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'Handset Manufacturer': 'first',
            'Handset Type': 'first'
        }

        aggregated_df = self.df.groupby('IMSI').agg(aggregation).reset_index()
        return aggregated_df

    def run_analysis(self):
        self.handle_missing_values()
        return self.aggregate_user_experience()
f