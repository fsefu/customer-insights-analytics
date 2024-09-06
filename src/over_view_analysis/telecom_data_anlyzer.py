import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class TelecomDataAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
        self.clean_data()

    def clean_data(self):
        # Handle missing values and 'undefined' in 'Handset Type'
        self.df['Handset Type'] = self.df['Handset Type'].fillna('Unknown')
        self.df['Handset Type'] = self.df['Handset Type'].replace('undefined', 'Unknown')

    def get_top_10_handsets(self):
        # Exclude 'Unknown' values from the count
        top_10_handsets = self.df[self.df['Handset Type'] != 'Unknown']['Handset Type'].value_counts().head(10)
        return top_10_handsets
    def plot_top_10_handsets(self):
        top_10_handsets = self.get_top_10_handsets()
        # Plot a bar chart
        top_10_handsets.plot(kind='bar', color='skyblue', figsize=(10, 6))
        plt.title('Top 10 Handsets by Frequency of Use')
        plt.xlabel('Handset Type')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    def plot_top_10_handsets(self):
        top_10_handsets = self.get_top_10_handsets()
        # Plot a bar chart
        top_10_handsets.plot(kind='bar', color='skyblue', figsize=(10, 6))
        plt.title('Top 10 Handsets by Frequency of Use')
        plt.xlabel('Handset Type')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    
    def get_top_3_manufacturers(self):
        # Counting occurrences of each handset manufacturer
        top_3_manufacturers = self.df['Handset Manufacturer'].value_counts().head(3)
        return top_3_manufacturers
    
    def plot_top_3_manufacturers(self):
        # Plot bar chart for top 3 manufacturers
        top_3_manufacturers = self.get_top_3_manufacturers()
        top_3_manufacturers.plot(kind='bar', color='lightgreen', figsize=(8, 5))
        plt.title('Top 3 Handset Manufacturers by Frequency')
        plt.xlabel('Manufacturer')
        plt.ylabel('Frequency')
        plt.xticks(rotation=0, ha='center')
        plt.tight_layout()
        plt.show()

    def get_top_5_handsets_per_top_3_manufacturers(self):
        # Getting the top 3 manufacturers
        top_3_manufacturers = self.get_top_3_manufacturers().index
        top_5_handsets = {}

        for manufacturer in top_3_manufacturers:
            # Filtering data for each manufacturer
            manufacturer_data = self.df[self.df['Handset Manufacturer'] == manufacturer]
            # Counting occurrences of each handset type
            top_5_handsets[manufacturer] = manufacturer_data['Handset Type'].value_counts().head(5)

        return top_5_handsets

    def plot_top_5_handsets_per_top_3_manufacturers(self):
        # Get data for top 5 handsets per top 3 manufacturers
        top_5_handsets = self.get_top_5_handsets_per_top_3_manufacturers()
        
        # Create a list of all unique handsets in top 5 per manufacturer
        handsets = list(set([handset for handsets_list in top_5_handsets.values() for handset in handsets_list.index]))
        
        # Create a figure and axis for plotting
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Bar width for each manufacturer
        bar_width = 0.25
        # Bar positions on the x-axis
        indices = np.arange(len(handsets))
        
        # Plot each manufacturer's top 5 handsets
        for i, (manufacturer, handsets_count) in enumerate(top_5_handsets.items()):
            # Align bars with an offset for each manufacturer
            bar_positions = indices + i * bar_width
            ax.bar(bar_positions, [handsets_count.get(handset, 0) for handset in handsets], 
                   width=bar_width, label=manufacturer)
        
        # Add title and labels
        ax.set_title('Top 5 Handsets Per Top 3 Manufacturers')
        ax.set_xlabel('Handset Type')
        ax.set_ylabel('Frequency')
        ax.set_xticks(indices + bar_width)
        ax.set_xticklabels(handsets, rotation=45, ha='right')
        
        # Add legend
        ax.legend(title='Manufacturer')

        # Improve layout
        plt.tight_layout()
        plt.show()

    def generate_recommendations(self):
        # Fetch top handsets and manufacturers
        top_10_handsets = self.get_top_10_handsets()
        top_3_manufacturers = self.get_top_3_manufacturers()
        top_5_handsets_per_manufacturer = self.get_top_5_handsets_per_top_3_manufacturers()

        # Recommendations based on top 10 handsets
        if not top_10_handsets.empty:
            handsets_recommendation = "Consider launching device-specific promotions for popular models such as {}.".format(
                ', '.join(top_10_handsets.index[:3])
            )
        else:
            handsets_recommendation = "No popular handsets were found in the data."

        # Recommendations based on top 3 manufacturers
        if not top_3_manufacturers.empty:
            manufacturers_recommendation = "The top manufacturers are {}. Partnering with these companies could be beneficial for targeted promotions.".format(
                ', '.join(top_3_manufacturers.index)
            )
        else:
            manufacturers_recommendation = "No dominant handset manufacturers were identified."

        # Recommendations based on top 5 handsets per manufacturer
        manufacturer_handsets_recommendations = []
        for manufacturer, handsets in top_5_handsets_per_manufacturer.items():
            recommendation = "For {}, consider marketing or bundling offers for the following top handsets: {}.".format(
                manufacturer, ', '.join(handsets.index)
            )
            manufacturer_handsets_recommendations.append(recommendation)
        
        manufacturer_handsets_recommendation = '\n'.join(manufacturer_handsets_recommendations) if manufacturer_handsets_recommendations else "No specific handset recommendations for manufacturers."

        # Final recommendation
        recommendations = {
            'Top 10 Handsets': top_10_handsets,
            'Top 3 Manufacturers': top_3_manufacturers,
            'Top 5 Handsets per Manufacturer': top_5_handsets_per_manufacturer,
            'Marketing Recommendations': {
                'Handset Promotion Strategy': handsets_recommendation,
                'Manufacturer Partnership Strategy': manufacturers_recommendation,
                'Handset-Specific Recommendations': manufacturer_handsets_recommendation
            }
        }

        return recommendations



    def calculate_total_usage(self):
        """
        Calculate total upload and download data for each application
        and add them as new columns in the DataFrame.
        """
        self.df['Total Social Media Data (Bytes)'] = self.df['Social Media DL (Bytes)'] + self.df['Social Media UL (Bytes)']
        self.df['Total Google Data (Bytes)'] = self.df['Google DL (Bytes)'] + self.df['Google UL (Bytes)']
        self.df['Total YouTube Data (Bytes)'] = self.df['Youtube DL (Bytes)'] + self.df['Youtube UL (Bytes)']
        self.df['Total Netflix Data (Bytes)'] = self.df['Netflix DL (Bytes)'] + self.df['Netflix UL (Bytes)']
        self.df['Total Gaming Data (Bytes)'] = self.df['Gaming DL (Bytes)'] + self.df['Gaming UL (Bytes)']
        self.df['Total Other Data (Bytes)'] = self.df['Other DL (Bytes)'] + self.df['Other UL (Bytes)']

    def aggregate_data_by_user(self, user_identifier='IMSI'):
        """
        Group data by a user identifier (IMSI, MSISDN, etc.) and calculate the
        sum of data usage for each application.
        
        Args:
        user_identifier (str): The column name representing the user (e.g., IMSI, MSISDN)
        
        Returns:
        pd.DataFrame: Aggregated DataFrame sorted by YouTube data usage.
        """
        user_data_usage = self.df.groupby(user_identifier).agg({
            'Total Social Media Data (Bytes)': 'sum',
            'Total Google Data (Bytes)': 'sum',
            'Total YouTube Data (Bytes)': 'sum',
            'Total Netflix Data (Bytes)': 'sum',
            'Total Gaming Data (Bytes)': 'sum',
            'Total Other Data (Bytes)': 'sum'
        }).reset_index()

        # Sort by YouTube data usage as an example
        return user_data_usage.sort_values(by='Total YouTube Data (Bytes)', ascending=False)

    def aggregate_data_by_handset(self):
        """
        Group data by handset manufacturer and type, and calculate the
        sum of data usage for each application.

        Returns:
        pd.DataFrame: Aggregated DataFrame sorted by Netflix data usage.
        """
        handset_data_usage = self.df.groupby(['Handset Manufacturer', 'Handset Type']).agg({
            'Total YouTube Data (Bytes)': 'sum',
            'Total Netflix Data (Bytes)': 'sum',
            'Total Social Media Data (Bytes)': 'sum'
        }).reset_index()

        # Sort by Netflix data usage
        return handset_data_usage.sort_values(by='Total Netflix Data (Bytes)', ascending=False)

    def plot_top_users(self, user_data_usage, app_column='Total YouTube Data (Bytes)', top_n=5):
        """
        Plot the top N users by data consumption for a specific application.
        
        Args:
        user_data_usage (pd.DataFrame): The aggregated user data usage DataFrame.
        app_column (str): The application column to sort and visualize.
        top_n (int): Number of top users to visualize.
        """
        # Ensure the top_n is not larger than the actual number of users
        top_users = user_data_usage.nlargest(top_n, app_column)
        
        if top_users.empty:
            print("No data available to plot.")
            return
        
        # Sort top_users to have the highest values first (for better visualization)
        top_users = top_users.sort_values(by=app_column, ascending=False)
        
        # Plotting
        plt.figure(figsize=(10, 6))
        bars = plt.bar(top_users['IMSI'].astype(str), top_users[app_column], color='skyblue')

        # Add labels on top of the bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,.0f}', ha='center', va='bottom')
        
        plt.title(f'Top {top_n} Users by {app_column}', fontsize=14)
        plt.xlabel('User Identifier (IMSI)', fontsize=12)
        plt.ylabel(f'{app_column} (Bytes)', fontsize=12)
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
        plt.tight_layout()
        plt.show()

    def get_top_users(self, user_data_usage, app_column='Total YouTube Data (Bytes)', top_n=5):
        """
        Retrieve the top N users by data consumption for a specific application.
        
        Args:
        user_data_usage (pd.DataFrame): The aggregated user data usage DataFrame.
        app_column (str): The application column to sort and retrieve.
        top_n (int): Number of top users to return.
        
        Returns:
        pd.DataFrame: DataFrame containing the top N users for the specified application.
        """
        return user_data_usage.nlargest(top_n, app_column)