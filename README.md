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
cd tellco-telecom-analysis
```
