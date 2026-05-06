# HR Analytics — Employee Attrition Analysis

A complete data analysis & visualization project that explores **why employees
leave a company**, using the IBM HR Analytics Employee Attrition dataset.

**Repo:** <https://github.com/Saddiq15/HR_Attrition_Analysis>

---

## Project Overview

- **Goal:** Identify and visualize the key factors driving employee attrition,
  and provide actionable recommendations to HR.
- **Dataset:** IBM HR Analytics Employee Attrition (1,470 employees, 35 features).
- **Tech stack:** Python 3.10+, SQL (SQLite, in-memory), pandas, NumPy,
  Matplotlib, Seaborn, Plotly, Jupyter.
- **Deliverables:** A reproducible Jupyter notebook, a runnable Python script,
  and 8 saved chart PNGs + 2 interactive Plotly charts.

---

## Project Structure

```
HR_Attrition_Analysis/
│
├── archive/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv   # IBM HR dataset (from Kaggle)
│
├── visuals/                                    # Generated automatically on run
│   ├── 01_overall_attrition.png
│   ├── 02_age_attrition.png
│   ├── 03_income_attrition.png
│   ├── 04_overtime_attrition.png
│   ├── 05_satisfaction_wlb.png
│   ├── 06_jobrole_attrition.png
│   ├── 07_correlation_heatmap.png
│   └── 08_years_attrition.png
│
├── HR_Attrition_Analysis.ipynb   # Main notebook (START HERE)
├── firstrun.py                   # Same analysis as a runnable script
├── requirements.txt              # Python dependencies
├── config.yaml                   # (optional) project config
└── README.md                     # This file
```

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/Saddiq15/HR_Attrition_Analysis.git
cd HR_Attrition_Analysis
```

### 2. Create a virtual environment & install dependencies
```powershell
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Get the dataset
The CSV is already included under `archive/`. If you ever need to re-download it:
1. Go to <https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset>
2. Download `WA_Fn-UseC_-HR-Employee-Attrition.csv`
3. Place it at `archive/WA_Fn-UseC_-HR-Employee-Attrition.csv`

### 4. Run the analysis — pick one

**As a notebook (recommended for exploration):**
```bash
jupyter notebook HR_Attrition_Analysis.ipynb
# then: Kernel -> Restart & Run All
```

**As a script (one-shot, generates all PNGs in `visuals/`):**
```bash
python firstrun.py
```

Both produce the same 8 static charts plus 2 interactive Plotly figures and a
printed insights/recommendations summary.

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

## Dataset Details

| Property | Value |
|----------|-------|
| Source | IBM HR Analytics (via Kaggle) |
| Rows | 1,470 employees |
| Columns | 35 features |
| Target | `Attrition` (Yes / No) |

**Key columns used:**
- `Attrition` — target variable (Yes/No)
- `Age`, `Gender`, `MaritalStatus`
- `Department`, `JobRole`, `JobLevel`
- `MonthlyIncome`, `PercentSalaryHike`
- `JobSatisfaction`, `WorkLifeBalance`, `JobInvolvement`
- `OverTime`, `YearsAtCompany`, `YearsSinceLastPromotion`

---

## Reproducibility Notes

A few small bug fixes were applied to make the notebook/script run reliably on
any machine:

- The CSV path is now **relative** (`archive/WA_Fn-UseC_-HR-Employee-Attrition.csv`)
  instead of a hard-coded absolute path.
- The `visuals/` directory is created automatically with `os.makedirs(..., exist_ok=True)`
  so chart saving never fails on a fresh clone.
- `stdout` is reconfigured to UTF-8 so the emoji in `print()` calls don't raise
  `UnicodeEncodeError` on Windows consoles (default `cp1252`).
- `pd.cut` for `AgeGroup` uses `include_lowest=True` so 18-year-olds aren't
  silently dropped, and `IncomeGroup` uses `np.inf` as its upper bound.

---

## Next Steps (Optional Enhancements)

- Train a **machine-learning model** (logistic regression / random forest /
  gradient boosting) to predict attrition probability per employee.
- Build a **Streamlit dashboard** for interactive exploration.
- Swap the in-memory SQLite layer for **PostgreSQL** for a production setup.
- Publish a **Power BI / Tableau** version of the visualizations.

---

## License

Released under the MIT License — see `LICENSE` if present, otherwise feel free
to reuse with attribution.

The IBM HR Analytics dataset is provided by IBM and distributed via Kaggle
under its own terms.

---

*Built as a data analytics portfolio project by [@Saddiq15](https://github.com/Saddiq15).*
