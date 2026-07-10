"""
05_resume_nlp.py

Purpose:
- Load resume dataset
- Clean resume text
- Extract technical skills from resumes
- Save extracted skills for skill gap analysis
"""

import pandas as pd
import re
import ast


# -----------------------------
# File Paths
# -----------------------------

RESUME_PATH = "data/raw/Resume/Resume.csv"
OUTPUT_PATH = "data/cleaned/resume_skills_extracted.csv"


# -----------------------------
# Skill Dictionary
# -----------------------------

SKILL_LIST = [
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Data Analysis",
    "Data Visualization",
    "Pandas",
    "NumPy",
    "Scikit Learn",
    "AWS",
    "Azure",
    "Java",
    "C++",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Statistics",
    "Git",
    "Docker"
]


# -----------------------------
# Text Cleaning Function
# -----------------------------

def clean_text(text):

    if pd.isna(text):
        return ""

    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()



# -----------------------------
# Skill Extraction Function
# -----------------------------

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILL_LIST:

        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills



# -----------------------------
# Main Pipeline
# -----------------------------

print("Loading Resume Dataset...")

resume_df = pd.read_csv(RESUME_PATH)


print("Dataset Shape:", resume_df.shape)


# Check columns
print("\nColumns:")
print(resume_df.columns.tolist())


# Clean resume text

resume_df["clean_resume"] = resume_df["Resume_str"].apply(clean_text)


# Extract skills

print("\nExtracting skills...")

resume_df["extracted_skills"] = (
    resume_df["clean_resume"]
    .apply(extract_skills)
)



# Save only required columns

output_df = resume_df[
    [
        "ID",
        "Category",
        "clean_resume",
        "extracted_skills"
    ]
]


output_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\nSkill extraction completed!")
print("Saved file:")
print(OUTPUT_PATH)


# Preview

print("\nSample Result:")
print(output_df.head())