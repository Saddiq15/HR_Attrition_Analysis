# HR Analytics — Employee Attrition Analysis

A small data-analysis project that explores **why employees leave a company**,
using the IBM HR Analytics Employee Attrition dataset. The same analysis is
provided in two equivalent forms: a Jupyter notebook for exploration and a
plain Python script for one-shot runs.

## Project Structure

```
HR_Attrition/
├── HR_Attrition_Analysis.ipynb            # Main notebook — start here
├── main.py                                # Same analysis as a runnable script
├── requirements.txt                       # Python dependencies
├── WA_Fn-UseC_-HR-Employee-Attrition.csv  # IBM HR dataset (1,470 rows × 35 cols)
├── visuals/                               # Generated chart PNGs
│   ├── 01_overall_attrition.png
│   ├── 02_age_attrition.png
│   ├── 03_income_attrition.png
│   ├── 04_overtime_attrition.png
│   ├── 05_satisfaction_wlb.png
│   ├── 06_jobrole_attrition.png
│   ├── 07_correlation_heatmap.png
│   └── 08_years_attrition.png
└── README.md                              # This file
```

The script and notebook both expect to be run from inside the `HR_Attrition/`
folder so the relative paths to the CSV and `visuals/` resolve correctly.

---

## Quick Start

### 1. Get the code
```bash
git clone https://github.com/Saddiq15/HR_Attrition_Analysis.git
cd HR_Attrition_Analysis/HR_Attrition
```

### 2. Create a virtual environment & install dependencies

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` pulls in `numpy`, `pandas`, `matplotlib`, `seaborn`,
`plotly`, and `requests`. To run the notebook you'll also want Jupyter:
```bash
pip install jupyter
```

### 3. Run the analysis — pick one

**Notebook (recommended for exploration):**
```bash
jupyter notebook HR_Attrition_Analysis.ipynb
# then: Kernel → Restart & Run All
```

**Script (one-shot, regenerates every PNG in `visuals/`):**
```bash
python main.py
```

Both produce the same 8 static charts saved to `visuals/`, two interactive
Plotly figures, and a printed insights/recommendations summary.

---

## What the Analysis Does

| Step | What happens |
|------|--------------|
| 1 | Imports libraries and configures the plot style |
| 2 | Loads the IBM HR CSV into a pandas DataFrame |
| 3 | Loads the data into an in-memory **SQLite** DB and runs 4 SQL queries |
| 4 | Cleans the data and engineers `AttritionBinary`, `AgeGroup`, `IncomeGroup` |
| 5 | EDA — distribution of attrition by department, role, gender, marital status, overtime |
| 6 | 10 visualizations (8 saved as PNG + 2 interactive Plotly) |
| 7 | Prints key insights and HR recommendations |

### SQL queries
1. Overall attrition count (Yes vs No, with %)
2. Attrition rate by department
3. Average income / age / tenure / job satisfaction by attrition
4. Top 5 job roles ranked by attrition rate

### Visualizations
1. Overall attrition pie + department bar
2. Age group vs attrition
3. Monthly income boxplot by attrition
4. Overtime vs attrition
5. Job satisfaction & work-life balance vs attrition
6. Attrition rate by job role
7. Correlation heatmap of key numeric features
8. Years at company vs attrition (histogram)
9. *(interactive)* Income by department & attrition (Plotly box)
10. *(interactive)* Age vs income, sized by years at company (Plotly scatter)

---

## Key Findings

- **Overall attrition: ~16%** — roughly 1 in 6 employees leaves.
- **Overtime** employees are about **3× more likely** to leave (≈30% vs ≈10%).
- **Young employees (18-25)** have the highest attrition rate (~36%).
- **Low job satisfaction (score 1)** roughly doubles the leave rate vs **high satisfaction (score 4)**.
- Employees who left earn on average **~$2,000/month less** than those who stayed.

## HR Recommendations

- Review and limit mandatory overtime, especially in high-attrition departments.
- Build a Young Talent retention program (mentoring, clear progression paths).
- Run regular satisfaction pulse surveys and act on low scores quickly.
- Benchmark salaries for the highest-attrition roles (Sales Reps, Lab Technicians).
- Invest in employee experience during the first 1–3 years at the company.

---

## Dataset

| Property | Value |
|----------|-------|
| Source   | IBM HR Analytics Employee Attrition (Kaggle) |
| Rows     | 1,470 |
| Columns  | 35 |
| Target   | `Attrition` (Yes / No) |

Original Kaggle page:
<https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset>

Key columns used by the analysis: `Attrition`, `Age`, `Gender`, `MaritalStatus`,
`Department`, `JobRole`, `JobLevel`, `MonthlyIncome`, `PercentSalaryHike`,
`JobSatisfaction`, `WorkLifeBalance`, `JobInvolvement`, `OverTime`,
`YearsAtCompany`, `YearsSinceLastPromotion`.

---

## Reproducibility Notes

A few small details make the project run cleanly on a fresh clone:

- All paths are **relative to the project folder**, so the code works on any
  machine without editing.
- `main.py` resolves the CSV and `visuals/` paths relative to the script file
  itself, so it also works when invoked from a different working directory.
- `visuals/` is auto-created (`os.makedirs(..., exist_ok=True)`), so saving
  charts never fails on a clean checkout.
- `stdout` is reconfigured to UTF-8 so emoji in `print()` calls don't trip the
  `cp1252` Windows console.
- `pd.cut` for `AgeGroup` uses `include_lowest=True` (so age 18 isn't dropped),
  and `IncomeGroup`'s upper bound is `np.inf` to avoid silent data loss.

---

## Possible Next Steps

- Train a **classifier** (logistic regression / random forest / gradient
  boosting) to predict attrition probability per employee.
- Wrap the EDA in a **Streamlit** dashboard for interactive exploration.
- Swap the in-memory SQLite layer for **PostgreSQL** for a production setup.
- Publish a **Power BI / Tableau** version of the visuals.

---

*Built as a data analytics portfolio project by [@Saddiq15](https://github.com/Saddiq15).*
