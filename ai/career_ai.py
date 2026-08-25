from ai.gemini import ask_gemini
def recommend_career(category, skills, interests):

    prompt = f"""
You are an expert AI Career Counselor.

Category:
{category}

Skills:
{skills}

Interests:
{interests}

Suggest:

1. Best Career
2. Why this career
3. Required Skills
4. Salary
5. Future Scope
6. Top Certifications
7. Learning Resources
"""

    return ask_gemini(prompt)