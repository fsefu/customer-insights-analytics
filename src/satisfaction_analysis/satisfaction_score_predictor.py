import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

class SatisfactionScorePredictor:
    def __init__(self, user_data):
        """
        Initialize the SatisfactionScorePredictor class.
        
        Parameters:
        - user_data: DataFrame containing user data with engagement, experience, and satisfaction scores.
        """
        self.user_data = user_data
        self.model = None

    def prepare_data(self):
        """
        Prepares the data for training the regression model.
        
        Returns:
        - X_train, X_test: Features for training and testing.
        - y_train, y_test: Target satisfaction scores for training and testing.
        """
        # Extract features (engagement and experience scores) and target (satisfaction score)
        X = self.user_data[['engagement_score', 'experience_score']]
        y = self.user_data['satisfaction_score']
        
        # Split the data into training and testing sets (80% train, 20% test)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def build_regression_model(self):
        """
        Builds and trains a linear regression model to predict customer satisfaction score.
        
        Returns:
        - The trained model.
        """
        # Prepare the data
        X_train, X_test, y_train, y_test = self.prepare_data()
        
        # Instantiate and train the linear regression model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Make predictions on the test set
        y_pred = self.model.predict(X_test)
        
        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Evaluation:\nMean Squared Error: {mse:.4f}\nR-squared: {r2:.4f}")
        return self.model

    def predict_satisfaction(self, engagement_score, experience_score):
        """
        Predict the satisfaction score for a new customer based on engagement and experience scores.
        
        Parameters:
        - engagement_score: The engagement score of the customer.
        - experience_score: The experience score of the customer.
        
        Returns:
        - Predicted satisfaction score.
        """
        if self.model is None:
            raise Exception("The model is not trained. Call `build_regression_model` first.")
        
        # Create a DataFrame for prediction
        input_data = pd.DataFrame([[engagement_score, experience_score]], 
                                  columns=['engagement_score', 'experience_score'])
        
        # Predict the satisfaction score
        predicted_score = self.model.predict(input_data)
        return predicted_score[0]
    def visualize_results(self, X_test, y_test):
        """
        Visualizes the results of the regression model, comparing actual vs predicted satisfaction scores
        and plotting residuals.
        
        Parameters:
        - X_test: Test set features (engagement and experience scores).
        - y_test: Actual satisfaction scores from the test set.
        """
        # Generate predictions for the test set
        y_pred = self.model.predict(X_test)
        
        # Actual vs Predicted Satisfaction Scores
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_test, y=y_pred, color='blue', edgecolor='w', s=100)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2, color='red')
        plt.title("Actual vs Predicted Satisfaction Scores", fontsize=14)
        plt.xlabel("Actual Satisfaction Score")
        plt.ylabel("Predicted Satisfaction Score")
        plt.grid(True)
        plt.show()

        # Residual Plot
        residuals = y_test - y_pred
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=y_pred, y=residuals, color='green', edgecolor='w', s=100)
        plt.axhline(0, color='red', linestyle='--', lw=2)
        plt.title("Residuals Plot", fontsize=14)
        plt.xlabel("Predicted Satisfaction Score")
        plt.ylabel("Residuals")
        plt.grid(True)
        plt.show()