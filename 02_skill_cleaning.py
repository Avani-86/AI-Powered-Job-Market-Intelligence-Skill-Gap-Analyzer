import pandas as pd
from collections import Counter
import re

print("Loading merged dataset...")
df = pd.read_csv("data/cleaned/master_jobs_skills.csv")
print("Shape:", df.shape)

df = df.dropna(subset=['job_skills'])
print("After dropping missing skills:", df.shape)

def normalize_skill(skill):
    skill = skill.strip().lower()
    skill = re.sub(r'\s+', ' ', skill)  # collapse multiple spaces
    skill = skill.replace('problemsolving', 'problem solving')
    return skill.title()  # consistent capitalization

print("\nCounting skills (this is memory-efficient)...")

skill_counter = Counter()

for skills_text in df['job_skills']:
    skills = [normalize_skill(s) for s in skills_text.split(',')]
    skill_counter.update(skills)

print("\n--- Top 30 Most In-Demand Skills (Cleaned) ---")
top_skills = skill_counter.most_common(30)
for skill, count in top_skills:
    print(f"{skill}: {count}")

    print("\n--- Saving Top Skills ---")
skills_df = pd.DataFrame(skill_counter.most_common(100), columns=['skill', 'count'])
skills_df.to_csv("data/cleaned/top_skills.csv", index=False)
print("Saved top 100 skills to data/cleaned/top_skills.csv!")