import pandas as pd

class DataToExport:
    def __init__(self, satisfied_customers: pd.DataFrame, clustered_data: pd.DataFrame):
        """
        Initializes the DataMerger with two dataframes.

        :param satisfied_customers: DataFrame with columns ['MSISDN/Number', 'satisfaction_score']
        :param clustered_data: DataFrame with columns ['MSISDN/Number', 'engagement_score', 'experience_score']
        """
        self.satisfied_customers = satisfied_customers
        self.clustered_data = clustered_data

    def merge_data(self) -> pd.DataFrame:
        """
        Merges the two dataframes on 'MSISDN/Number'.

        :return: Merged DataFrame with columns ['user_id', 'engagement_score', 'experience_score', 'satisfaction_score']
        """
        # Merging the dataframes on 'MSISDN/Number'
        merged_df = pd.merge(self.clustered_data, self.satisfied_customers, on='MSISDN/Number', how='inner')
        
        # Renaming columns to match the required format
        merged_df = merged_df.rename(columns={
            'MSISDN/Number': 'user_id',
            'satisfaction_score': 'satisfaction_score'
        })

        return merged_df[['user_id', 'engagement_score', 'experience_score', 'satisfaction_score']]
