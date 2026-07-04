import pandas as pd
import ast

print("Loading data...")
top_skills_df = pd.read_csv("data/cleaned/top_skills.csv")
resume_df = pd.read_csv("data/cleaned/resume_skills_extracted.csv")

# Get top 20 market skills
market_skills = set(top_skills_df['skill'].head(20).tolist())

# Parse extracted skills
resume_df['extracted_skills'] = resume_df['extracted_skills'].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else []
)

print("\n--- Skill Gap Analysis by Category ---")

categories = ['INFORMATION-TECHNOLOGY', 'ENGINEERING', 'HEALTHCARE', 
              'BANKING', 'FINANCE', 'BUSINESS-DEVELOPMENT']

for category in categories:
    cat_df = resume_df[resume_df['Category'] == category]
    
    all_skills = []
    for skills in cat_df['extracted_skills']:
        all_skills.extend(skills)
    
    resume_skills = set([s.title() for s in all_skills])
    gaps = market_skills - resume_skills
    matching = market_skills & resume_skills
    
    print(f"\n{category}:")
    print(f"  ✅ Matching skills ({len(matching)}): {matching}")
    print(f"  ❌ Skill gaps ({len(gaps)}): {gaps}")

# Save gap analysis
gap_results = []
for category in resume_df['Category'].unique():
    cat_df = resume_df[resume_df['Category'] == category]
    all_skills = []
    for skills in cat_df['extracted_skills']:
        all_skills.extend(skills)
    resume_skills = set([s.title() for s in all_skills])
    gaps = market_skills - resume_skills
    matching = market_skills & resume_skills
    gap_results.append({
        'category': category,
        'matching_count': len(matching),
        'gap_count': len(gaps),
        'gaps': str(list(gaps))
    })

gap_df = pd.DataFrame(gap_results)
gap_df.to_csv("data/cleaned/skill_gap_results.csv", index=False)
print("\n✅ Skill gap results saved!")
print(gap_df.sort_values('gap_count', ascending=False))