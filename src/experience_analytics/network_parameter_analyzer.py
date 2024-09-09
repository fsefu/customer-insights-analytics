import pandas as pd

class NetworkParameterAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """Initialize with a pandas DataFrame."""
        self.df = df

    def _get_top_bottom_frequent(self, column: str, n: int = 10):
        """
        Compute the top, bottom, and most frequent values for a given column.
        
        Args:
            column (str): The column name for which to compute values.
            n (int): Number of top/bottom/frequent values to return.
            
        Returns:
            dict: Dictionary with top, bottom, and most frequent values.
        """
        # Drop missing values for the column
        valid_data = self.df[column].dropna()

        # Compute top n values
        top_n = valid_data.nlargest(n).values

        # Compute bottom n values
        bottom_n = valid_data.nsmallest(n).values

        # Compute most frequent n values
        most_frequent = valid_data.value_counts().nlargest(n).index.values

        return {
            "top_n": top_n,
            "bottom_n": bottom_n,
            "most_frequent": most_frequent
        }

    def compute_tcp_stats(self):
        """Compute top, bottom, and most frequent values for TCP retransmission (DL + UL)."""
        # Combine TCP DL and UL retransmission volumes
        self.df['TCP_Retransmission'] = self.df['TCP DL Retrans. Vol (Bytes)'] + self.df['TCP UL Retrans. Vol (Bytes)']
        return self._get_top_bottom_frequent('TCP_Retransmission')

    def compute_rtt_stats(self):
        """Compute top, bottom, and most frequent values for RTT (DL + UL)."""
        # Combine RTT DL and UL
        self.df['RTT'] = self.df['Avg RTT DL (ms)'] + self.df['Avg RTT UL (ms)']
        return self._get_top_bottom_frequent('RTT')

    def compute_throughput_stats(self):
        """Compute top, bottom, and most frequent values for Throughput (DL + UL)."""
        # Combine Throughput DL and UL
        self.df['Throughput'] = self.df['Avg Bearer TP DL (kbps)'] + self.df['Avg Bearer TP UL (kbps)']
        return self._get_top_bottom_frequent('Throughput')

    def print_stats(self, metric_name: str, stats: dict):
        """Prints out the computed stats for a given metric."""
        print(f"\n{metric_name} Stats:")
        print(f"Top 10: {stats['top_n']}")
        print(f"Bottom 10: {stats['bottom_n']}")
        print(f"Most Frequent 10: {stats['most_frequent']}")

# Sample usage:
# df = pd.read_csv("your_data.csv")
# analyzer = NetworkParameterAnalyzer(df)
# tcp_stats = analyzer.compute_tcp_stats()
# analyzer.print_stats("TCP Retransmission", tcp_stats)
