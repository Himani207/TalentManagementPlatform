import random


QUESTION_BANK = [

    {
        "question": "You are given a difficult problem that you have never seen before. What would you most likely do first?",
        "skill": "Problem Solving",
        "options": [
            ("Break the problem into smaller parts and solve it step by step.", 4),
            ("Try to understand the problem and then look for a possible approach.", 3),
            ("Try a few solutions without planning much.", 2),
            ("Wait for someone else to explain the solution.", 1)
        ]
    },

    {
        "question": "When solving a mathematical or logical problem, which approach describes you best?",
        "skill": "Logical Thinking",
        "options": [
            ("I carefully analyze the information and identify logical patterns.", 4),
            ("I usually analyze the problem before making a decision.", 3),
            ("I sometimes use logic but often rely on trial and error.", 2),
            ("I find logical problems difficult to analyze.", 1)
        ]
    },

    {
        "question": "You have an idea for a school project. What would you most likely do?",
        "skill": "Creativity",
        "options": [
            ("Develop an original idea and find a creative way to present it.", 4),
            ("Modify an existing idea and add something new.", 3),
            ("Follow an existing example with small changes.", 2),
            ("Prefer someone else to provide the complete idea.", 1)
        ]
    },

    {
        "question": "You need to learn a completely new technology or topic. What do you do?",
        "skill": "Learning Ability",
        "options": [
            ("Explore it independently through tutorials, practice and projects.", 4),
            ("Learn it using tutorials and ask questions when necessary.", 3),
            ("Learn only what is required for an assignment.", 2),
            ("Avoid learning it unless someone teaches me directly.", 1)
        ]
    },

    {
        "question": "During a group project, one team member is struggling with their task. What would you do?",
        "skill": "Teamwork",
        "options": [
            ("Help them understand the task while making sure the whole team progresses.", 4),
            ("Offer help if I have enough time.", 3),
            ("Focus mainly on completing my own task.", 2),
            ("Leave the problem to the team member.", 1)
        ]
    },

    {
        "question": "You have to explain a difficult concept to a classmate. How would you approach it?",
        "skill": "Communication",
        "options": [
            ("Explain it clearly using simple examples and check whether they understand.", 4),
            ("Explain the main points and answer their questions.", 3),
            ("Give a short explanation without checking their understanding.", 2),
            ("Find it difficult to explain complex ideas to others.", 1)
        ]
    },

    {
        "question": "Your team is working on a project and nobody is taking responsibility for organizing the work. What would you do?",
        "skill": "Leadership",
        "options": [
            ("Take initiative, divide responsibilities and help the team stay on track.", 4),
            ("Suggest a plan and encourage team members to participate.", 3),
            ("Wait until someone else takes responsibility.", 2),
            ("Avoid taking responsibility for the group.", 1)
        ]
    },

    {
        "question": "You have a coding, science or engineering task that requires several attempts before it works. How do you respond?",
        "skill": "Persistence",
        "options": [
            ("Analyze my mistakes, try different approaches and continue until I improve.", 4),
            ("Try again several times and ask for help when needed.", 3),
            ("Try a few times and move on if it becomes difficult.", 2),
            ("Give up quickly when the first attempts fail.", 1)
        ]
    },

    {
        "question": "You receive two different solutions to the same problem. What would you do?",
        "skill": "Critical Thinking",
        "options": [
            ("Compare both solutions using evidence and determine which is more effective.", 4),
            ("Consider the advantages and disadvantages of both solutions.", 3),
            ("Choose the solution that looks easier.", 2),
            ("Choose whichever solution someone else recommends.", 1)
        ]
    },

    {
        "question": "When using a computer or learning programming, how do you usually approach a new task?",
        "skill": "Technical Thinking",
        "options": [
            ("Experiment with the tools, understand how they work and build something.", 4),
            ("Follow documentation or tutorials and practice along the way.", 3),
            ("Use the tools only when required for an assignment.", 2),
            ("Avoid technical tasks whenever possible.", 1)
        ]
    }

]


def get_questions(number=8):

    """
    Return a random set of assessment questions.
    """

    number = min(number, len(QUESTION_BANK))

    return random.sample(
        QUESTION_BANK,
        number
    )