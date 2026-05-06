# 🏢 HR Analytics — Employee Attrition Analysis
### A Complete Data Analysis & Visualization Portfolio Project

---

## 📌 Project Overview

**Goal:** Identify and visualize the key factors driving employee attrition at a company, and provide actionable recommendations to HR.

**Dataset:** IBM HR Analytics Employee Attrition Dataset  
**Tools:** Python, SQL (SQLite), Pandas, Matplotlib, Seaborn, Plotly  
**Level:** Beginner–Intermediate

---

## 📁 Project Structure

```
hr-attrition-project/
│
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv   ← Download from Kaggle
│
├── visuals/
│   ├── 01_overall_attrition.png
│   ├── 02_age_attrition.png
│   ├── 03_income_attrition.png
│   ├── 04_overtime_attrition.png
│   ├── 05_satisfaction_wlb.png
│   ├── 06_jobrole_attrition.png
│   ├── 07_correlation_heatmap.png
│   └── 08_years_attrition.png
│
├── HR_Attrition_Analysis.ipynb   ← Main notebook (START HERE)
└── README.md                     ← This file
```

---

## ⚙️ Setup Instructions

### Step 1: Install Python
Make sure Python 3.8+ is installed. Download from https://python.org

### Step 2: Install Required Libraries
Open your terminal and run:
```bash
pip install pandas numpy matplotlib seaborn plotly jupyter
```

### Step 3: Download the Dataset
1. Go to: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
2. Sign in / create a free Kaggle account
3. Click **Download**
4. Place the CSV file inside the `data/` folder

### Step 4: Launch Jupyter Notebook
```bash
jupyter notebook
```
Then open `HR_Attrition_Analysis.ipynb`

### Step 5: Run All Cells
Click **Kernel → Restart & Run All** to execute the entire notebook.

---

## 📊 What's Inside the Notebook

| Step | Description |
|------|-------------|
| 1 | Install & Import Libraries |
| 2 | Load Dataset |
| 3 | SQL Exploration (4 queries) |
| 4 | Data Cleaning & Feature Engineering |
| 5 | Exploratory Data Analysis |
| 6 | 10 Visualizations (Static + Interactive) |
| 7 | Key Insights & HR Recommendations |

---

## 🔍 SQL Queries Included

1. **Overall Attrition Count** — How many employees left vs stayed?
2. **Attrition by Department** — Which department has the highest turnover?
3. **Average Key Metrics by Attrition** — Income, age, satisfaction
4. **Top Job Roles with Highest Attrition** — Which roles are most at risk?

---

## 📈 Visualizations Created

1. 🥧 Overall Attrition Pie Chart + Department Bar Chart
2. 📊 Age Group vs Attrition
3. 📦 Monthly Income Boxplot by Attrition
4. ⏰ Overtime vs Attrition
5. 😊 Job Satisfaction & Work-Life Balance vs Attrition
6. 👔 Attrition Rate by Job Role
7. 🌡️ Correlation Heatmap
8. 📅 Years at Company vs Attrition
9. 🎯 Interactive: Income by Dept & Attrition (Plotly)
10. 🔵 Interactive: Age vs Income Scatter Plot (Plotly)

---

## 💡 Key Findings

1. **Overall attrition rate: ~16%** — roughly 1 in 6 employees leaves
2. **Overtime employees** are 3x more likely to leave
3. **Young employees (18-25)** have the highest attrition risk
4. **Low job satisfaction** strongly correlates with leaving
5. **Employees who leave earn ~$2,000 less/month** on average

---

## ✅ HR Recommendations

- Review and limit mandatory overtime
- Create a Young Talent Retention Program
- Conduct regular satisfaction surveys
- Review salary benchmarks for high-attrition roles
- Focus on employee experience in first 1-3 years

---

## 🚀 Next Steps (Optional Enhancements)

- Build a **Machine Learning model** to predict attrition probability
- Create a **Streamlit web dashboard** for interactive exploration
- Use **PostgreSQL** instead of SQLite for a production setup
- Add **Power BI / Tableau** version of the visualizations

---

## 📚 Dataset Details

| Property | Value |
|----------|-------|
| Source | IBM HR Analytics (via Kaggle) |
| Rows | 1,470 employees |
| Columns | 35 features |
| Target | Attrition (Yes / No) |

**Key columns used:**
- `Attrition` — Target variable (Yes/No)
- `Age`, `Gender`, `MaritalStatus`
- `Department`, `JobRole`, `JobLevel`
- `MonthlyIncome`, `PercentSalaryHike`
- `JobSatisfaction`, `WorkLifeBalance`, `JobInvolvement`
- `OverTime`, `YearsAtCompany`, `YearsSinceLastPromotion`

---

*Built as a Data Science portfolio project.*
