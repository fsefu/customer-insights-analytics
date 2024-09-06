import pandas as pd
import numpy as np

# Data Cleaner Class
class DataCleaner:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        """Clean the dataset by handling missing values and duplicates."""
        # Remove rows with missing MSISDN/Number or Bearer Id (key identifiers)
        self.df = self.df.dropna(subset=['MSISDN/Number', 'Bearer Id'])
        
        # Convert Start and End columns to datetime format using .loc to avoid SettingWithCopyWarning
        self.df.loc[:, 'Start'] = pd.to_datetime(self.df['Start'], errors='coerce')
        self.df.loc[:, 'End'] = pd.to_datetime(self.df['End'], errors='coerce')

        # Drop rows where Start or End time conversion fails
        self.df = self.df.dropna(subset=['Start', 'End'])

        # Handle any other missing values (e.g., replace with 0 for numeric fields)
        numeric_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(0)

        return self.df
    def convert_units_to_mb(self):
        """
        Convert all columns with data in bytes or kilobytes to megabytes.
        """
        # List of column suffixes that need to be converted
        columns_in_bytes = [col for col in self.df.columns if '(Bytes)' in col]
        columns_in_kb = [col for col in self.df.columns if '(kbps)' in col or '(Kbps)' in col]
        print("columns_in_bytes: ", columns_in_bytes)
        print("columns_in_kb: ", columns_in_kb)

        # Convert Bytes to MB (1 MB = 1,000,000 Bytes)
        self.df[columns_in_bytes] = self.df[columns_in_bytes].apply(lambda x: x / 1_000_000)

        # Convert kbps to MB (1 kbps = 1/8 MBps, and assuming duration is in seconds)
        self.df[columns_in_kb] = self.df[columns_in_kb].apply(lambda x: (x / 8) / 1_000)

        print("Unit conversion complete: Bytes and kbps columns converted to MB.")
        return self.df

    def handle_missing_and_outliers(self):
        """
        Identify and treat missing values & outliers by replacing with mean for numeric columns.
        """
        # Ensure the operation is done only for numeric columns
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Handle missing values by replacing with the mean of each column
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        
        # Cap outliers: values greater than the 99th percentile are replaced by the column's mean
        self.df[numeric_cols] = self.df[numeric_cols].apply(
            lambda x: np.where(x > x.quantile(0.99), x.mean(), x)
        )

        print("Missing values and outliers treated.")
        return self.df
