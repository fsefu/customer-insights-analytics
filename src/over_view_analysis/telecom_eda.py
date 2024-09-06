import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class TelecomEDA:
    def __init__(self, data):
        """
        Initialize with the dataset
        """
        self.data = data

        # Define DL and UL columns
        self.dl_columns = [
            'Avg Bearer TP DL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 'HTTP DL (Bytes)',
            'Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
            'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)',
            'Other DL (Bytes)', 'Total DL (Bytes)'
        ]
        self.ul_columns = [
            'Avg Bearer TP UL (kbps)', 'TCP UL Retrans. Vol (Bytes)', 'HTTP UL (Bytes)',
            'Social Media UL (Bytes)', 'Google UL (Bytes)', 'Email UL (Bytes)',
            'Youtube UL (Bytes)', 'Netflix UL (Bytes)', 'Gaming UL (Bytes)',
            'Other UL (Bytes)', 'Total UL (Bytes)'
        ]
        
        # Ensure DL and UL columns exist in the dataset
        self.dl_columns = [col for col in self.dl_columns if col in self.data.columns]
        self.ul_columns = [col for col in self.ul_columns if col in self.data.columns]
        self.data['application_type'] = self.data.apply(
                    lambda row: 'YouTube' if row['Youtube DL (Bytes)'] > 0 
                    else 'Netflix' if row['Netflix DL (Bytes)'] > 0
                    else 'Social Media' if row['Social Media DL (Bytes)'] > 0
                    else 'Gaming' if row['Gaming DL (Bytes)'] > 0
                    else 'Google' if row['Google DL (Bytes)'] > 0
                    else 'Email' if row['Email DL (Bytes)'] > 0
                    else 'Other', axis=1
                )
                

    def describe_variables(self):
        """
        Describe all relevant variables and associated data types
        """
        description = self.data.describe()
        print(f"Dataset Description:\n{description}")
        return description
    def segment_users_by_decile(self):
        """
        Segment users into decile classes based on total session duration
        and compute the total data (DL+UL) per decile class.
        """
        # Rename 'Dur. (ms)' to 'total_duration'
        if 'Dur. (ms)' in self.data.columns:
            self.data.rename(columns={'Dur. (ms)': 'total_duration'}, inplace=True)
        else:
            print("Error: 'Dur. (ms)' column not found in the dataset.")
            return None

        # Calculate total download and upload data
        self.data['total_DL'] = self.data[self.dl_columns].sum(axis=1)
        self.data['total_UL'] = self.data[self.ul_columns].sum(axis=1)
        self.data['total_data'] = self.data['total_DL'] + self.data['total_UL']

        # Segment users by decile based on session duration
        self.data['decile_class'] = pd.qcut(self.data['total_duration'], 5, labels=False)
        decile_summary = self.data.groupby('decile_class').agg({
            'total_duration': 'sum',
            'total_data': 'sum'
        })
        print(f"Decile Summary:\n{decile_summary}")
        return decile_summary
    
    def basic_metrics(self):
        """
        Analyze basic metrics (mean, median, standard deviation) for numeric columns only.
        """
        # Select only numeric columns
        numeric_data = self.data.select_dtypes(include=[np.number])

        # Calculate mean, median, and standard deviation
        metrics = {
            'mean': numeric_data.mean(numeric_only=True),
            'median': numeric_data.median(numeric_only=True),
            'std_dev': numeric_data.std(numeric_only=True)
        }

        print(f"Basic Metrics:\n{metrics}")
        return metrics

    def univariate_analysis(self):
        """
        Non-graphical univariate analysis: Dispersion parameters for each quantitative variable.
        """
        dispersion = self.data.describe()
        print(f"Univariate Analysis:\n{dispersion}")
        return dispersion

    def graphical_univariate_analysis(self):
        """
        Graphical univariate analysis: Suitable plotting options for each variable.
        Dynamically adjusts the grid layout based on the number of numerical columns.
        """
        num_columns = len(self.data.select_dtypes(include=[np.number]).columns)
        
        # Calculate the number of rows needed for the grid
        ncols = 3  # You can adjust this for a different number of columns per row
        nrows = (num_columns + ncols - 1) // ncols  # Calculate rows needed (ceiling division)

        plt.figure(figsize=(5 * ncols, 5 * nrows))  # Adjusting figure size for better readability
        for i, column in enumerate(self.data.select_dtypes(include=[np.number]).columns):
            plt.subplot(nrows, ncols, i + 1)
            sns.histplot(self.data[column], kde=True)
            plt.title(f"Distribution of {column}")
        
        plt.tight_layout()
        plt.show()


    def bivariate_analysis(self):
        """
        Explore relationships between applications & total DL+UL data.
        """

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=self.data, x='total_data', y='application_type', hue='total_duration')
        plt.title("Bivariate Analysis: Application vs Data")
        plt.show()

    def correlation_analysis(self):
        """
        Compute a correlation matrix and visualize the relationships.
        """
        corr_matrix = self.data[['Social_Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 
                                 'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
        plt.title("Correlation Matrix")
        plt.show()
        return corr_matrix

    def dimensionality_reduction(self):
        """
        Perform PCA to reduce dimensionality and interpret results.
        """
        features = ['Social_Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)', 
                    'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']
        x = self.data[features].values
        x = StandardScaler().fit_transform(x)
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(x)
        explained_variance = pca.explained_variance_ratio_
        print(f"PCA Explained Variance: {explained_variance}")

        # Plot the principal components
        plt.figure(figsize=(8, 6))
        plt.scatter(principal_components[:, 0], principal_components[:, 1], alpha=0.5)
        plt.title('2 Component PCA')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.show()

        return explained_variance
