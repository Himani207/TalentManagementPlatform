# ==========================================================
# SALARY DATASET (LPA)
# ==========================================================

salary_data = {

    "Software Engineer": {
        "0-2": 6,
        "3-5": 10,
        "6-8": 16,
        "9+": 24
    },

    "Python Developer": {
        "0-2": 6,
        "3-5": 11,
        "6-8": 17,
        "9+": 25
    },

    "Java Developer": {
        "0-2": 6,
        "3-5": 10,
        "6-8": 16,
        "9+": 24
    },

    "Frontend Developer": {
        "0-2": 5,
        "3-5": 9,
        "6-8": 15,
        "9+": 22
    },

    "Backend Developer": {
        "0-2": 6,
        "3-5": 11,
        "6-8": 18,
        "9+": 26
    },

    "Full Stack Developer": {
        "0-2": 7,
        "3-5": 13,
        "6-8": 20,
        "9+": 30
    },

    "React Developer": {
        "0-2": 6,
        "3-5": 11,
        "6-8": 18,
        "9+": 27
    },

    "Node.js Developer": {
        "0-2": 6,
        "3-5": 11,
        "6-8": 18,
        "9+": 28
    },

    "DevOps Engineer": {
        "0-2": 8,
        "3-5": 15,
        "6-8": 24,
        "9+": 35
    },

    "Cloud Engineer": {
        "0-2": 8,
        "3-5": 15,
        "6-8": 25,
        "9+": 36
    },

    "AWS Engineer": {
        "0-2": 9,
        "3-5": 16,
        "6-8": 27,
        "9+": 40
    },

    "Data Analyst": {
        "0-2": 5,
        "3-5": 9,
        "6-8": 15,
        "9+": 22
    },

    "Business Analyst": {
        "0-2": 6,
        "3-5": 10,
        "6-8": 16,
        "9+": 24
    },

    "Data Engineer": {
        "0-2": 8,
        "3-5": 14,
        "6-8": 22,
        "9+": 32
    },

    "Data Scientist": {
        "0-2": 10,
        "3-5": 18,
        "6-8": 28,
        "9+": 40
    },

    "Machine Learning Engineer": {
        "0-2": 10,
        "3-5": 18,
        "6-8": 30,
        "9+": 42
    },

    "AI Engineer": {
        "0-2": 12,
        "3-5": 20,
        "6-8": 32,
        "9+": 45
    },

    "Cyber Security Engineer": {
        "0-2": 8,
        "3-5": 15,
        "6-8": 24,
        "9+": 35
    },

    "QA Engineer": {
        "0-2": 5,
        "3-5": 8,
        "6-8": 13,
        "9+": 20
    },

    "Automation Test Engineer": {
        "0-2": 6,
        "3-5": 10,
        "6-8": 16,
        "9+": 24
    },

    "UI UX Designer": {
        "0-2": 5,
        "3-5": 9,
        "6-8": 15,
        "9+": 22
    },

    "Mobile App Developer": {
        "0-2": 7,
        "3-5": 12,
        "6-8": 19,
        "9+": 28
    },

    "Project Manager": {
        "0-2": 10,
        "3-5": 18,
        "6-8": 28,
        "9+": 40
    },

    "Technical Lead": {
        "0-2": 12,
        "3-5": 20,
        "6-8": 32,
        "9+": 45
    }

}


# ==========================================================
# LOCATION BONUS (LPA)
# ==========================================================

location_bonus = {

    "bangalore": 3,

    "bengaluru": 3,

    "hyderabad": 2,

    "pune": 2,

    "gurgaon": 3,

    "gurugram": 3,

    "noida": 2,

    "delhi": 2,

    "mumbai": 2,

    "chennai": 2,

    "kolkata": 1,

    "ahmedabad": 1,

    "remote": 1
}


# ==========================================================
# SKILL BONUS (LPA)
# ==========================================================

skill_bonus = {

    "python": 1,

    "java": 1,

    "c++": 1,

    "react": 1,

    "node": 1,

    "node.js": 1,

    "fastapi": 1,

    "django": 1,

    "flask": 1,

    "sql": 1,

    "mongodb": 1,

    "postgresql": 1,

    "docker": 2,

    "kubernetes": 3,

    "aws": 3,

    "azure": 3,

    "gcp": 3,

    "terraform": 2,

    "jenkins": 2,

    "git": 1,

    "linux": 1,

    "system design": 3,

    "machine learning": 3,

    "deep learning": 3,

    "artificial intelligence": 3,

    "ai": 3
}


# ==========================================================
# EXPERIENCE RANGE
# ==========================================================

def get_experience_range(experience):

    if experience <= 2:
        return "0-2"

    elif experience <= 5:
        return "3-5"

    elif experience <= 8:
        return "6-8"

    else:
        return "9+"
# ==========================================================
# MARKET SALARY CALCULATION
# ==========================================================

def calculate_market_salary(profile):

    # -------------------------
    # Profile Data
    # -------------------------

    role = profile.get(
        "current_role",
        "Software Engineer"
    ).strip()

    experience = int(
        profile.get(
            "experience",
            0
        )
    )

    location = profile.get(
        "location",
        ""
    ).lower()

    leadership = int(
        profile.get(
            "leadership",
            50
        )
    )

    skills = [

        skill.strip().lower()

        for skill in profile.get(
            "technical_skills",
            ""
        ).split(",")

        if skill.strip()

    ]

    certifications = [

        cert.strip()

        for cert in profile.get(
            "certifications",
            ""
        ).split(",")

        if cert.strip()

    ]

    # -------------------------
    # Experience Range
    # -------------------------

    exp_range = get_experience_range(
        experience
    )

    # -------------------------
    # Base Salary
    # -------------------------

    role_data = salary_data.get(

        role,

        salary_data["Software Engineer"]

    )

    salary = role_data[exp_range]

    # -------------------------
    # Location Bonus
    # -------------------------

    for city, bonus in location_bonus.items():

        if city in location:

            salary += bonus

            break

    # -------------------------
    # Skill Bonus
    # -------------------------

    for skill in skills:

        salary += skill_bonus.get(
            skill,
            0
        )

    # -------------------------
    # Certification Bonus
    # -------------------------

    salary += len(certifications) * 0.5

    # -------------------------
    # Leadership Bonus
    # -------------------------

    if leadership >= 90:

        salary += 2

    elif leadership >= 75:

        salary += 1

    elif leadership >= 60:

        salary += 0.5

    # -------------------------
    # Expected Salary
    # -------------------------

    expected_salary = round(
        salary * 1.20,
        1
    )

    # -------------------------
    # Salary Growth %
    # -------------------------

    growth = round(
        ((expected_salary - salary) / salary) * 100,
        1
    )

    # -------------------------
    # Return
    # -------------------------

    return {

        "market_salary": round(salary, 1),

        "expected_salary": expected_salary,

        "growth": growth,

        "skills_count": len(skills),

        "certifications_count": len(certifications)

    }