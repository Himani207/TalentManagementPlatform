import sqlite3


DB_NAME = "talentsphere.db"


# ---------------------------------
# Create Internship Table
# ---------------------------------

def create_internship_table():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT,

            company TEXT,

            role TEXT,

            duration TEXT,

            internship_type TEXT,

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()



create_internship_table()



# ---------------------------------
# Save Internship
# ---------------------------------

def save_internship(
        email,
        company,
        role,
        duration,
        internship_type,
        description
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO internships
        (
            email,
            company,
            role,
            duration,
            internship_type,
            description
        )

        VALUES (?,?,?,?,?,?)

        """,

        (
            email,
            company,
            role,
            duration,
            internship_type,
            description
        )
    )


    conn.commit()
    conn.close()



# ---------------------------------
# Get Student Internships
# ---------------------------------

def get_internships(email):

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM internships
        WHERE email=?
        ORDER BY id DESC
        """,

        (email,)
    )


    data = cursor.fetchall()


    conn.close()


    return data



# ---------------------------------
# Internship Score Calculation
# ---------------------------------

def get_internship_score(email):

    internships = get_internships(email)


    total = len(internships)



    # No internship
    if total == 0:

        return 0



    # Score based on experience

    score = 0



    for internship in internships:


        duration = internship["duration"]


        if duration == "1 Month":

            score += 20


        elif duration == "2 Months":

            score += 30


        elif duration == "3 Months":

            score += 40


        elif duration == "6 Months":

            score += 50


        elif duration == "12 Months":

            score += 60



    # Maximum score 100

    if score > 100:

        score = 100



    return score