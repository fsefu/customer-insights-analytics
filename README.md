# TellCo Telecommunication Analysis and Recommendation

### By: Sefuwan Feysa  
### Date: September 10, 2024

## Overview

This repository contains the analysis of TellCo's telecommunication data to uncover user behavior, engagement, experience, and satisfaction insights. The main objective of this analysis is to provide actionable recommendations to a potential investor, focusing on improving network performance, enhancing user engagement, and boosting customer satisfaction.

The analysis is built using Python and incorporates several methodologies, including Exploratory Data Analysis (EDA), clustering (K-Means), and regression models for satisfaction prediction. The project is designed with modularity in mind, featuring Dockerized deployment and CI/CD workflows.

## Repository Structure

```bash
.
├── .github/
│   └── workflows/        # CI/CD pipelines for automatic testing, linting, and deployment.
├── app/
│   ├── dashboard_analysis.py  # Main dashboard logic for rendering user behavior, engagement, experience, and satisfaction insights.
│   ├── engagement_analysis.py # Engagement-related visualizations and metrics.
│   ├── experience_analysis.py # Experience-based metrics and clustering insights.
│   ├── satisfaction_analysis.py # Satisfaction score prediction and regression performance.
│   └── user_overview.py    # General user and handset analysis.
├── databases/
│   ├── connections.py      # Establishes connection to local PostgreSQL and MySQL databases.
│   └── database_conversion.py # Handles data export and database structure conversion.
├── notebooks/
│   ├── engagement_analysis.ipynb  # Detailed user engagement metrics exploration.
│   ├── experience_analysis.ipynb  # Network experience metrics and clustering insights.
│   ├── overview_analysis.ipynb    # High-level user and handset analysis.
│   └── satisfaction_analysis.ipynb # Satisfaction prediction model evaluation.
├── scripts/
│   ├── data_cleaning/      
│   │   └── data_cleaning.py # Main data cleaning script for preprocessing.
│   ├── data_loader/
│   │   └── mega_data_loader.py # Consolidated script for loading data.
│   └── data_export/
│       └── data_to_export.py # Aggregates and exports data to MySQL.
├── tasks/
│   ├── export_to_db.py      # Bulk export of final analysis results to the database.
│   └── load_smy.py          # Utility to load summary statistics for data interpretation.
├── utils/
│   ├── Dockerfile           # Docker configuration for containerization.
│   ├── requirements.txt     # Python dependencies.
│   └── .gitignore           # Files and directories to be ignored in Git.
└── README.md                # Project documentation.

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
