import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

conn = sqlite3.connect("data/cleaned/skill_gap_analyzer.db")

# --- Chart 1: Top 20 Skills ---
print("Creating Chart 1: Top 20 Skills...")
top_skills = pd.read_sql("SELECT skill, count FROM top_skills ORDER BY count DESC LIMIT 20", conn)

plt.figure(figsize=(12,8))
sns.barplot(x='count', y='skill', data=top_skills, palette='viridis')
plt.title('Top 20 Most In-Demand Skills', fontsize=16, fontweight='bold')
plt.xlabel('Number of Job Postings')
plt.ylabel('Skill')
plt.tight_layout()
plt.savefig('data/cleaned/chart1_top_skills.png')
plt.show()
print("Chart 1 saved!")

# --- Chart 2: Salary by Experience Level ---
print("\nCreating Chart 2: Salary by Experience...")
salary_exp = pd.read_sql("""
SELECT experience_level, AVG(salary_in_usd) as avg_salary
FROM salaries
GROUP BY experience_level
ORDER BY avg_salary DESC
""", conn)

plt.figure(figsize=(10,6))
sns.barplot(x='experience_level', y='avg_salary', data=salary_exp, palette='Blues_r')
plt.title('Average Salary by Experience Level', fontsize=16, fontweight='bold')
plt.xlabel('Experience Level')
plt.ylabel('Average Salary (USD)')
plt.tight_layout()
plt.savefig('data/cleaned/chart2_salary_experience.png')
plt.show()
print("Chart 2 saved!")

# --- Chart 3: Top Paying Job Categories ---
print("\nCreating Chart 3: Top Paying Categories...")
top_categories = pd.read_sql("""
SELECT job_category, AVG(salary_in_usd) as avg_salary
FROM salaries
GROUP BY job_category
ORDER BY avg_salary DESC
LIMIT 15
""", conn)

plt.figure(figsize=(12,8))
sns.barplot(x='avg_salary', y='job_category', data=top_categories, palette='Oranges_r')
plt.title('Top 15 Highest Paying Job Categories', fontsize=16, fontweight='bold')
plt.xlabel('Average Salary (USD)')
plt.ylabel('Job Category')
plt.tight_layout()
plt.savefig('data/cleaned/chart3_top_categories.png')
plt.show()
print("Chart 3 saved!")

# --- Chart 4: Top Job Locations ---
print("\nCreating Chart 4: Top Job Locations...")
top_locations = pd.read_sql("""
SELECT job_location, COUNT(*) as job_count
FROM jobs_skills
GROUP BY job_location
ORDER BY job_count DESC
LIMIT 10
""", conn)

plt.figure(figsize=(12,6))
sns.barplot(x='job_count', y='job_location', data=top_locations, palette='Greens_r')
plt.title('Top 10 Job Locations', fontsize=16, fontweight='bold')
plt.xlabel('Number of Jobs')
plt.ylabel('Location')
plt.tight_layout()
plt.savefig('data/cleaned/chart4_top_locations.png')
plt.show()
print("Chart 4 saved!")

conn.close()
print("\nAll charts created successfully!")