CREATE DATABASE ai_skill_gap_analyzer;

USE ai_skill_gap_analyzer;

CREATE TABLE jobs (
    job_id INT PRIMARY KEY,
    company VARCHAR(100),
    job_title VARCHAR(100),
    location VARCHAR(100),
    salary DECIMAL(10,2),
    experience_level VARCHAR(50)
);

CREATE TABLE skills (
    skill_id INT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(100)
);

CREATE TABLE resume_skills (
    skill_id INT PRIMARY KEY AUTO_INCREMENT,
    skill_name VARCHAR(100)
);