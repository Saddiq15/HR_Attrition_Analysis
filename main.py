# Install required libraries (run once)
# !pip install pandas numpy matplotlib seaborn plotly

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import warnings

warnings.filterwarnings('ignore')

# Ensure stdout can print Unicode characters (emoji) on Windows consoles
# whose default encoding is cp1252.
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Make sure the output directory for charts exists.
VISUALS_DIR = 'visuals'
os.makedirs(VISUALS_DIR, exist_ok=True)

# Set plot style
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

print('✅ All libraries imported successfully!')

#step 2

# Load the dataset (use a path relative to this script so it runs anywhere)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, 'archive', 'WA_Fn-UseC_-HR-Employee-Attrition.csv')
df = pd.read_csv(CSV_PATH)

print(f'✅ Dataset loaded successfully!')
print(f'📊 Shape: {df.shape[0]} rows × {df.shape[1]} columns')
print(f'\n🔍 First 5 rows:')
df.head()

#step 3

# Create in-memory SQLite database
conn = sqlite3.connect(':memory:')
df.to_sql('employees', conn, index=False, if_exists='replace')
print('✅ Data loaded into SQLite database!')

# SQL Query 1: Overall Attrition Count
query1 = '''
SELECT 
    Attrition,
    COUNT(*) AS Count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 2) AS Percentage
FROM employees
GROUP BY Attrition
'''
print('📊 SQL Query 1: Overall Attrition')
pd.read_sql_query(query1, conn)

# SQL Query 2: Attrition by Department
query2 = '''
SELECT 
    Department,
    COUNT(*) AS Total_Employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Left,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM employees
GROUP BY Department
ORDER BY Attrition_Rate DESC
'''
print('📊 SQL Query 2: Attrition Rate by Department')
pd.read_sql_query(query2, conn)

# SQL Query 3: Average Salary by Attrition
query3 = '''
SELECT 
    Attrition,
    ROUND(AVG(MonthlyIncome), 2) AS Avg_Monthly_Income,
    ROUND(AVG(Age), 1) AS Avg_Age,
    ROUND(AVG(YearsAtCompany), 1) AS Avg_Years_At_Company,
    ROUND(AVG(JobSatisfaction), 2) AS Avg_Job_Satisfaction
FROM employees
GROUP BY Attrition
'''
print('📊 SQL Query 3: Key Averages by Attrition')
pd.read_sql_query(query3, conn)

# SQL Query 4: Top 5 Job Roles with Highest Attrition
query4 = '''
SELECT 
    JobRole,
    COUNT(*) AS Total,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS Left_Count,
    ROUND(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Attrition_Rate
FROM employees
GROUP BY JobRole
ORDER BY Attrition_Rate DESC
LIMIT 5
'''
print('📊 SQL Query 4: Top 5 Job Roles by Attrition Rate')
pd.read_sql_query(query4, conn)


#step 4

# Check for null values
print('🔍 Null Values in Dataset:')
print(df.isnull().sum().sum(), 'total nulls found')

# Check for duplicates
print(f'\n🔍 Duplicate Rows: {df.duplicated().sum()}')

# Basic info
print('\n📋 Data Types:')
df.info()

# Drop columns with no useful variation
cols_to_drop = ['EmployeeCount', 'StandardHours', 'Over18', 'EmployeeNumber']
df_clean = df.drop(columns=cols_to_drop)

# Encode target column: Attrition (Yes=1, No=0)
df_clean['AttritionBinary'] = df_clean['Attrition'].map({'Yes': 1, 'No': 0})

# Create Age Groups (include_lowest=True so age==18 isn't dropped to NaN)
df_clean['AgeGroup'] = pd.cut(
    df_clean['Age'],
    bins=[18, 25, 35, 45, 60],
    labels=['18-25', '26-35', '36-45', '46-60'],
    include_lowest=True
)

# Create Income Groups (use np.inf as upper bound to avoid dropping high incomes)
df_clean['IncomeGroup'] = pd.cut(
    df_clean['MonthlyIncome'],
    bins=[0, 3000, 6000, 10000, np.inf],
    labels=['Low (<3K)', 'Medium (3-6K)', 'High (6-10K)', 'Very High (>10K)']
)

print(f'✅ Data cleaned! Shape: {df_clean.shape}')
print(f'\nNew columns added: AttritionBinary, AgeGroup, IncomeGroup')

#step 5

# Basic statistics
print('📊 Summary Statistics (Numerical Columns):')
df_clean.describe().round(2)

# Attrition distribution
attrition_counts = df_clean['Attrition'].value_counts()
attrition_pct = df_clean['Attrition'].value_counts(normalize=True) * 100

print('📊 Overall Attrition Distribution:')
print(f'  Stayed  : {attrition_counts["No"]}  ({attrition_pct["No"]:.1f}%)')
print(f'  Left    : {attrition_counts["Yes"]}  ({attrition_pct["Yes"]:.1f}%)')
print(f'\n⚠️  Attrition Rate: {attrition_pct["Yes"]:.1f}%')

# Attrition by key categorical variables
categorical_cols = ['Department', 'JobRole', 'Gender', 'MaritalStatus', 'OverTime']

for col in categorical_cols:
    attrition_by = df_clean.groupby(col)['AttritionBinary'].mean() * 100
    print(f'\n📌 Attrition Rate by {col}:')
    print(attrition_by.sort_values(ascending=False).round(1).to_string())

#step 6

# ── Chart 1: Overall Attrition Pie Chart ──
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart
colors = ['#2ecc71', '#e74c3c']
axes[0].pie(
    attrition_counts,
    labels=['Stayed', 'Left'],
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    explode=(0, 0.05),
    shadow=True,
    textprops={'fontsize': 13}
)
axes[0].set_title('Overall Employee Attrition', fontsize=15, fontweight='bold')

# Bar chart
attrition_dept = df_clean.groupby('Department')['AttritionBinary'].mean() * 100
attrition_dept.sort_values().plot(kind='barh', ax=axes[1], color=['#3498db', '#9b59b6', '#e74c3c'])
axes[1].set_title('Attrition Rate by Department', fontsize=15, fontweight='bold')
axes[1].set_xlabel('Attrition Rate (%)')
axes[1].xaxis.set_major_formatter(mtick.PercentFormatter())
for i, v in enumerate(attrition_dept.sort_values()):
    axes[1].text(v + 0.3, i, f'{v:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visuals/01_overall_attrition.png', dpi=150, bbox_inches='tight')
plt.show()
print('💾 Chart saved!')

# ── Chart 2: Age Group vs Attrition ──
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Age distribution
df_clean.groupby(['AgeGroup', 'Attrition']).size().unstack().plot(
    kind='bar', ax=axes[0], color=['#2ecc71', '#e74c3c'], edgecolor='white'
)
axes[0].set_title('Employee Count by Age Group', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Age Group')
axes[0].set_ylabel('Count')
axes[0].legend(['Stayed', 'Left'])
axes[0].tick_params(axis='x', rotation=0)

# Attrition rate by age group
attrition_age = df_clean.groupby('AgeGroup')['AttritionBinary'].mean() * 100
attrition_age.plot(kind='bar', ax=axes[1], color='#e74c3c', edgecolor='white')
axes[1].set_title('Attrition Rate by Age Group', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Age Group')
axes[1].set_ylabel('Attrition Rate (%)')
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].tick_params(axis='x', rotation=0)
for i, v in enumerate(attrition_age):
    axes[1].text(i, v + 0.3, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visuals/02_age_attrition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 3: Monthly Income vs Attrition (Box Plot) ──
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_clean,
    x='Attrition',
    y='MonthlyIncome',
    palette={'No': '#2ecc71', 'Yes': '#e74c3c'},
    width=0.5
)
plt.title('Monthly Income vs Attrition', fontsize=15, fontweight='bold')
plt.xlabel('Attrition')
plt.ylabel('Monthly Income ($)')
plt.xticks([0, 1], ['Stayed', 'Left'])

# Add mean annotations
for i, status in enumerate(['No', 'Yes']):
    mean_val = df_clean[df_clean['Attrition'] == status]['MonthlyIncome'].mean()
    plt.text(i, mean_val + 300, f'Mean: ${mean_val:,.0f}', ha='center', fontweight='bold', color='navy')

plt.tight_layout()
plt.savefig('visuals/03_income_attrition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 4: Overtime vs Attrition ──
overtime_data = df_clean.groupby(['OverTime', 'Attrition']).size().unstack()
overtime_pct = overtime_data.div(overtime_data.sum(axis=1), axis=0) * 100

plt.figure(figsize=(8, 6))
overtime_pct.plot(
    kind='bar',
    color=['#2ecc71', '#e74c3c'],
    edgecolor='white',
    width=0.5
)
plt.title('Attrition Rate: Overtime vs No Overtime', fontsize=14, fontweight='bold')
plt.xlabel('Overtime')
plt.ylabel('Percentage (%)')
plt.legend(['Stayed', 'Left'])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('visuals/04_overtime_attrition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 5: Job Satisfaction vs Attrition ──
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Job Satisfaction
sat_data = df_clean.groupby(['JobSatisfaction', 'Attrition']).size().unstack()
sat_pct = sat_data.div(sat_data.sum(axis=1), axis=0) * 100
sat_pct['Yes'].plot(kind='bar', ax=axes[0], color='#e74c3c', edgecolor='white')
axes[0].set_title('Attrition Rate by Job Satisfaction', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Job Satisfaction (1=Low, 4=High)')
axes[0].set_ylabel('Attrition Rate (%)')
axes[0].tick_params(axis='x', rotation=0)

# Work-Life Balance
wlb_data = df_clean.groupby(['WorkLifeBalance', 'Attrition']).size().unstack()
wlb_pct = wlb_data.div(wlb_data.sum(axis=1), axis=0) * 100
wlb_pct['Yes'].plot(kind='bar', ax=axes[1], color='#9b59b6', edgecolor='white')
axes[1].set_title('Attrition Rate by Work-Life Balance', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Work-Life Balance (1=Bad, 4=Best)')
axes[1].set_ylabel('Attrition Rate (%)')
axes[1].tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.savefig('visuals/05_satisfaction_wlb.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 6: Top 10 Job Roles Attrition ──
jobrole_attr = df_clean.groupby('JobRole')['AttritionBinary'].mean() * 100
jobrole_attr = jobrole_attr.sort_values(ascending=True)

colors_list = ['#e74c3c' if x > 15 else '#3498db' for x in jobrole_attr]

plt.figure(figsize=(10, 7))
jobrole_attr.plot(kind='barh', color=colors_list, edgecolor='white')
plt.title('Attrition Rate by Job Role', fontsize=14, fontweight='bold')
plt.xlabel('Attrition Rate (%)')
plt.axvline(x=16.1, linestyle='--', color='gray', alpha=0.7, label='Overall Average')
for i, v in enumerate(jobrole_attr):
    plt.text(v + 0.2, i, f'{v:.1f}%', va='center', fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig('visuals/06_jobrole_attrition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 7: Correlation Heatmap ──
# Select numerical columns relevant to attrition
num_cols = [
    'AttritionBinary', 'Age', 'MonthlyIncome', 'JobSatisfaction',
    'WorkLifeBalance', 'YearsAtCompany', 'YearsSinceLastPromotion',
    'NumCompaniesWorked', 'DistanceFromHome', 'PercentSalaryHike',
    'TotalWorkingYears', 'JobInvolvement'
]

corr = df_clean[num_cols].corr()

plt.figure(figsize=(12, 9))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr,
    mask=mask,
    annot=True,
    fmt='.2f',
    cmap='RdYlGn',
    center=0,
    linewidths=0.5,
    square=True
)
plt.title('Correlation Heatmap — Key Features vs Attrition', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/07_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print('\n📌 Key correlations with AttritionBinary:')
print(corr['AttritionBinary'].drop('AttritionBinary').sort_values().round(3).to_string())

# ── Chart 8: Years at Company vs Attrition ──
plt.figure(figsize=(12, 5))

sns.histplot(
    data=df_clean,
    x='YearsAtCompany',
    hue='Attrition',
    multiple='dodge',
    palette={'No': '#2ecc71', 'Yes': '#e74c3c'},
    bins=20,
    edgecolor='white'
)
plt.title('Years at Company vs Attrition', fontsize=14, fontweight='bold')
plt.xlabel('Years at Company')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('visuals/08_years_attrition.png', dpi=150, bbox_inches='tight')
plt.show()

# ── Chart 9: Interactive Plotly Chart — Income by Dept & Attrition ──
fig = px.box(
    df_clean,
    x='Department',
    y='MonthlyIncome',
    color='Attrition',
    color_discrete_map={'No': '#2ecc71', 'Yes': '#e74c3c'},
    title='Monthly Income Distribution by Department & Attrition',
    labels={'MonthlyIncome': 'Monthly Income ($)', 'Department': 'Department'},
    template='plotly_white'
)
fig.update_layout(title_font_size=16)
fig.show()

# ── Chart 10: Interactive Plotly Scatter — Age vs Income ──
fig = px.scatter(
    df_clean,
    x='Age',
    y='MonthlyIncome',
    color='Attrition',
    size='YearsAtCompany',
    hover_data=['JobRole', 'Department'],
    color_discrete_map={'No': '#2ecc71', 'Yes': '#e74c3c'},
    title='Age vs Monthly Income (Size = Years at Company)',
    template='plotly_white',
    opacity=0.7
)
fig.update_layout(title_font_size=16)
fig.show()

#step 7

# Calculate key stats for the insights summary
overall_rate = df_clean['AttritionBinary'].mean() * 100
overtime_yes_rate = df_clean[df_clean['OverTime'] == 'Yes']['AttritionBinary'].mean() * 100
overtime_no_rate = df_clean[df_clean['OverTime'] == 'No']['AttritionBinary'].mean() * 100
young_rate = df_clean[df_clean['AgeGroup'] == '18-25']['AttritionBinary'].mean() * 100
lowsat_rate = df_clean[df_clean['JobSatisfaction'] == 1]['AttritionBinary'].mean() * 100
highsat_rate = df_clean[df_clean['JobSatisfaction'] == 4]['AttritionBinary'].mean() * 100
mean_income_left = df_clean[df_clean['Attrition'] == 'Yes']['MonthlyIncome'].mean()
mean_income_stayed = df_clean[df_clean['Attrition'] == 'No']['MonthlyIncome'].mean()

print('=' * 65)
print('          📋 KEY INSIGHTS SUMMARY')
print('=' * 65)

print(f"""
📌 INSIGHT 1 — OVERALL ATTRITION
   Overall attrition rate is {overall_rate:.1f}%.
   This means ~1 in 6 employees leaves the company.

📌 INSIGHT 2 — OVERTIME IS A MAJOR DRIVER
   Employees working overtime: {overtime_yes_rate:.1f}% attrition rate
   Employees NOT working overtime: {overtime_no_rate:.1f}% attrition rate
   → Overtime employees are {overtime_yes_rate/overtime_no_rate:.1f}x more likely to leave!

📌 INSIGHT 3 — YOUNG EMPLOYEES LEAVE MORE
   Age 18-25 attrition rate: {young_rate:.1f}%
   → Youngest employees are the most at-risk group.

📌 INSIGHT 4 — JOB SATISFACTION MATTERS
   Low satisfaction (score 1): {lowsat_rate:.1f}% attrition
   High satisfaction (score 4): {highsat_rate:.1f}% attrition
   → Improving satisfaction can significantly reduce attrition.

📌 INSIGHT 5 — LOWER INCOME = HIGHER ATTRITION
   Average monthly income of those who LEFT:   ${mean_income_left:,.0f}
   Average monthly income of those who STAYED: ${mean_income_stayed:,.0f}
   → Employees who leave earn ~${mean_income_stayed - mean_income_left:,.0f} less on average.
""")

print('=' * 65)
print('          💼 HR RECOMMENDATIONS')
print('=' * 65)
print("""
✅ 1. Review overtime policies — introduce compensatory time off
      or limit mandatory overtime in high-attrition departments.

✅ 2. Create a Young Talent Retention Program — mentoring,
      career progression paths, and bonuses for employees under 25.

✅ 3. Conduct regular satisfaction surveys and take action
      quickly when scores are low.

✅ 4. Review salary benchmarks — especially for Sales Reps
      and Lab Technicians, who show the highest attrition.

✅ 5. Focus retention efforts on employees in their first
      1-3 years at the company (highest risk period).
""")
