import pandas as pd
import sqlite3

conn = sqlite3.connect("data/cleaned/skill_gap_analyzer.db")

print("--- Query 1: Top 10 Job Locations ---")
q1 = """
SELECT job_location, COUNT(*) as job_count
FROM jobs_skills
GROUP BY job_location
ORDER BY job_count DESC
LIMIT 10
"""
print(pd.read_sql(q1, conn))

print("\n--- Query 2: Top 10 Job Titles ---")
q2 = """
SELECT job_title, COUNT(*) as job_count
FROM jobs_skills
GROUP BY job_title
ORDER BY job_count DESC
LIMIT 10
"""
print(pd.read_sql(q2, conn))

print("\n--- Query 3: Average Salary by Experience Level ---")
q3 = """
SELECT experience_level, AVG(salary_in_usd) as avg_salary, COUNT(*) as job_count
FROM salaries
GROUP BY experience_level
ORDER BY avg_salary DESC
"""
print(pd.read_sql(q3, conn))

print("\n--- Query 4: Top Job Categories by Average Salary ---")
q4 = """
SELECT job_category, AVG(salary_in_usd) as avg_salary
FROM salaries
GROUP BY job_category
ORDER BY avg_salary DESC
LIMIT 15
"""
print(pd.read_sql(q4, conn))

conn.close()