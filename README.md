# Care Transition Efficiency & Placement Outcome Analytics

## Overview

The **Care Transition Efficiency & Placement Outcome Analytics** project is an interactive data analytics solution developed to evaluate the operational efficiency of the **Unaccompanied Children (UAC) Care Transition Pipeline** managed by the **U.S. Department of Health and Human Services (HHS)**.

The project models the care process as a three-stage pipeline:

**CBP Custody → HHS Care → Sponsor Placement**

Instead of monitoring only the number of children currently in custody, this project focuses on measuring the efficiency of transitions between each stage, identifying operational bottlenecks, monitoring backlog accumulation, and analyzing placement outcomes over time.

An interactive **Streamlit dashboard** was developed to transform operational data into actionable insights for policymakers, program managers, and operational teams.

---

# Problem Statement

Traditional operational reports primarily focus on aggregate custody counts, providing limited visibility into the efficiency of care transitions.

Key operational questions include:

- How efficiently are children transferred from CBP custody to HHS care?
- Are discharge rates keeping pace with new arrivals?
- When do operational backlogs begin to accumulate?
- Are sponsor placement outcomes improving over time?
- Which stages of the care pipeline contribute most to delays?

This project addresses these challenges by introducing process-oriented performance metrics and interactive visual analytics.

---

# Project Objectives

### Primary Objectives

- Measure CBP to HHS transition efficiency
- Evaluate discharge effectiveness
- Monitor sponsor placement outcomes
- Identify operational bottlenecks
- Analyze backlog accumulation
- Track temporal trends in pipeline performance

### Secondary Objectives

- Support faster reunification
- Improve operational visibility
- Enable data-driven decision making
- Provide an interactive analytical dashboard

---

# Dataset

The dataset contains daily operational records representing the movement of children through the care pipeline.

| Column | Description |
|----------|-------------|
| Date | Reporting date |
| CBP Intake | Children apprehended and placed into CBP custody |
| CBP Custody | Active children in CBP custody |
| Transferred to HHS | Children transferred to HHS care |
| HHS Care | Active children receiving HHS care |
| Discharged | Children successfully placed with approved sponsors |

---

# Technology Stack

### Programming Language

- Python

### Libraries

- Pandas
- NumPy
- Plotly
- Streamlit

### Development Environment

- Jupyter Notebook
- Visual Studio Code

### Version Control

- Git
- GitHub

---

# Data Preprocessing

The following preprocessing steps were performed before analysis:

- Converted date values into datetime format
- Standardized column names
- Converted numerical columns into numeric data types
- Removed invalid values
- Handled missing data
- Verified data consistency
- Engineered analytical features

---

# Key Performance Indicators (KPIs)

### Transfer Efficiency

Measures how efficiently children are transferred from CBP custody to HHS care.

**Formula**

```
Transfer Efficiency (%) =
(Transferred to HHS / CBP Custody) × 100
```

---

### Discharge Efficiency

Measures the proportion of children successfully discharged relative to children currently in HHS care.

**Formula**

```
Discharge Efficiency (%) =
(Discharged / HHS Care) × 100
```

---

### Pipeline Throughput

Measures the overall effectiveness of the transition pipeline.

**Formula**

```
Pipeline Throughput (%) =
(Discharged / CBP Intake) × 100
```

---

### Placement Ratio

Measures successful sponsor placements relative to transfers into HHS care.

**Formula**

```
Placement Ratio (%) =
(Discharged / Transferred to HHS) × 100
```

---

### Daily Backlog

```
Daily Backlog =
CBP Intake − Discharged
```

---

### Cumulative Backlog

```
Running Sum of Daily Backlog
```

---

### Unresolved Cases

```
Unresolved Cases =
CBP Custody + HHS Care
```

---

# Dashboard Features

The Streamlit dashboard provides an interactive interface for monitoring care transition performance.

## Core Modules

- Care Pipeline Flow Visualization
- Transfer Efficiency Dashboard
- Discharge Efficiency Dashboard
- Bottleneck Detection Charts
- Outcome Trend Analysis

---

## User Features

- Date Range Selection
- Interactive KPI Cards
- Ratio-Based Metric Toggle
- Threshold-Based Alerts
- Interactive Charts
- Download Processed Dataset

---

# Dashboard Visualizations

The dashboard includes:

- Care Pipeline Flow Diagram
- Daily Transfer Trend
- Daily Discharge Trend
- Pipeline Throughput Trend
- Backlog Analysis
- Monthly Placement Trends
- Weekday vs Weekend Analysis
- Outcome Stability Charts
- KPI Summary Cards

---

# Project Workflow

```
Data Collection
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Metric Calculation
        │
        ▼
Interactive Dashboard
        │
        ▼
Business Insights & Recommendations
```

---

# Expected Outcomes

The dashboard helps stakeholders:

- Monitor operational efficiency
- Detect transition bottlenecks
- Identify backlog accumulation
- Evaluate sponsor placement performance
- Support operational planning
- Improve decision-making using data

---

# Future Enhancements

Future improvements may include:

- Predictive analytics using Machine Learning
- Backlog forecasting
- Anomaly detection
- Regional performance comparison
- Real-time data integration
- Automated reporting
- Role-based dashboard access

---

# Repository Structure

```
Care-Transition-Analytics/
│
├── app.py
├── requirements.txt
├── README.md
├── dataset/
│   └── care_transition.csv
├── notebooks/
│   └── EDA.ipynb
├── screenshots/
├── reports/
└── assets/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Care-Transition-Analytics.git
```

Navigate to the project directory

```bash
cd Care-Transition-Analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```
- Upload the Cleaned csv file for dashboard
---



# Author

**Vikram Patel**

B.Tech – Artificial Intelligence & Machine Learning

Data Analytics | Python | SQL | Streamlit | Machine Learning

---

# License

This project was developed for educational, research, and portfolio purposes.
