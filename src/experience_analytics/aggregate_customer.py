import pandas as pd
import numpy as np

class AggregateCustomer:
    def __init__(self, df):
        """
        Initialize with the dataset.
        Args:
        - df: DataFrame containing the telecommunication data.
        """
        self.df = df
    
    def handle_missing_values(self):
        """
        Handles missing values by replacing them with the mean for numeric columns
        and the mode for categorical columns.
        """
        # Numeric columns related to experience metrics
        numeric_cols = [
            'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 
            'TCP DL Retrans. Vol (Bytes)', 'TCP UL Retrans. Vol (Bytes)', 
            'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)'
        ]
        # Categorical columns
        categorical_cols = ['Handset Manufacturer', 'Handset Type']
        
        # Replace missing values in numeric columns with the mean
        for col in numeric_cols:
            self.df[col].fillna(self.df[col].mean(), inplace=True)
        
        # Replace missing values in categorical columns with the mode
        for col in categorical_cols:
            self.df[col].fillna(self.df[col].mode()[0], inplace=True)

    def aggregate_user_experience(self):
        """
        Aggregate per customer the average values for TCP retransmission, RTT, and throughput.
        """
        # Define aggregation logic for customer-level experience metrics
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
        
        # Assuming Customer ID is represented by 'IMSI' or 'MSISDN/Number'
        aggregated_df = self.df.groupby('IMSI').agg(aggregation).reset_index()
        return aggregated_df

    def run_analysis(self):
        """
        Perform the full user experience analysis by handling missing data, outliers,
        and aggregating the required metrics.
        """
        self.handle_missing_values()  # Step 1: Handle missing values
        return self.aggregate_user_experience()  # Step 2: Aggregate metrics


# # Example usage:
# if __name__ == "__main__":
#     # Assuming df is a pandas DataFrame loaded from the actual data
#     data_path = '/mnt/data/sample_data.csv'  # Replace with your actual data file path
#     df = pd.read_csv(data_path)
    
#     analysis = UserExperienceAnalysis(df)
#     aggregated_data = analysis.run_analysis()
#     print(aggregated_data)
