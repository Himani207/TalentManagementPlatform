from ai.gemini import ask_gemini


def career_chat(question, category="General"):

    prompt = f"""
You are TalentSphere Elevate AI.

User Category:
{category}

Answer the following career question professionally.

Question:
{question}

Provide:
1. Clear answer
2. Step-by-step guidance
3. Skills required
4. Helpful resources
"""

    return ask_gemini(prompt)