import streamlit as st

from utils.professional_sidebar import professional_sidebar
from utils.professional_theme import load_professional_theme
from utils.salary_dataset import calculate_market_salary
from utils.professional_db import (
    calculate_skill_score,
    calculate_promotion_score,
    calculate_salary_growth
)
from utils.salary_dataset import calculate_market_salary

from utils.salary_db import (
    create_salary_table,
    save_salary_history,
    get_salary_history
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Salary Insights",
    page_icon="💰",
    layout="wide"
)

load_professional_theme()

# ==========================================================
# LOAD PROFILE
# ==========================================================

profile = professional_sidebar()

if not profile:
    st.stop()

create_salary_table()

# ==========================================================
# PROFESSIONAL CSS
# ==========================================================

st.markdown("""
<style>

.main-title{
font-size:34px;
font-weight:700;
color:#1F2937;
margin-bottom:5px;
}

.subtitle{
font-size:16px;
color:#6B7280;
margin-bottom:20px;
}

.metric-card{
background:white;
padding:20px;
border-radius:15px;
border:1px solid #E5E7EB;
box-shadow:0 2px 10px rgba(0,0,0,.05);
}

.section-card{
background:white;
padding:25px;
border-radius:15px;
border:1px solid #E5E7EB;
box-shadow:0 4px 12px rgba(0,0,0,.05);
margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class="main-title">
Salary Insights
</div>

<div class="subtitle">
Analyze your current salary, compare it with the estimated market salary and discover opportunities to improve your earning potential.
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================================
# PROFILE DATA
# ==========================================================

experience = int(
    profile.get(
        "experience",
        0
    )
)

skills = [

    skill.strip()

    for skill in profile.get(
        "technical_skills",
        ""
    ).split(",")

    if skill.strip()

]
skill_score = calculate_skill_score(profile)
promotion_score = calculate_promotion_score(profile)
salary_growth = calculate_salary_growth(profile)

# Get salary data from dataset
salary_info = calculate_market_salary(profile)
market_salary = salary_info["market_salary"]
expected_salary = salary_info["expected_salary"]

# Current salary (optional, if stored in profile)
current_salary = float(
    profile.get(
        "current_salary",
        market_salary
    )
)

salary_gap = round(
    market_salary - current_salary,
    1
)
# ==========================================================
# SAVE HISTORY
# ==========================================================

save_salary_history(

    profile["email"],

    current_salary,

    market_salary,

    expected_salary,

    skill_score,

    promotion_score

)

# ==========================================================
# DASHBOARD
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(

        "Current Salary",

        f"₹ {current_salary:.1f} LPA"

    )

with c2:

    st.metric(

        "Market Salary",

        f"₹ {market_salary:.1f} LPA",

        delta=f"{salary_gap:+.1f} LPA"

    )

with c3:

    st.metric(

        "Expected Salary",

        f"₹ {expected_salary:.1f} LPA"

    )

with c4:

    st.metric(

        "Promotion Score",

        f"{promotion_score}%"

    )

# ==========================================================
# SALARY PROGRESS
# ==========================================================

st.divider()

st.subheader("Salary Progress")

progress = min(

    current_salary /

    max(market_salary, 1),

    1.0

)

st.progress(progress)

st.caption(

    f"You currently earn approximately {progress*100:.0f}% of the estimated market salary."

)

# ==========================================================
# PROFILE SUMMARY
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-card">',
    unsafe_allow_html=True
)

st.subheader("Professional Summary")

left, right = st.columns(2)

with left:

    st.write(
        f"**Current Role:** {profile.get('current_role')}"
    )

    st.write(
        f"**Company:** {profile.get('company')}"
    )

    st.write(
        f"**Experience:** {experience} Years"
    )

    st.write(
        f"**Technical Skills:** {len(skills)}"
    )

with right:

    st.write(
        f"**Skill Score:** {skill_score}%"
    )

    st.write(
        f"**Promotion Score:** {promotion_score}%"
    )

    st.write(
        f"**Salary Growth Potential:** +{salary_growth}%"
    )

    st.write(
        f"**Salary Gap:** ₹ {salary_gap:.1f} LPA"
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
# ==========================================================
# SALARY COMPARISON
# ==========================================================

st.divider()

st.subheader("Market Salary Comparison")

comparison_data = {
    "Current Salary": current_salary,
    "Market Salary": market_salary,
    "Expected Salary": expected_salary
}

st.bar_chart(comparison_data)

if current_salary >= market_salary:

    st.success(
        "Your salary is at or above the estimated market salary."
    )

elif current_salary >= market_salary * 0.80:

    st.info(
        "Your salary is close to the market average."
    )

else:

    st.warning(
        "Your salary is below the estimated market salary."
    )


# ==========================================================
# SALARY FORECAST
# ==========================================================

st.divider()

st.subheader("Salary Growth Forecast")

growth_data = {

    "Current": current_salary,

    "1 Year": round(current_salary * 1.10, 1),

    "2 Years": round(current_salary * 1.22, 1),

    "3 Years": round(current_salary * 1.38, 1)

}

st.line_chart(growth_data)


# ==========================================================
# CAREER LEVEL
# ==========================================================

st.divider()

st.subheader("Career Level")

if experience < 2:

    level = "Junior Professional"

elif experience < 5:

    level = "Mid-Level Professional"

elif experience < 8:

    level = "Senior Professional"

else:

    level = "Leadership"

st.metric(
    "Current Level",
    level
)


# ==========================================================
# HIGH VALUE SKILLS
# ==========================================================

st.divider()

st.subheader("High Value Skills")

high_value_skills = {

    "AWS":20,

    "Docker":15,

    "Kubernetes":20,

    "System Design":18,

    "FastAPI":12,

    "React":10,

    "Python":15,

    "AI / ML":25

}

user_skills = [

    skill.lower()

    for skill in skills

]

left,right = st.columns(2)

items = list(high_value_skills.items())

with left:

    for skill,value in items[:4]:

        if skill.lower() in user_skills:

            st.success(
                f"{skill}   (+{value}% Salary Impact)"
            )

        else:

            st.warning(
                f"{skill}   (+{value}% Salary Impact)"
            )

with right:

    for skill,value in items[4:]:

        if skill.lower() in user_skills:

            st.success(
                f"{skill}   (+{value}% Salary Impact)"
            )

        else:

            st.warning(
                f"{skill}   (+{value}% Salary Impact)"
            )


# ==========================================================
# RECOMMENDATIONS
# ==========================================================

st.divider()

st.subheader("Salary Improvement Recommendations")

recommendations = []

if salary_gap > 0:

    recommendations.append(
        "Consider negotiating your salary during your next performance review."
    )

if len(skills) < 6:

    recommendations.append(
        "Expand your technical skill set to increase your market value."
    )

if "aws" not in user_skills:

    recommendations.append(
        "Learning AWS Cloud can significantly improve your salary potential."
    )

if "docker" not in user_skills:

    recommendations.append(
        "Docker is highly valued for backend and DevOps roles."
    )

if "kubernetes" not in user_skills:

    recommendations.append(
        "Kubernetes expertise can increase your earning potential."
    )

if promotion_score < 75:

    recommendations.append(
        "Develop leadership and communication skills for better promotion opportunities."
    )

if experience < 3:

    recommendations.append(
        "Gain more real-world project experience to improve your profile."
    )

if not recommendations:

    recommendations.append(
        "Excellent profile! Continue learning new technologies to maintain your competitive advantage."
    )

for item in recommendations:

    st.info(item)


# ==========================================================
# AI SALARY INSIGHTS
# ==========================================================

st.divider()

st.subheader("AI Salary Insights")

if salary_gap <= 0:

    st.success(
        "Your current salary is competitive with the estimated market salary."
    )

elif salary_gap <= 2:

    st.info(
        f"You are approximately ₹ {salary_gap:.1f} LPA below the market salary. Upskilling and certifications can help bridge this gap."
    )

elif salary_gap <= 5:

    st.warning(
        f"You are approximately ₹ {salary_gap:.1f} LPA below the market salary. Focus on in-demand technologies and impactful projects."
    )

else:

    st.error(
        f"Your salary is approximately ₹ {salary_gap:.1f} LPA below the estimated market value. Consider targeting higher-paying organizations or specialized roles."
    )
# ==========================================================
# SALARY HISTORY
# ==========================================================

st.divider()

st.subheader("Salary History")

history = get_salary_history(profile["email"])

if history:

    history_data = []

    for row in history:

        history_data.append({
            "Current Salary": row["current_salary"],
            "Market Salary": row["market_salary"],
            "Expected Salary": row["expected_salary"]
        })

    st.line_chart(history_data)

    st.markdown("### Previous Salary Records")

    for row in history:

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "Current",
                    f"₹ {row['current_salary']:.1f} LPA"
                )

            with c2:

                st.metric(
                    "Market",
                    f"₹ {row['market_salary']:.1f} LPA"
                )

            with c3:

                st.metric(
                    "Expected",
                    f"₹ {row['expected_salary']:.1f} LPA"
                )

            with c4:

                st.caption(row["created_at"])

else:

    st.info("No salary history available.")
# ==========================================================
# CAREER GROWTH INDEX
# ==========================================================

st.divider()

st.subheader("Career Growth Index")

career_growth = round(
    (skill_score + promotion_score) / 2,
    1
)

st.progress(career_growth / 100)

st.metric(
    "Career Growth",
    f"{career_growth}%"
)

if career_growth >= 90:

    st.success(
        "Outstanding career progression."
    )

elif career_growth >= 75:

    st.info(
        "You are progressing well in your career."
    )

elif career_growth >= 60:

    st.warning(
        "Continue improving your skills and leadership."
    )

else:

    st.error(
        "Focus on upskilling and gaining practical experience."
    )
# ==========================================================
# PROFILE STRENGTH
# ==========================================================

st.divider()

st.subheader("Professional Profile Strength")

strength = 0

strength += skill_score * 0.40
strength += promotion_score * 0.35
strength += min(experience * 5, 25)

strength = min(round(strength), 100)

st.progress(strength / 100)

st.metric(
    "Overall Profile Strength",
    f"{strength}%"
)

if strength >= 90:

    st.success(
        "Excellent professional profile."
    )

elif strength >= 75:

    st.info(
        "Strong profile with good career opportunities."
    )

elif strength >= 60:

    st.warning(
        "Your profile is good but still has room for improvement."
    )

else:

    st.error(
        "Develop more skills and gain industry experience."
    )
# ==========================================================
# FUTURE OPPORTUNITIES
# ==========================================================

st.divider()

st.subheader("Suggested Future Roles")

future_roles = []

role = profile.get(
    "current_role",
    ""
).lower()

if "python" in role:

    future_roles = [
        "Senior Python Developer",
        "Backend Engineer",
        "Software Architect",
        "Engineering Manager"
    ]

elif "frontend" in role:

    future_roles = [
        "Senior Frontend Developer",
        "React Architect",
        "UI Lead",
        "Frontend Manager"
    ]

elif "data" in role:

    future_roles = [
        "Senior Data Scientist",
        "ML Engineer",
        "AI Engineer",
        "Analytics Manager"
    ]

elif "devops" in role:

    future_roles = [
        "Cloud Engineer",
        "Site Reliability Engineer",
        "Infrastructure Architect",
        "DevOps Manager"
    ]

else:

    future_roles = [
        "Senior Software Engineer",
        "Technical Lead",
        "Solution Architect",
        "Engineering Manager"
    ]

for future_role in future_roles:

    st.success(future_role)
# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

st.divider()

report = f"""
Salary Insights Report

Current Role : {profile.get('current_role')}

Experience : {experience} Years

Current Salary : ₹ {current_salary:.1f} LPA

Estimated Market Salary : ₹ {market_salary:.1f} LPA

Expected Salary : ₹ {expected_salary:.1f} LPA

Skill Score : {skill_score}%

Promotion Score : {promotion_score}%

Profile Strength : {strength}%

Career Growth : {career_growth}%

Generated by TalentSphere Elevate
"""

st.download_button(

    "Download Salary Report",

    report,

    file_name="salary_report.txt"

)
# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#6B7280;padding:20px;">
        <b>TalentSphere Elevate</b><br>
        AI-Powered Career Development Platform<br><br>
        Salary Insights • Career Growth • Promotion Analytics
    </div>
    """,
    unsafe_allow_html=True
)