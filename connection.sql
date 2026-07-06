import sqlite3
import pandas as pd

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect("data/cleaned/skill_gap_analyzer.db")
    return conn

def run_query(query):
    """Run a SQL query and return results"""
    conn = get_connection()
    result = pd.read_sql(query, conn)
    conn.close()
    return result

def run_schema():
    """Create database schema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    with open('schema.sql', 'r') as f:
        schema = f.read()
    
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("Schema created successfully!")

def run_all_queries():
    """Run all queries and show results"""
    conn = get_connection()
    
    queries = {
        "Top 10 Skills": """
            SELECT skill, count FROM top_skills 
            ORDER BY count DESC LIMIT 10
        """,
        "Salary by Experience": """
            SELECT experience_level, 
            ROUND(AVG(salary_in_usd), 2) as avg_salary
            FROM salaries GROUP BY experience_level
            ORDER BY avg_salary DESC
        """,
        "Top Job Categories": """
            SELECT job_category,
            ROUND(AVG(salary_in_usd), 2) as avg_salary
            FROM salaries GROUP BY job_category
            ORDER BY avg_salary DESC LIMIT 10
        """,
        "Top Locations": """
            SELECT job_location, COUNT(*) as job_count
            FROM jobs_skills GROUP BY job_location
            ORDER BY job_count DESC LIMIT 10
        """
    }
    
    for title, query in queries.items():
        print(f"\n--- {title} ---")
        result = pd.read_sql(query, conn)
        print(result)
    
    conn.close()
    print("\nAll queries executed successfully!")

if __name__ == "__main__":
    print("Testing database connection...")
    conn = get_connection()
    print("Connection successful!")
    conn.close()
    
    print("\nRunning all queries...")
    run_all_queries()