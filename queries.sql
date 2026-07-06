-- AI Skill Gap Analyzer - SQL Queries
-- Created by Awantika Shivhare

-- Query 1: Top 10 Most In-Demand Skills
SELECT skill, count
FROM top_skills
ORDER BY count DESC
LIMIT 10;

-- Query 2: Average Salary by Experience Level
SELECT 
    experience_level,
    ROUND(AVG(salary_in_usd), 2) as avg_salary,
    COUNT(*) as total_jobs
FROM salaries
GROUP BY experience_level
ORDER BY avg_salary DESC;

-- Query 3: Top 10 Highest Paying Job Categories
SELECT 
    job_category,
    ROUND(AVG(salary_in_usd), 2) as avg_salary,
    COUNT(*) as total_jobs
FROM salaries
GROUP BY job_category
ORDER BY avg_salary DESC
LIMIT 10;

-- Query 4: Top 10 Job Locations
SELECT 
    job_location,
    COUNT(*) as job_count
FROM jobs_skills
GROUP BY job_location
ORDER BY job_count DESC
LIMIT 10;

-- Query 5: Top 10 Job Titles
SELECT 
    job_title,
    COUNT(*) as job_count
FROM jobs_skills
GROUP BY job_title
ORDER BY job_count DESC
LIMIT 10;

-- Query 6: Salary by Work Setting
SELECT 
    work_setting,
    ROUND(AVG(salary_in_usd), 2) as avg_salary,
    COUNT(*) as total_jobs
FROM salaries
GROUP BY work_setting
ORDER BY avg_salary DESC;

-- Query 7: Salary by Company Size
SELECT 
    company_size,
    ROUND(AVG(salary_in_usd), 2) as avg_salary,
    COUNT(*) as total_jobs
FROM salaries
GROUP BY company_size
ORDER BY avg_salary DESC;

-- Query 8: Experience Level Distribution
SELECT 
    experience_level,
    COUNT(*) as total_jobs,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM salaries), 2) as percentage
FROM salaries
GROUP BY experience_level
ORDER BY total_jobs DESC;

-- Query 9: Top 10 Companies by Job Count
SELECT 
    company,
    COUNT(*) as job_count
FROM jobs_skills
GROUP BY company
ORDER BY job_count DESC
LIMIT 10;

-- Query 10: Skill Gap by Category
SELECT 
    category,
    matching_count,
    gap_count,
    gaps
FROM skill_gap_results
ORDER BY gap_count DESC;

-- Query 11: Window Function - Salary Rank by Category
SELECT 
    job_category,
    job_title,
    ROUND(AVG(salary_in_usd), 2) as avg_salary,
    RANK() OVER (PARTITION BY job_category ORDER BY AVG(salary_in_usd) DESC) as salary_rank
FROM salaries
GROUP BY job_category, job_title
ORDER BY job_category, salary_rank;

-- Query 12: CTE - High Paying Jobs
WITH high_paying AS (
    SELECT 
        job_title,
        job_category,
        ROUND(AVG(salary_in_usd), 2) as avg_salary
    FROM salaries
    GROUP BY job_title, job_category
    HAVING AVG(salary_in_usd) > 100000
)
SELECT * FROM high_paying
ORDER BY avg_salary DESC
LIMIT 20;