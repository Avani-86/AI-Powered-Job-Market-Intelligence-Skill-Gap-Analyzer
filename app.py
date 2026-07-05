import streamlit as st
import pandas as pd
import re
import plotly.express as px

st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    page_icon="🎯",
    layout="wide"
)

@st.cache_data
def load_data():
    top_skills = pd.read_csv("data/cleaned/top_skills.csv")
    gap_results = pd.read_csv("data/cleaned/skill_gap_results.csv")
    return top_skills, gap_results

top_skills_df, gap_df = load_data()

skills_list = top_skills_df['skill'].tolist()

def extract_skills(text):
    found = []
    text_lower = text.lower()
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
            found.append(skill)
    return found

st.sidebar.title("AI Skill Gap Analyzer")
page = st.sidebar.radio("Navigate", [
    "Home",
    "Market Insights", 
    "Skill Gap Analyzer",
    "Skill Matching",
    "Recommendation Engine"
])

if page == "Home":
    st.title("AI-Powered Job Market and Skill Gap Intelligence Platform")
    st.markdown("Built with Python, SQL, NLP, and Power BI")
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Job Postings Analyzed", "1.3M+")
    col2.metric("Unique Companies", "88,995")
    col3.metric("Locations Covered", "28,791")
    col4.metric("Skills Tracked", "100+")
    st.markdown("---")
    st.subheader("What This Platform Does")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Market Intelligence: Analyze 1.3M+ real job postings to find the most in-demand skills")
        st.success("Salary Insights: Discover which skills and categories pay the highest salaries")
    with col2:
        st.warning("Skill Gap Analysis: Paste your resume and instantly see which skills you are missing")
        st.error("Career Guidance: Get personalized recommendations on what to learn next")

elif page == "Market Insights":
    st.title("Job Market Insights")
    st.markdown("Based on analysis of 1.3 Million+ real job postings")
    st.markdown("---")
    st.subheader("Top 20 Most In-Demand Skills")
    top20 = top_skills_df.head(20)
    fig1 = px.bar(top20, x='count', y='skill',
                  orientation='h',
                  color='count',
                  color_continuous_scale='viridis',
                  title='Top 20 Skills Demanded by Employers')
    fig1.update_layout(height=600)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("---")
    st.subheader("Salary Insights by Job Category")
    salary_data = {
        'Category': ['Machine Learning and AI', 'Data Science',
                    'Data Architecture', 'Cloud and Database',
                    'Data Engineering', 'BI and Visualization',
                    'Data Analysis', 'Data Management'],
        'Avg Salary USD': [178925, 163758, 156002, 155000,
                          146198, 135092, 108505, 103139]
    }
    salary_df = pd.DataFrame(salary_data)
    fig2 = px.bar(salary_df, x='Avg Salary USD', y='Category',
                  orientation='h',
                  color='Avg Salary USD',
                  color_continuous_scale='oranges',
                  title='Average Salary by Job Category')
    fig2.update_layout(height=500)
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Skill Gap Analyzer":
    st.title("Personal Skill Gap Analyzer")
    st.markdown("Paste your resume text below to get an instant skill gap analysis!")
    st.markdown("---")
    job_category = st.selectbox("Select your target job category:",
        ['Data Science', 'Software Engineering', 'Marketing',
         'Finance', 'Healthcare', 'Business Development'])
    resume_text = st.text_area("Paste your resume text here:",
        height=300,
        placeholder="Paste your resume content here...")
    if st.button("Analyze My Skills", type="primary"):
        if resume_text:
            found_skills = extract_skills(resume_text)
            market_top20 = set(top_skills_df['skill'].head(20).tolist())
            missing_skills = market_top20 - set(found_skills)
            matching_skills = market_top20 & set(found_skills)
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            col1.metric("Skills Found", len(found_skills))
            col2.metric("Market Skills Matched", len(matching_skills))
            col3.metric("Skills Missing", len(missing_skills))
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.success("Skills you have:")
                for skill in sorted(found_skills):
                    st.write(f"- {skill}")
            with col2:
                st.error("Skills you are missing:")
                for skill in sorted(missing_skills):
                    st.write(f"- {skill}")
            st.markdown("---")
            st.subheader("Recommended Learning Path")
            for skill in sorted(missing_skills):
                st.info(f"Learn {skill} — Search for '{skill} course' on Coursera or Udemy")
        else:
            st.warning("Please paste your resume text first!")

elif page == "Skill Matching":
    st.title("Job Role Skill Matching")
    st.markdown("Find out how well your skills match different job roles!")
    st.markdown("---")
    job_roles = {
        "Data Analyst": ["Data Analysis", "Microsoft Office Suite",
                        "Communication", "Problem Solving", "Teamwork",
                        "Attention To Detail", "Time Management",
                        "Project Management", "Leadership", "Collaboration"],
        "HR Manager": ["Communication", "Leadership", "Teamwork",
                      "Problem Solving", "Time Management",
                      "Interpersonal Skills", "Organizational Skills",
                      "Training", "Collaboration", "Attention To Detail"],
        "Sales Executive": ["Sales", "Communication", "Customer Service",
                           "Problem Solving", "Teamwork", "Leadership",
                           "Time Management", "Interpersonal Skills",
                           "Collaboration", "Attention To Detail"],
        "Business Developer": ["Communication", "Leadership", "Sales",
                              "Problem Solving", "Teamwork",
                              "Project Management", "Time Management",
                              "Interpersonal Skills", "Collaboration",
                              "Customer Service"],
        "Healthcare Professional": ["Patient Care", "Nursing", "Communication",
                                   "Teamwork", "Problem Solving", "Leadership",
                                   "Attention To Detail", "Time Management",
                                   "Collaboration", "Training"]
    }
    resume_text = st.text_area("Paste your resume text here:",
        height=200,
        placeholder="Paste your resume content here...")
    if st.button("Find My Best Job Match", type="primary"):
        if resume_text:
            found_skills = set(extract_skills(resume_text))
            st.markdown("---")
            st.subheader("Your Job Role Match Results")
            match_results = []
            for role, required_skills in job_roles.items():
                required = set(required_skills)
                matched = found_skills & required
                match_pct = round((len(matched) / len(required)) * 100, 1)
                match_results.append({
                    'Job Role': role,
                    'Match %': match_pct,
                    'Matched Skills': len(matched),
                    'Required Skills': len(required)
                })
            match_df = pd.DataFrame(match_results)
            match_df = match_df.sort_values('Match %', ascending=False)
            for _, row in match_df.iterrows():
                match_pct = row['Match %']
                if match_pct >= 70:
                    st.success(f"{row['Job Role']} — {match_pct}% match ({row['Matched Skills']}/{row['Required Skills']} skills)")
                elif match_pct >= 40:
                    st.warning(f"{row['Job Role']} — {match_pct}% match ({row['Matched Skills']}/{row['Required Skills']} skills)")
                else:
                    st.error(f"{row['Job Role']} — {match_pct}% match ({row['Matched Skills']}/{row['Required Skills']} skills)")
            best_match = match_df.iloc[0]
            st.markdown("---")
            st.subheader(f"Your Best Match: {best_match['Job Role']} ({best_match['Match %']}%)")
            best_role_skills = set(job_roles[best_match['Job Role']])
            missing = best_role_skills - found_skills
            if missing:
                st.warning(f"Skills to improve for {best_match['Job Role']}: {', '.join(missing)}")
        else:
            st.warning("Please paste your resume text first!")

elif page == "Recommendation Engine":
    st.title("Personalized Recommendation Engine")
    st.markdown("Get personalized course and career recommendations!")
    st.markdown("---")
    course_recommendations = {
        "Data Analysis": {"course": "Google Data Analytics Certificate", "platform": "Coursera", "duration": "6 months"},
        "Communication": {"course": "Communication Skills for Beginners", "platform": "Coursera", "duration": "1 month"},
        "Project Management": {"course": "Google Project Management Certificate", "platform": "Coursera", "duration": "6 months"},
        "Leadership": {"course": "Leadership Skills", "platform": "LinkedIn Learning", "duration": "2 months"},
        "Microsoft Office Suite": {"course": "Microsoft Office 365 Training", "platform": "Microsoft Learn", "duration": "1 month"},
        "Customer Service": {"course": "Customer Service Fundamentals", "platform": "Coursera", "duration": "1 month"},
        "Problem Solving": {"course": "Critical Thinking and Problem Solving", "platform": "Coursera", "duration": "2 months"},
        "Sales": {"course": "Sales Training: Practical Sales Techniques", "platform": "Udemy", "duration": "1 month"},
        "Time Management": {"course": "Work Smarter Not Harder: Time Management", "platform": "Coursera", "duration": "1 month"},
        "Teamwork": {"course": "Teamwork Skills: Communicating Effectively", "platform": "Coursera", "duration": "1 month"}
    }
    career_paths = {
        "Data Analyst": ["Learn Data Analysis", "Master Excel and SQL",
                        "Learn Power BI or Tableau", "Build Projects", "Apply for Junior Data Analyst"],
        "HR Manager": ["Learn HR Fundamentals", "Get HR Certification",
                      "Practice Recruitment", "Learn Labor Laws", "Apply for HR Executive"],
        "Sales Executive": ["Learn Sales Techniques", "Practice Communication",
                           "Learn CRM Tools", "Build Client Network", "Apply for Sales Associate"],
        "Business Developer": ["Learn Business Strategy", "Master Communication",
                              "Learn Market Research", "Build Network", "Apply for BD Executive"]
    }
    resume_text = st.text_area("Paste your resume text here:",
        height=200, placeholder="Paste your resume content here...")
    target_role = st.selectbox("Select your target job role:",
        ["Data Analyst", "HR Manager", "Sales Executive", "Business Developer"])
    if st.button("Get My Recommendations", type="primary"):
        if resume_text:
            found_skills = set(extract_skills(resume_text))
            market_top20 = set(top_skills_df['skill'].head(20).tolist())
            missing_skills = market_top20 - found_skills
            st.markdown("---")
            st.subheader("Recommended Courses for You")
            recommended = []
            for skill in missing_skills:
                if skill in course_recommendations:
                    recommended.append((skill, course_recommendations[skill]))
            if recommended:
                for skill, details in recommended[:5]:
                    with st.expander(f"Learn {skill}"):
                        st.write(f"Course: {details['course']}")
                        st.write(f"Platform: {details['platform']}")
                        st.write(f"Duration: {details['duration']}")
            else:
                st.success("Great! You have all the top market skills!")
            st.markdown("---")
            st.subheader(f"Career Path to become {target_role}")
            if target_role in career_paths:
                for i, step in enumerate(career_paths[target_role], 1):
                    st.info(f"Step {i}: {step}")
            st.markdown("---")
            st.subheader("Your Skills Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Skills You Have", len(found_skills))
            col2.metric("Market Skills Matched", len(market_top20 & found_skills))
            col3.metric("Skills to Learn", len(missing_skills))
        else:
            st.warning("Please paste your resume text first!")

st.markdown("---")
st.markdown("Built by Awantika Shivhare | AI Skill Gap Analyzer | Python + SQL + NLP + Power BI")