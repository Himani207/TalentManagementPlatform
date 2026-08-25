from database import get_connection
# Create tables

def create_job_tables():

    conn = get_connection()
    cursor = conn.cursor()


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


    conn.commit()
    conn.close()



# Save Job
def save_job(email, job_id, role, company, location):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO saved_jobs
        (email, job_id, role, company, location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        email,
        job_id,
        role,
        company,
        location
    ))

    conn.commit()
    conn.close()
# Apply Job
def apply_job(email, job_id, role, company, location):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO job_applications
        (email, job_id, role, company, location, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        job_id,
        role,
        company,
        location,
        "Applied"
    ))

    conn.commit()
    conn.close()
#Cgeck applied

def check_applied(email,job_id):

    conn=get_connection()
    cursor=conn.cursor()


    cursor.execute(
    """
    SELECT *
    FROM job_applications
    WHERE email=? AND job_id=?
    """,
    (
        email,
        job_id
    )
    )


    data=cursor.fetchone()

    conn.close()
    return data is not None
def get_applied_jobs(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, company, location, status
        FROM job_applications
        WHERE email=?
    """, (email,))

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def get_saved_jobs(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, company, location
        FROM saved_jobs
        WHERE email=?
    """, (email,))

    jobs = cursor.fetchall()

    conn.close()

    return jobs