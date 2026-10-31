import sqlite3
import random
from ai.gemini import ask_gemini
DB_NAME = "talentsphere.db"
# ==========================================================
# DATABASE CONNECTION
# ==========================================================
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
# ==========================================================
# CREATE PROFESSIONAL TABLE
# ==========================================================
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professional_profile(
        email TEXT PRIMARY KEY,

        full_name TEXT,
        phone TEXT,
        location TEXT,

        company TEXT,
        current_role TEXT,
        experience INTEGER,

        technical_skills TEXT,
        soft_skills TEXT,

        leadership INTEGER,

        work_experience TEXT,
        achievements TEXT,
        certifications TEXT,

        career_goal TEXT,
        preferred_role TEXT,

        current_salary INTEGER,

        linkedin TEXT,
        github TEXT
    )
    """)

    conn.commit()
    conn.close()
def migrate_professional_profile():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(professional_profile)")
    columns = {row[1] for row in cursor.fetchall()}

    columns_to_add = {
        "phone": "TEXT",
        "location": "TEXT",
        "company": "TEXT",
        "current_role": "TEXT",
        "experience": "INTEGER DEFAULT 0",
        "technical_skills": "TEXT",
        "soft_skills": "TEXT",
        "leadership": "INTEGER DEFAULT 0",
        "work_experience": "TEXT",
        "achievements": "TEXT",
        "certifications": "TEXT",
        "career_goal": "TEXT",
        "preferred_role": "TEXT",
        "current_salary": "INTEGER DEFAULT 0",
        "linkedin": "TEXT",
        "github": "TEXT"
    }

    for column, column_type in columns_to_add.items():

        if column not in columns:
            cursor.execute(
                f"ALTER TABLE professional_profile "
                f"ADD COLUMN {column} {column_type}"
            )

    conn.commit()
    conn.close()
# ==========================================================
# SAVE PROFESSIONAL PROFILE
# ==========================================================
def save_profile(data):

    # Make sure database structure is updated
    migrate_professional_profile()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO professional_profile(
            email,
            full_name,
            phone,
            location,
            company,
            current_role,
            experience,
            technical_skills,
            soft_skills,
            leadership,
            work_experience,
            achievements,
            certifications,
            career_goal,
            preferred_role,
            current_salary,
            linkedin,
            github
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        data.get("email", ""),
        data.get("full_name", ""),
        data.get("phone", ""),
        data.get("location", ""),
        data.get("company", ""),
        data.get("current_role", ""),
        int(data.get("experience", 0) or 0),
        data.get("technical_skills", ""),
        data.get("soft_skills", ""),
        int(data.get("leadership", 0) or 0),
        data.get("work_experience", ""),
        data.get("achievements", ""),
        data.get("certifications", ""),
        data.get("career_goal", ""),
        data.get("preferred_role", ""),
        int(data.get("current_salary", 0) or 0),
        data.get("linkedin", ""),
        data.get("github", "")
    ))

    conn.commit()
    conn.close()
# ==========================================================
# GET PROFESSIONAL PROFILE
# ==========================================================
def get_profile(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM professional_profile
        WHERE email=?
        """,
        (email,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        profile = dict(row)

        # Make sure all expected fields exist
        defaults = {
            "full_name": "",
            "phone": "",
            "location": "",
            "company": "",
            "current_role": "",
            "experience": 0,
            "technical_skills": "",
            "soft_skills": "",
            "leadership": 0,
            "work_experience": "",
            "achievements": "",
            "certifications": "",
            "career_goal": "",
            "preferred_role": "",
            "current_salary": 0,
            "linkedin": "",
            "github": "",
            "resume_score": 0
        }

        for key, default in defaults.items():
            profile.setdefault(key, default)

        # Clean text values
        text_fields = [
            "full_name",
            "phone",
            "location",
            "company",
            "current_role",
            "technical_skills",
            "soft_skills",
            "work_experience",
            "achievements",
            "certifications",
            "career_goal",
            "preferred_role",
            "linkedin",
            "github"
        ]

        for field in text_fields:
            profile[field] = profile.get(field) or ""

        # Convert numeric values
        profile["experience"] = int(
            profile.get("experience") or 0
        )

        profile["leadership"] = int(
            profile.get("leadership") or 0
        )

        profile["current_salary"] = int(
            profile.get("current_salary") or 0
        )

        profile["resume_score"] = int(
            profile.get("resume_score") or 0
        )

        return profile

    return None
# ==========================================================
# UPDATE PROFESSIONAL PROFILE
# ==========================================================
def update_profile(email, data):
    conn = get_connection()
    cursor = conn.cursor()
    print(data)
    print("Soft Skills:", data.get("soft_skills"))
    cursor.execute("""
        UPDATE professional_profile
        SET
            full_name=?,
            phone=?,
            location=?,
            company=?,
            current_role=?,
            experience=?,
            technical_skills=?,
            soft_skills=?,
            leadership=?,
            work_experience=?,
            achievements=?,
            certifications=?,
            career_goal=?,
            preferred_role=?,
            current_salary=?,
            linkedin=?,
            github=?
        WHERE email=?
    """, (
        data.get("full_name", ""),
        data.get("phone", ""),
        data.get("location", ""),
        data.get("company", ""),
        data.get("current_role", ""),
        int(data.get("experience", 0)),
        data.get("technical_skills", ""),
        data.get("soft_skills", ""),
        int(data.get("leadership", 0)),
        data.get("work_experience", ""),
        data.get("achievements", ""),
        data.get("certifications", ""),
        data.get("career_goal", ""),
        data.get("preferred_role", ""),
        int(data.get("current_salary", 0)),
        data.get("linkedin", ""),
        data.get("github", ""),
        email
    ))

    conn.commit()
    conn.close()
# ==========================================================
# PROFILE COMPLETION
# ==========================================================

def calculate_profile_completion(profile):


    fields=[

        "full_name",
        "company",
        "current_role",
        "experience",
        "technical_skills",
        "career_goal",
        "preferred_role",
        "leadership",
        "work_experience",
        "achievements",
        "certifications"

    ]


    completed=0


    for field in fields:

        if profile.get(field):

            completed +=1


    return int(
        completed/len(fields)*100
    )
# ==========================================================
# SKILL SCORE
# ==========================================================

def calculate_skill_score(profile):
    skills = profile.get(
        "technical_skills",
        ""
    )
    count = len(
        skills.split(",")
    )


    score = count * 12


    if score > 100:

        score=100


    return score
# ==========================================================
# PROMOTION SCORE
# ==========================================================

def calculate_promotion_score(profile):


    score=0


    experience=int(
        profile.get(
            "experience",
            0
        )
    )


    leadership=int(
        profile.get(
            "leadership",
            0
        )
    )


    if experience>=5:

        score +=30

    elif experience>=2:

        score +=20

    else:

        score +=10



    score += leadership*0.4



    skills=len(
        profile.get(
            "technical_skills",
            ""
        ).split(",")
    )


    score += skills*5



    if score>100:

        score=100


    return int(score)




# ==========================================================
# CAREER GROWTH SCORE
# ==========================================================

def calculate_career_growth(profile):


    skill = calculate_skill_score(profile)

    promotion = calculate_promotion_score(profile)


    return int(
        (skill+promotion)/2
    )
# ==========================================================
# SALARY GROWTH
# ==========================================================

def calculate_salary_growth(profile):


    experience=int(
        profile.get(
            "experience",
            0
        )
    )


    skill_score=calculate_skill_score(profile)


    growth = (
        experience*2
        +
        skill_score*0.2
    )


    if growth>60:

        growth=60


    return int(growth)



# ==========================================================
# EXPERIENCE LEVEL
# ==========================================================

def get_experience_level(profile):


    exp=int(
        profile.get(
            "experience",
            0
        )
    )


    if exp<2:

        return "Entry Level"


    elif exp<5:

        return "Mid Level"


    elif exp<10:

        return "Senior Level"


    return "Expert"
# ==========================================================
# JOB MATCHING
# ==========================================================

def get_job_matches(profile):

    jobs = [

        {
            "role": "Full Stack Developer",
            "company": "Microsoft",
            "location": "Bangalore",
            "salary": "$120k - $160k",
            "job_type": "Full Time",
            "experience": 2,
            "skills": [
                "React",
                "JavaScript",
                "Python"
            ],
            "description": "Develop scalable web applications."
        },

        {
            "role": "Backend Developer",
            "company": "Amazon",
            "location": "Hyderabad",
            "salary": "$110k - $150k",
            "job_type": "Full Time",
            "experience": 2,
            "skills": [
                "Python",
                "API",
                "Database"
            ],
            "description": "Build backend services and APIs."
        },

        {
            "role": "AI Engineer",
            "company": "Google",
            "location": "Bangalore",
            "salary": "$130k - $170k",
            "job_type": "Full Time",
            "experience": 3,
            "skills": [
                "Python",
                "Machine Learning",
                "AI"
            ],
            "description": "Develop AI powered solutions."
        }

    ]

    # ======================================================
    # GET USER DATA SAFELY
    # ======================================================

    technical_skills = profile.get("technical_skills", "") or ""

    user_skills = [
        skill.strip().lower()
        for skill in technical_skills.split(",")
        if skill.strip()
    ]

    user_role = (
        profile.get("preferred_role", "") or ""
    ).lower()

    experience = int(
        profile.get("experience", 0) or 0
    )

    # ======================================================
    # CALCULATE MATCH
    # ======================================================

    for job in jobs:

        required_skills = [
            skill.strip().lower()
            for skill in job["skills"]
        ]

        # --------------------------------------------------
        # Skill matching
        # --------------------------------------------------

        matched_skills = len(
            set(user_skills) &
            set(required_skills)
        )

        skill_score = (
            matched_skills /
            len(required_skills)
        ) * 70

        # --------------------------------------------------
        # Role matching
        # --------------------------------------------------

        role_score = 0

        if (
            user_role
            and
            any(
                word in job["role"].lower()
                for word in user_role.split()
            )
        ):
            role_score = 20

        # --------------------------------------------------
        # Experience matching
        # --------------------------------------------------

        experience_score = 0

        if experience >= job["experience"]:
            experience_score = 10

        # --------------------------------------------------
        # Final match score
        # --------------------------------------------------

        job["match"] = min(
            int(
                skill_score +
                role_score +
                experience_score
            ),
            100
        )

    return sorted(
        jobs,
        key=lambda x: x["match"],
        reverse=True
    )
# ==========================================================
# CERTIFICATION RECOMMENDATION
# ==========================================================

def get_certifications(profile):


    skills = profile.get(
        "technical_skills",
        ""
    ).lower()


    certifications=[]


    if "python" in skills:

        certifications.append(
            "Python Institute Certification"
        )


    if "aws" not in skills:

        certifications.append(
            "AWS Certified Solutions Architect"
        )


    if "cloud" not in skills:

        certifications.append(
            "Microsoft Azure Fundamentals"
        )


    if "ai" in skills or "machine learning" in skills:

        certifications.append(
            "Google Machine Learning Certification"
        )


    if "docker" not in skills:

        certifications.append(
            "Docker Certified Associate"
        )


    if len(certifications)==0:

        certifications.append(
            "Advanced Leadership Certification"
        )


    return certifications
# ==========================================================
# INDUSTRY TRENDS
# ==========================================================
def get_industry_trends(profile):

    prompt = f"""
You are an Industry Expert and Career Advisor.

Professional Profile

Current Role:
{profile.get("current_role")}

Company:
{profile.get("company")}

Experience:
{profile.get("experience")} years

Technical Skills:
{profile.get("technical_skills")}

Career Goal:
{profile.get("career_goal")}

Preferred Role:
{profile.get("preferred_role")}

Generate the latest industry trends personalized for this professional.

Include:

1. Top 5 trending technologies related to their skills
2. Current hiring trends
3. Future job opportunities
4. High-demand skills to learn
5. Salary trend
6. AI impact on this career

Return the answer as bullet points.
"""

    try:
        return ask_gemini(prompt)

    except Exception:
        return """
• Generative AI adoption is increasing.
• Cloud Computing continues to grow rapidly.
• Cyber Security demand is increasing.
• Data Engineering remains a high-paying field.
• Full Stack Development continues to be in demand.
"""
# ==========================================================
# FUTURE JOB ROLES
# ==========================================================

def get_future_roles(profile):


    skills = profile.get(
        "technical_skills",
        ""
    ).lower()


    roles=[]


    if "python" in skills:

        roles.append(
            "AI Engineer"
        )


    if "cloud" in skills or "aws" in skills:

        roles.append(
            "Cloud Architect"
        )


    if "javascript" in skills:

        roles.append(
            "Full Stack Developer"
        )


    roles.extend(
        [
            "Technical Lead",
            "Solution Architect",
            "Engineering Manager"
        ]
    )


    return roles



# ==========================================================
# SKILL GAP ANALYSIS
# ==========================================================

def get_skill_gap(profile):
    required_skills=[

        "Python",
        "Cloud Computing",
        "System Design",
        "Communication",
        "Leadership",
        "AI"

    ]
    user_skills=[
        x.strip().lower()
        for x in profile.get(
            "technical_skills",
            ""
        ).split(",")
    ]
    missing=[]


    for skill in required_skills:

        if skill.lower() not in user_skills:

            missing.append(skill)


    return missing
# ==========================================================
# LEARNING ROADMAP
# ==========================================================

def get_learning_roadmap(profile):
    missing = get_skill_gap(profile)
    roadmap=[]
    for skill in missing:

        roadmap.append(
            {
                "skill":skill,
                "duration":"4-8 weeks",
                "priority":"High"
            }
        )


    return roadmap
# ==========================================================
# GEMINI AI CAREER FUNCTIONS
# ==========================================================


def create_professional_prompt(profile):

    return f"""

You are an expert AI Career Coach.

Analyze this professional profile:

Name:
{profile.get('full_name')}

Current Role:
{profile.get('current_role')}

Company:
{profile.get('company')}

Experience:
{profile.get('experience')} years

Technical Skills:
{profile.get('technical_skills')}

Career Goal:
{profile.get('career_goal')}

Preferred Role:
{profile.get('preferred_role')}

Leadership Score:
{profile.get('leadership')}%

Provide professional and personalized guidance.

"""



# ==========================================================
# AI CAREER OBJECTIVE
# ==========================================================

def generate_career_objective(profile):

    prompt = create_professional_prompt(profile)

    prompt += """

Write a professional career objective
for this person.

Keep it suitable for:
- Resume
- LinkedIn
- Professional portfolio

Maximum 4-5 lines.

"""


    try:

        response = ask_gemini(prompt)

        return response


    except Exception:

        return (
            "Experienced professional focused on "
            "continuous learning and career growth."
        )

# ==========================================================
# AI CAREER COACH
# ==========================================================

def generate_ai_career_advice(profile, question):


    prompt = create_professional_prompt(profile)


    prompt += f"""

User Question:

{question}


Give:

1. Career Advice
2. Skills to Improve
3. Certifications
4. Action Plan
5. Timeline


Answer in simple professional language.

"""


    try:

        return ask_gemini(prompt)


    except Exception as e:

        return str(e)
# ==========================================================
# AI INDUSTRY ANALYSIS
# ==========================================================
def generate_industry_analysis(profile):

    prompt = f"""
You are an Industry Expert and Career Advisor.

Professional Profile

Current Role:
{profile.get("current_role")}

Company:
{profile.get("company")}

Experience:
{profile.get("experience")} years

Technical Skills:
{profile.get("technical_skills")}

Soft Skills:
{profile.get("soft_skills")}

Career Goal:
{profile.get("career_goal")}

Preferred Role:
{profile.get("preferred_role")}

Generate a personalized industry report.

Include these sections using Markdown headings:

## 🚀 Trending Technologies

## 💼 Hiring Trends

## 📊 Market Demand

## 💰 Salary Trends

## 🎯 Skills to Learn

## 🏆 Recommended Certifications

## 🤖 AI Impact

## 📅 Outlook for the Next 5 Years

Use bullet points.
Keep the report professional, concise, and personalized.
"""

    try:
        return ask_gemini(prompt)

    except Exception:
        return """
## 🚀 Trending Technologies
- Artificial Intelligence
- Cloud Computing
- Cyber Security

## 💼 Hiring Trends
- Demand for skilled professionals is increasing.

## 📊 Market Demand
- Companies are hiring professionals with modern technical skills.

## 💰 Salary Trends
- AI, Cloud, and Security roles continue to offer strong compensation.

## 🎯 Skills to Learn
- System Design
- Docker
- Kubernetes
- AWS

## 🏆 Recommended Certifications
- AWS Certified Solutions Architect
- Microsoft Azure Fundamentals

## 🤖 AI Impact
- AI is automating repetitive work while increasing demand for advanced technical skills.

## 📅 Outlook for the Next 5 Years
- Strong growth in AI, cloud computing, cybersecurity, and data engineering careers.
"""
# ==========================================================
# AI SKILL GAP ANALYSIS
# ==========================================================

def generate_skill_gap_analysis(profile):


    missing_skills = get_skill_gap(profile)


    prompt = f"""

You are a Skill Gap Analyst.

Professional Skills:

{profile.get('technical_skills')}


Missing Skills:

{missing_skills}


Explain:

1. Why these skills are important
2. Learning priority
3. Best resources
4. Expected career impact


"""


    try:

        return ask_gemini(prompt)


    except Exception as e:

        return str(e)




# ==========================================================
# AI CAREER ROADMAP
# ==========================================================

def generate_career_roadmap(profile):


    prompt = create_professional_prompt(profile)


    prompt += """

Create a personalized career roadmap.

Divide into:

0-3 Months:
Learning goals

3-6 Months:
Projects and certifications

6-12 Months:
Career growth steps

1-3 Years:
Long term career goals


"""


    try:

        return ask_gemini(prompt)


    except Exception as e:

        return str(e)
def generate_promotion_recommendation(profile):

    prompt = f"""
You are an HR Manager and Promotion Evaluation Expert.

Evaluate the following professional profile.

Name: {profile.get("full_name")}
Current Role: {profile.get("current_role")}
Company: {profile.get("company")}
Experience: {profile.get("experience")} years
Technical Skills: {profile.get("technical_skills")}
Soft Skills: {profile.get("soft_skills")}
Leadership: {profile.get("leadership")}
Achievements: {profile.get("achievements")}
Work Experience: {profile.get("work_experience")}
Certifications: {profile.get("certifications")}
Career Goal: {profile.get("career_goal")}
Preferred Role: {profile.get("preferred_role")}

Analyze the profile like an HR manager.

Return ONLY in this format:

Promotion Readiness Score: XX

Promotion Level:
- Excellent / Good / Average / Needs Improvement

Strengths:
- ...

Weaknesses:
- ...

Missing Skills:
- ...

Recommended Certifications:
- ...

Promotion Chances:
- ...

6-Month Action Plan:
- ...

Do not include any extra text.
"""

    try:
        return ask_gemini(prompt)

    except Exception as e:
        return str(e)
# ==========================================================
# PROMOTION READINESS
# ==========================================================

def calculate_promotion_readiness(profile):

    experience = int(profile.get("experience", 0))
    leadership = int(profile.get("leadership", 0))

    skill_score = calculate_skill_score(profile)

    certifications = [
        c.strip()
        for c in (profile.get("certifications") or "").split(",")
        if c.strip()
    ]

    certification_score = min(len(certifications) * 20, 100)

    resume_score = int(profile.get("resume_score", 0))

    if experience >= 10:
        experience_score = 100
    elif experience >= 5:
        experience_score = 80
    elif experience >= 2:
        experience_score = 60
    else:
        experience_score = 40

    promotion_score = int(
        experience_score * 0.30 +
        skill_score * 0.25 +
        leadership * 0.20 +
        certification_score * 0.15 +
        resume_score * 0.10
    )

    return {
        "promotion_score": promotion_score,
        "experience_score": experience_score,
        "skill_score": skill_score,
        "leadership_score": leadership,
        "resume_score": resume_score,
        "certification_score": certification_score,
    }
def create_job_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        job_id TEXT,
        role TEXT,
        company TEXT,
        location TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        job_id TEXT,
        role TEXT,
        company TEXT,
        location TEXT
    )
    """)

    conn.commit()
    conn.close()
def apply_job(email, job_id, role, company, location):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO job_applications
        (email, job_id, role, company, location, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            email,
            job_id,
            role,
            company,
            location,
            "Applied"
        )
    )

    conn.commit()
    conn.close()
def save_job(email, role, company):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO saved_jobs
        (email, role, company)
        VALUES (?, ?, ?)
        """,
        (
            email,
            role,
            company
        )
    )

    conn.commit()
    conn.close()
def get_all_professionals():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM professional_profile
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
def get_total_job_matches():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM job_applications
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
create_table()
migrate_professional_profile()
create_job_tables()
