from ai.gemini import ask_gemini


def skill_gap(current, target):

    prompt = f"""
Compare these skills.

Current Skills:

{current}

Target Career:

{target}

Return:

1. Missing Skills

2. Learning Priority

3. Best Courses

4. Practice Projects

5. Timeline

"""

    return ask_gemini(prompt)