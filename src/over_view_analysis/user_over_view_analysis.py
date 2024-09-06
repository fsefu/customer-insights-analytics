# User Overview Analysis Class
class UserOverviewAnalysis:
    def __init__(self, df):
        self.df = df

    def aggregate_user_data(self):
        """Aggregate data per user (MSISDN/Number) based on the given requirements."""
        # Group by MSISDN/Number (user ID)
        aggregated_data = self.df.groupby('MSISDN/Number').agg(
            num_sessions=('Bearer Id', 'nunique'),  # Number of xDR sessions
            total_duration=('Dur. (ms)', 'sum'),    # Total session duration
            total_dl_data=('Total DL (Bytes)', 'sum'),  # Total download data
            total_ul_data=('Total UL (Bytes)', 'sum'),  # Total upload data
            youtube_dl=('Youtube DL (Bytes)', 'sum'),  # Total YouTube download
            youtube_ul=('Youtube UL (Bytes)', 'sum'),  # Total YouTube upload
            netflix_dl=('Netflix DL (Bytes)', 'sum'),  # Total Netflix download
            netflix_ul=('Netflix UL (Bytes)', 'sum'),  # Total Netflix upload
            gaming_dl=('Gaming DL (Bytes)', 'sum'),    # Total Gaming download
            gaming_ul=('Gaming UL (Bytes)', 'sum')     # Total Gaming upload
        ).reset_index()

        # Calculate total data volume per user
        aggregated_data['total_data_volume'] = aggregated_data['total_dl_data'] + aggregated_data['total_ul_data']

        return aggregated_data
