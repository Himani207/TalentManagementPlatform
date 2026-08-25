import sqlite3
DB_NAME = "talentsphere.db"
def calculate_job_matches(
        skills,
        cgpa,
        projects,
        resume_score,
        coding_score,
        location
):

    jobs = [

        {
            "role":"Software Developer",
            "skills":["python","java","c++","dsa"],
            "location":"Remote"
        },

        {
            "role":"Backend Developer",
            "skills":["python","sql","api","database"],
            "location":"Remote"
        },

        {
            "role":"Data Analyst",
            "skills":["python","sql","excel","data"],
            "location":"Hybrid"
        },

        {
            "role":"QA Engineer",
            "skills":["testing","sql","automation"],
            "location":"On-site"
        }

    ]


    student_skills = [
        s.strip().lower()
        for s in skills.split(",")
    ]


    results=[]


    for job in jobs:


        matched_skills = 0


        for skill in job["skills"]:

            if skill in student_skills:
                matched_skills += 1



        skill_score = (
            matched_skills /
            len(job["skills"])
        ) * 100



        project_score = 0


        if projects:

            project_count = len(
                projects.split(",")
            )

            project_score = min(
                project_count * 25,
                100
            )



        cgpa_score = (
            float(cgpa) / 10
        ) * 100



        location_score = 100


        if location.lower() != job["location"].lower():

            location_score = 60



        final_score = round(

            (skill_score * 0.40)
            +
            (resume_score * 0.20)
            +
            (coding_score * 0.20)
            +
            (project_score * 0.10)
            +
            (location_score * 0.10)

        )
        results.append({

            "role":job["role"],

            "match":min(
                final_score,
                100
            ),

            "location":job["location"],

            "skills":job["skills"]

        })
    return sorted(
        results,
        key=lambda x:x["match"],
        reverse=True
    )