from ai.gemini import ask_gemini


def roadmap(goal):

    prompt = f"""
Create a learning roadmap.

Goal:

{goal}

Return:

Week 1

Week 2

Week 3

Week 4

Week 5

Week 6

Projects

Certifications

Interview Preparation
"""

    return ask_gemini(prompt)