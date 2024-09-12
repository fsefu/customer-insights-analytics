# TellCo Telecommunication Analysis and Recommendation

### By: Sefuwan Feysa  
### Date: September 10, 2024

## Overview

This repository contains the analysis of TellCo's telecommunication data to uncover user behavior, engagement, experience, and satisfaction insights. The main objective of this analysis is to provide actionable recommendations to a potential investor, focusing on improving network performance, enhancing user engagement, and boosting customer satisfaction.

The analysis is built using Python and incorporates several methodologies, including Exploratory Data Analysis (EDA), clustering (K-Means), and regression models for satisfaction prediction. The project is designed with modularity in mind, featuring Dockerized deployment and CI/CD workflows.

## Repository Structure

```bash
Customer-Insights-Analytics/
├── .devcontainer/
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .vscode/
├── app/
│   ├── dashboard_analytics/
│   │   ├── engagement_analysis.py
│   │   ├── experience_analytics.py
│   │   ├── satisfaction_analysis.py
│   │   └── user_overview.py
│   └── main.py
├── databases/
│   ├── connections/
│       ├── database_connector.py
│     
├── mlruns/
├── notebooks/
│   ├── engagement_analysis.ipynb
│   ├── experience_analytics.ipynb
│   ├── export_db.ipynb
│   ├── overview_analysis.ipynb
│   └── satisfaction_analysis.ipynb
├── scripts/
│   └── data_export/
│       └── data_to_export.py
├── src/
│   ├── cleaning/
│   │   └── data_cleaning.py
│   ├── data_loader/
│   │   └── teleco_data_loader.py
│   ├── engagement_analysis/
│   │   ├── telecom_engagement_analysis.py
│   │   └── user_engagement_analysis.py
│   ├── experience_analytics/
│   │   ├── aggregate_customer.py
│   │   ├── distribution_analysis.py
│   │   ├── experience_clustering.py
│   │   └── network_parameter_analyzer.py
│   ├── overview_analysis/
│   │   ├── telecom_data_analyzer.py
│   │   └── telecom_eda.py
│   └── satisfaction_analysis/
│       ├── cluster_score_aggregator.py
│       ├── engagement_experience_scores.py
│       ├── final_data_exporter.py
│       ├── satisfaction_kmeans.py
│       ├── satisfaction_score_predictor.py
│       └── top_satisfactions_analysis.py
├── tests/
│   └── export_to_db.py
├── utils/
│   ├── export_to_db.py
│   └── load_env.py
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt

```

# How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/fsefu/customer-insights-analytics.git
cd customer-insights-analytics
```

 ## 2. Setup Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
 ## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
### 4. Setup Database Connections
Ensure that PostgreSQL and MySQL databases are set up on your local machine or a remote server.
Update the connection parameters in databases/connections.py.

Also, create a .env file in the root directory of the project with the following content:

```bash
DB_NAME="teleco"
DB_HOST="localhost"
DB_PASSWORD=1234
DB_USER="postgres"
DB_PORT=5432
```
Make sure to replace these values with your actual database credentials if they differ.

### 5. Running the Web-based Dashboard
To launch the Streamlit dashboard, execute the following command:

```bash
streamlit run app/dashboard_analysis.py
```

### 6. Dockerized Deployment (Optional)
If you want to deploy the project using Docker:

```bash
docker build -t tellco-telecom-analysis .
docker run -p 8501:8501 tellco-telecom-analysis
```

## Key Features
 - Exploratory Data Analysis (EDA): Comprehensive analysis of user engagement and experience data.
 - K-Means Clustering: User segmentation based on experience and engagement scores.
 - Regression Model for Satisfaction: Predicting customer satisfaction with high accuracy.
 - Streamlit Dashboard: Interactive web-based dashboard for data exploration and visualization.
 - Database Export: Final analysis results are exported to a PostgreSQL/MySQL database for further processing.
## Technologies Used
- Python: Core programming language for analysis and model building.
- Pandas, NumPy: Data manipulation libraries.
- Scikit-learn: For machine learning algorithms such as clustering and regression.
- Streamlit: Framework for building the interactive dashboard.
- PostgreSQL/MySQL: Database systems for storing and querying the final results.
- Docker: Containerization of the project for easy deployment.

## Author
Sefuwan Feysa

Feel free to reach out for any questions or feedback at sefuwanfd@gmail.com.
