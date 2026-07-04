import pandas as pd
import re
from collections import Counter

print("Loading datasets...")
resume_df = pd.read_csv("data/raw/Resume/Resume.csv")
top_skills_df = pd.read_csv("data/cleaned/top_skills.csv")

print("Shape:", resume_df.shape)

# Create skills list from top 100 skills
skills_list = [skill.lower() for skill in top_skills_df['skill'].tolist()]

def extract_skills_from_resume(resume_text):
    """Extract skills from resume text by matching against known skills"""
    if pd.isna(resume_text):
        return []
    
    resume_lower = resume_text.lower()
    found_skills = []
    
    for skill in skills_list:
        # Check if skill appears in resume
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_lower):
            found_skills.append(skill.title())
    
    return found_skills

print("\nExtracting skills from resumes...")
resume_df['extracted_skills'] = resume_df['Resume_str'].apply(extract_skills_from_resume)
resume_df['skill_count'] = resume_df['extracted_skills'].apply(len)

print("\n--- Sample Results ---")
for i in range(3):
    print(f"\nResume {i+1} Category: {resume_df['Category'].iloc[i]}")
    print(f"Skills found: {resume_df['extracted_skills'].iloc[i]}")
    print(f"Total skills: {resume_df['skill_count'].iloc[i]}")

print("\n--- Average Skills per Resume by Category ---")
avg_skills = resume_df.groupby('Category')['skill_count'].mean().sort_values(ascending=False)
print(avg_skills)

# Save results
resume_df[['Category', 'extracted_skills', 'skill_count']].to_csv(
    "data/cleaned/resume_skills_extracted.csv", index=False)
print("\nSaved to data/cleaned/resume_skills_extracted.csv!")