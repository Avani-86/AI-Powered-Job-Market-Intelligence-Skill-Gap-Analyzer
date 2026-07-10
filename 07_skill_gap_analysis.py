"""
07_skill_gap_analysis.py

Purpose:
Compare resume skills with market demanded skills
and generate skill gap recommendations
"""

import pandas as pd
import ast


MARKET_SKILLS_PATH = "data/cleaned/top_skills.csv"
RESUME_SKILLS_PATH = "data/cleaned/final_resume_skills.csv"

OUTPUT_PATH = "data/cleaned/skill_gap_results.csv"


print("Loading data...")


market_df = pd.read_csv(MARKET_SKILLS_PATH)

resume_df = pd.read_csv(RESUME_SKILLS_PATH)


# -----------------------------
# Top market skills
# -----------------------------

market_skills = set(
    market_df["skill"]
    .head(20)
    .tolist()
)


# -----------------------------
# Convert skills column
# -----------------------------

resume_df["extracted_skills"] = (
    resume_df["extracted_skills"]
    .apply(ast.literal_eval)
)



results = []


print("\nRunning Skill Gap Analysis...")


for _, row in resume_df.iterrows():

    resume_skills = set(row["extracted_skills"])


    matched = (
        market_skills &
        resume_skills
    )


    missing = (
        market_skills -
        resume_skills
    )


    match_score = round(
        (len(matched) / len(market_skills)) * 100,
        2
    )


    results.append({

        "Category": row["Category"],

        "Match Score (%)":
        match_score,

        "Matched Skills":
        list(matched),

        "Missing Skills":
        list(missing)

    })



# Create dataframe

result_df = pd.DataFrame(results)



# Save result

result_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nSkill Gap Analysis Completed!")

print("Saved:")
print(OUTPUT_PATH)


print("\nSample Result:")
print(result_df.head())