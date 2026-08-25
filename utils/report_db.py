from utils.school_db import get_student_profile

def get_student_report(email):
    profile = get_student_profile(email)

    report = {
        "name": profile.get("name", ""),
        "class": profile.get("class", ""),
        "school": profile.get("school", ""),
        "career": profile.get("career", ""),
        "goal": profile.get("goal", ""),
    }

    return report