import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class DistributionAnalysis:
    def __init__(self, data):
        """
        Initializes the TelecomAnalysis class with the dataset.
        :param data: DataFrame containing the telecom data.
        """
        self.data = data
    
    def compute_average_throughput(self):
        """
        Computes the average throughput (DL and UL) per handset type.
        :return: DataFrame with handset type and average throughput values.
        """
        # Group by Handset Type and calculate average throughput
        avg_throughput = self.data.groupby('Handset Type').agg({
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean'
        }).reset_index()
        
        return avg_throughput
    
    def compute_average_tcp_retrans(self):
        """
        Computes the average TCP retransmission (DL and UL) per handset type.
        :return: DataFrame with handset type and average TCP retransmission values.
        """
        # Group by Handset Type and calculate average TCP retransmission
        avg_tcp_retrans = self.data.groupby('Handset Type').agg({
            'TCP DL Retrans. Vol (Bytes)': 'mean',
            'TCP UL Retrans. Vol (Bytes)': 'mean'
        }).reset_index()
        
        return avg_tcp_retrans
    
    def plot_distribution(self, df, x_col, y_col, title):
        """
        Plots the distribution of a given column per handset type.
        :param df: DataFrame containing the data to plot.
        :param x_col: The column to be plotted on the x-axis.
        :param y_col: The column to be plotted on the y-axis.
        :param title: Title of the plot.
        """
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x_col, y=y_col, data=df)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.show()
    
    def generate_report(self):
        """
        Generates the full report by computing metrics and displaying plots.
        """
        # Compute average throughput per handset type
        avg_throughput = self.compute_average_throughput()
        print("Average Throughput per Handset Type:")
        print(avg_throughput)
        
        # Plot average throughput distribution
        self.plot_distribution(avg_throughput, 'Handset Type', 'Avg Bearer TP DL (kbps)', 
                               'Average DL Throughput per Handset Type')
        self.plot_distribution(avg_throughput, 'Handset Type', 'Avg Bearer TP UL (kbps)', 
                               'Average UL Throughput per Handset Type')

        # Compute average TCP retransmission per handset type
        avg_tcp_retrans = self.compute_average_tcp_retrans()
        print("Average TCP Retransmission per Handset Type:")
        print(avg_tcp_retrans)
        
        # Plot average TCP retransmission distribution
        self.plot_distribution(avg_tcp_retrans, 'Handset Type', 'TCP DL Retrans. Vol (Bytes)', 
                               'Average DL TCP Retransmission per Handset Type')
        self.plot_distribution(avg_tcp_retrans, 'Handset Type', 'TCP UL Retrans. Vol (Bytes)', 
                               'Average UL TCP Retransmission per Handset Type')


# Assuming 'data' is your pandas DataFrame loaded with the telecommunication dataset
# For example:
# data = pd.read_csv('path_to_your_csv_file.csv')

# Instantiate the class and generate the report
# telecom_analysis = TelecomAnalysis(data)
# telecom_analysis.generate_report()
