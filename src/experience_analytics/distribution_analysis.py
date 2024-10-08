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
    
    def plot_distribution(self, df, x_col, y_col, title, y_label, palette="coolwarm"):
        """
        Plots the distribution of a given column per handset type with enhanced aesthetics.
        :param df: DataFrame containing the data to plot.
        :param x_col: The column to be plotted on the x-axis.
        :param y_col: The column to be plotted on the y-axis.
        :param title: Title of the plot.
        :param y_label: Label for the y-axis.
        :param palette: Seaborn color palette to use for the plot.
        """
        plt.figure(figsize=(12, 6))
        
        # Set Seaborn style and plot using a custom palette
        sns.set_style("whitegrid")
        ax = sns.barplot(x=x_col, y=y_col, data=df, palette=palette)
        
        # Add titles and labels
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_label, fontsize=12)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha="right", fontsize=10)
        
        # Add data labels on top of the bars
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.1f}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='center', 
                        xytext=(0, 9), textcoords='offset points', fontsize=10)
        
        # Display the plot
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """
        Generates the full report by computing metrics and displaying enhanced plots.
        """
        # Compute average throughput per handset type
        avg_throughput = self.compute_average_throughput()
        print("Average Throughput per Handset Type:")
        print(avg_throughput)
        
        # Plot average throughput distribution with improved visualization
        self.plot_distribution(avg_throughput, 'Handset Type', 'Avg Bearer TP DL (kbps)', 
                               'Average DL Throughput per Handset Type', 
                               'Avg Bearer TP DL (kbps)', palette="Blues_d")
        self.plot_distribution(avg_throughput, 'Handset Type', 'Avg Bearer TP UL (kbps)', 
                               'Average UL Throughput per Handset Type', 
                               'Avg Bearer TP UL (kbps)', palette="Greens_d")

        # Compute average TCP retransmission per handset type
        avg_tcp_retrans = self.compute_average_tcp_retrans()
        print("Average TCP Retransmission per Handset Type:")
        print(avg_tcp_retrans)
        
        # Plot average TCP retransmission distribution with enhanced visuals
        self.plot_distribution(avg_tcp_retrans, 'Handset Type', 'TCP DL Retrans. Vol (Bytes)', 
                               'Average DL TCP Retransmission per Handset Type', 
                               'TCP DL Retrans. Vol (Bytes)', palette="Reds_d")
        self.plot_distribution(avg_tcp_retrans, 'Handset Type', 'TCP UL Retrans. Vol (Bytes)', 
                               'Average UL TCP Retransmission per Handset Type', 
                               'TCP UL Retrans. Vol (Bytes)', palette="Oranges_d")


# Example usage (assuming 'data' is your pandas DataFrame):
# telecom_analysis = DistributionAnalysis(data)
# telecom_analysis.generate_report()
