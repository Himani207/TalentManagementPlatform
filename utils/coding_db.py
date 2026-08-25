import json
from database import get_connection



# ==========================================================
# CREATE CODING TABLES
# ==========================================================

def create_coding_tables():

    conn = get_connection()
    cursor = conn.cursor()


    # -------------------------------
    # Coding Questions Table
    # -------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coding_questions(

        id INTEGER PRIMARY KEY,

        title TEXT,

        difficulty TEXT,

        topic TEXT,

        description TEXT,

        examples TEXT,

        constraints TEXT,

        test_cases TEXT,

        function_name TEXT DEFAULT 'solution',
        language TEXT DEFAULT 'Python'

    )
    """)



    # -------------------------------
    # Student Progress Table
    # -------------------------------


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coding_progress(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        question_id INTEGER,

        status TEXT DEFAULT 'Not Attempted',

        score INTEGER DEFAULT 0,

        attempts INTEGER DEFAULT 0,


        FOREIGN KEY(question_id)
        REFERENCES coding_questions(id)

    )
    """)



    conn.commit()
    conn.close()





# ==========================================================
# ADD QUESTION
# ==========================================================


def add_question(question):

    conn = get_connection()
    cursor = conn.cursor()



    cursor.execute("""

    INSERT OR REPLACE INTO coding_questions

    (

    id,

    title,

    difficulty,

    topic,

    description,

    examples,

    constraints,

    test_cases,

    function_name,
    language
   

    )


    VALUES (?,?,?,?,?,?,?,?,?,?)

    """,

    (

    question["id"],

    question["title"],

    question["difficulty"],

    question["topic"],

    question["description"],

    question["examples"],

    question["constraints"],

    json.dumps(
        question["test_cases"]
    ),


    question.get(
        "function_name",
        "solution"
    ),
    ",".join(
        question.get(
            "language",
            ["Python"]
        )
    )
    ))



    conn.commit()
    conn.close()
# ==========================================================
# SAVE CODING RESULT
# ==========================================================

def save_coding_result(
        email,
        question_id,
        status,
        score
):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT id, attempts

    FROM coding_progress

    WHERE email=?
    AND question_id=?

    """,
    (
        email,
        question_id
    ))


    data = cursor.fetchone()



    if data:


        cursor.execute("""
        UPDATE coding_progress

        SET
        status=?,
        score=?,
        attempts=?

        WHERE id=?

        """,
        (
            status,
            score,
            data[1] + 1,
            data[0]
        ))


    else:


        cursor.execute("""
        INSERT INTO coding_progress

        (
            email,
            question_id,
            status,
            score,
            attempts
        )

        VALUES (?,?,?,?,?)

        """,
        (
            email,
            question_id,
            status,
            score,
            1
        ))



    conn.commit()
    conn.close()





# ==========================================================
# GET CODING SCORE / XP
# ==========================================================
def get_coding_score(email):

    conn = get_connection()
    cursor = conn.cursor()

    # total coding questions
    cursor.execute("""
        SELECT COUNT(*)
        FROM coding_questions
    """)

    total_questions = cursor.fetchone()[0]


    # solved questions by user
    cursor.execute("""
        SELECT COUNT(*)
        FROM coding_progress
        WHERE email=?
    """,
    (email,))

    solved_questions = cursor.fetchone()[0]


    conn.close()


    if total_questions == 0:
        return 0


    score = int(
        (solved_questions / total_questions) * 100
    )


    return score
# ==========================================================
# GET XP
# ==========================================================


def get_xp(email):

    return get_coding_score(email)





# ==========================================================
# ADD XP
# ==========================================================


def add_xp(email, xp):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    UPDATE coding_progress

    SET score = score + ?

    WHERE email=?

    """,
    (
        xp,
        email
    ))



    conn.commit()
    conn.close()

# ==========================================================
# INSERT DEFAULT QUESTIONS
# ==========================================================
def insert_questions():
    questions = [
        # ================= EASY 1 =================
        {
            "id":1,
            "title":"Two Sum",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find two numbers in an array whose sum equals the target.",
            "examples":"Input: nums=[2,7,11,15], target=9 Output:[0,1]",
            "constraints":"2 <= nums.length <= 10^4",
            "test_cases":[
                {
                    "input":"[2,7,11,15],9",
                    "output":"[0,1]"
                },
                {
                    "input":"[3,2,4],6",
                    "output":"[1,2]"
                }
            ]
        },


        # ================= EASY 2 =================

        {
            "id":2,
            "title":"Reverse String",
            "difficulty":"Easy",
            "topic":"Strings",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Reverse the given string.",
            "examples":"Input: hello Output: olleh",
            "constraints":"1 <= length <= 10^5",
            "test_cases":[
                {
                    "input":"hello",
                    "output":"olleh"
                },
                {
                    "input":"python",
                    "output":"nohtyp"
                }
            ]
        },


        # ================= EASY 3 =================

        {
            "id":3,
            "title":"Palindrome Number",
            "difficulty":"Easy",
            "topic":"Math",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Check whether a number is palindrome.",
            "examples":"Input:121 Output:true",
            "constraints":"-2^31 <= x <= 2^31-1",
            "test_cases":[
                {
                    "input":"121",
                    "output":"true"
                },
                {
                    "input":"123",
                    "output":"false"
                }
            ]
        },


        # ================= EASY 4 =================

        {
            "id":4,
            "title":"Valid Parentheses",
            "difficulty":"Easy",
            "topic":"Stack",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Check if brackets are balanced.",
            "examples":"Input:'()[]{}' Output:true",
            "constraints":"1 <= length <= 10^4",
            "test_cases":[
                {
                    "input":"()[]{}",
                    "output":"true"
                },
                {
                    "input":"(]",
                    "output":"false"
                }
            ]
        },


        # ================= EASY 5 =================

        {
            "id":5,
            "title":"Merge Sorted Array",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Merge two sorted arrays.",
            "examples":"Input:[1,2,3],[2,5,6]",
            "constraints":"Array size <= 200",
            "test_cases":[
                {
                    "input":"[1,2,3],[2,5,6]",
                    "output":"[1,2,2,3,5,6]"
                }
            ]
        },


        # ================= EASY 6 =================

        {
            "id":6,
            "title":"Best Time to Buy and Sell Stock",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find maximum profit from stock prices.",
            "examples":"Input:[7,1,5,3,6,4]",
            "constraints":"1 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"[7,1,5,3,6,4]",
                    "output":"5"
                }
            ]
        },


        # ================= EASY 7 =================

        {
            "id":7,
            "title":"Contains Duplicate",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
                        "function_name":"solution",
            "description":"Check whether array contains duplicate elements.",
            "examples":"Input:[1,2,3,1]",
            "constraints":"1 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"[1,2,3,1]",
                    "output":"true"
                },
                {
                    "input":"[1,2,3]",
                    "output":"false"
                }
            ]
        },


        # ================= EASY 8 =================

        {
            "id":8,
            "title":"Move Zeroes",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Move all zeroes to the end.",
            "examples":"Input:[0,1,0,3,12]",
            "constraints":"1 <= n <= 10^4",
            "test_cases":[
                {
                    "input":"[0,1,0,3,12]",
                    "output":"[1,3,12,0,0]"
                }
            ]
        },


        # ================= EASY 9 =================

        {
            "id":9,
            "title":"Maximum Subarray",
            "difficulty":"Easy",
            "topic":"DP",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find maximum sum contiguous subarray.",
            "examples":"Input:[-2,1,-3,4]",
            "constraints":"1 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"[-2,1,-3,4,-1,2,1,-5,4]",
                    "output":"6"
                }
            ]
        },


        # ================= EASY 10 =================

        {
            "id":10,
            "title":"Remove Duplicates from Sorted Array",
            "difficulty":"Easy",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Remove duplicates from sorted array.",
            "examples":"Input:[1,1,2]",
            "constraints":"1 <= n <= 3*10^4",
            "test_cases":[
                {
                    "input":"[1,1,2]",
                    "output":"2"
                }
            ]
        },


        # ================= EASY 11 =================

        {
            "id":11,
            "title":"Fizz Buzz",
            "difficulty":"Easy",
            "topic":"Math",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Return FizzBuzz sequence.",
            "examples":"Input:5",
            "constraints":"1 <= n <= 10^4",
            "test_cases":[
                {
                    "input":"5",
                    "output":"[1,2,'Fizz',4,'Buzz']"
                }
            ]
        },


        # ================= EASY 12 =================

        {
            "id":12,
            "title":"Search Insert Position",
            "difficulty":"Easy",
            "topic":"Binary Search",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find position where target should be inserted.",
            "examples":"Input:[1,3,5,6], target=5",
            "constraints":"1 <= n <= 10^4",
            "test_cases":[
                {
                    "input":"[1,3,5,6],5",
                    "output":"2"
                },
                {
                    "input":"[1,3,5,6],2",
                    "output":"1"
                }
            ]
        },
        # ================= MEDIUM QUESTIONS =================
        {
            "id":13,
            "title":"Merge Intervals",
            "difficulty":"Medium",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Merge all overlapping intervals.",
            "examples":"Input:[[1,3],[2,6],[8,10]] Output:[[1,6],[8,10]]",
            "constraints":"1 <= intervals.length <= 10^4",
            "test_cases":[
                {
                    "input":"[[1,3],[2,6],[8,10]]",
                    "output":"[[1,6],[8,10]]"
                },
                {
                    "input":"[[1,4],[4,5]]",
                    "output":"[[1,5]]"
                }
            ]
        },


        {
            "id":14,
            "title":"3Sum",
            "difficulty":"Medium",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find all unique triplets whose sum is zero.",
            "examples":"Input:[-1,0,1,2,-1,-4]",
            "constraints":"3 <= nums.length <= 3000",
            "test_cases":[
                {
                    "input":"[-1,0,1,2,-1,-4]",
                    "output":"[[-1,-1,2],[-1,0,1]]"
                }
            ]
        },


        {
            "id":15,
            "title":"Product of Array Except Self",
            "difficulty":"Medium",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Return product of all elements except current index.",
            "examples":"Input:[1,2,3,4]",
            "constraints":"2 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"[1,2,3,4]",
                    "output":"[24,12,8,6]"
                }
            ]
        },


        {
            "id":16,
            "title":"Longest Substring Without Repeating Characters",
            "difficulty":"Medium",
            "topic":"Strings",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find length of longest substring without duplicate characters.",
            "examples":"Input:'abcabcbb'",
            "constraints":"0 <= length <= 5*10^4",
            "test_cases":[
                {
                    "input":"abcabcbb",
                    "output":"3"
                },
                {
                    "input":"bbbbb",
                    "output":"1"
                }
            ]
        },


        {
            "id":17,
            "title":"Group Anagrams",
            "difficulty":"Medium",
            "topic":"Strings",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Group words that are anagrams.",
            "examples":"Input:['eat','tea','tan']",
            "constraints":"1 <= words <= 10^4",
            "test_cases":[
                {
                    "input":"['eat','tea','tan','ate']",
                    "output":"[['eat','tea','ate'],['tan']]"
                }
            ]
        },


        {
            "id":18,
            "title":"Rotate Array",
            "difficulty":"Medium",
            "topic":"Arrays",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Rotate array to right by k steps.",
            "examples":"Input:[1,2,3,4,5], k=2",
            "constraints":"1 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"([1,2,3,4,5],2)",
                    "output":"[4,5,1,2,3]"
                }
            ]
        },


        {
            "id":19,
            "title":"Container With Most Water",
            "difficulty":"Medium",
            "topic":"Two Pointer",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find maximum area of water container.",
            "examples":"Input:[1,8,6,2,5,4,8,3,7]",
            "constraints":"2 <= n <= 10^5",
            "test_cases":[
                {
                    "input":"[1,8,6,2,5,4,8,3,7]",
                    "output":"49"
                }
            ]
        },


        {
            "id":20,
            "title":"Binary Tree Level Order Traversal",
            "difficulty":"Medium",
            "topic":"Trees",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Return level order traversal of binary tree.",
            "examples":"Input:[3,9,20,null,null,15,7]",
            "constraints":"0 <= nodes <= 2000",
            "test_cases":[
                {
                    "input":"[3,9,20,null,null,15,7]",
                    "output":"[[3],[9,20],[15,7]]"
                }
            ]
        },


        {
            "id":21,
            "title":"Number of Islands",
            "difficulty":"Medium",
            "topic":"Graphs",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Count number of islands in a grid.",
            "examples":"Input:grid",
            "constraints":"m,n <= 300",
            "test_cases":[
                {
                    "input":"[['1','1','0'],['1','0','0'],['0','0','1']]",
                    "output":"2"
                }
            ]
        },


        {
            "id":22,
            "title":"Coin Change",
            "difficulty":"Medium",
            "topic":"DP",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find minimum coins required for amount.",
            "examples":"Input:[1,2,5], amount=11",
            "constraints":"1 <= amount <= 10^4",
            "test_cases":[
                {
                    "input":"[1,2,5],11",
                    "output":"3"
                }
            ]
        },


        {
            "id":23,
            "title":"Course Schedule",
            "difficulty":"Medium",
            "topic":"Graphs",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Check if all courses can be completed.",
            "examples":"Input:numCourses=2 prerequisites=[[1,0]]",
            "constraints":"1 <= courses <= 2000",
            "test_cases":[
                {
                    "input":"2,[[1,0]]",
                    "output":"true"
                }
            ]
        },


        {
            "id":24,
            "title":"House Robber",
            "difficulty":"Medium",
            "topic":"DP",
            "language":[
                "Python",
                "C",
                "C++",
                "Java"
            ],
            "function_name":"solution",
            "description":"Find maximum money without robbing adjacent houses.",
            "examples":"Input:[1,2,3,1]",
            "constraints":"1 <= n <= 100",
            "test_cases":[
                {
                    "input":"[1,2,3,1]",
                    "output":"4"
                },
                {
                    "input":"[2,7,9,3,1]",
                    "output":"12"
                }
            ]
        },
        # ================= HARD QUESTIONS =================
        {
            "id":25,
            "title":"Trapping Rain Water",
            "difficulty":"Hard",
            "topic":"Two Pointer",
            "function_name":"solution",
            "description":"Calculate total trapped rain water between bars.",
            "examples":"Input:[0,1,0,2,1,0,1,3,2,1,2,1] Output:6",
            "constraints":"1 <= n <= 2*10^4",
            "test_cases":[
                {
                    "input":"[0,1,0,2,1,0,1,3,2,1,2,1]",
                    "output":"6"
                }
            ]
        },


        {
            "id":26,
            "title":"Median of Two Sorted Arrays",
            "difficulty":"Hard",
            "topic":"Binary Search",
            "function_name":"solution",
            "description":"Find median of two sorted arrays.",
            "examples":"Input:[1,3],[2]",
            "constraints":"0 <= nums.length <= 1000",
            "test_cases":[
                {
                    "input":"[1,3],[2]",
                    "output":"2"
                }
            ]
        },


        {
            "id":27,
            "title":"Word Ladder",
            "difficulty":"Hard",
            "topic":"Graphs",
            "function_name":"solution",
            "description":"Find shortest transformation sequence between words.",
            "examples":"Input:hit,cog",
            "constraints":"Word length <= 10",
            "test_cases":[
                {
                    "input":"('hit','cog',['hot','dot','dog','lot','log','cog'])",
                    "output":"5"
                }
            ]
        },


        {
            "id":28,
            "title":"N Queens",
            "difficulty":"Hard",
            "topic":"Backtracking",
            "function_name":"solution",
            "description":"Place N queens on chess board without attacks.",
            "examples":"Input:n=4",
            "constraints":"1 <= n <= 9",
            "test_cases":[
                {
                    "input":"4",
                    "output":"2"
                }
            ]
        },


        {
            "id":29,
            "title":"Sudoku Solver",
            "difficulty":"Hard",
            "topic":"Backtracking",
            "function_name":"solution",
            "description":"Solve a 9x9 Sudoku puzzle.",
            "examples":"Input:9x9 board",
            "constraints":"Board size 9x9",
            "test_cases":[
                {
                    "input":"[[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,5,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]",
                    "output":"534678912672195348198342567859761423426853791713924856961537284287419635345286179"
                }
            ]
        },


        {
            "id":30,
            "title":"Regular Expression Matching",
            "difficulty":"Hard",
            "topic":"DP",
            "function_name":"solution",
            "description":"Match string using . and * pattern.",
            "examples":"Input:s='aa', p='a*'",
            "constraints":"Length <= 20",
            "test_cases":[
                {
                    "input":"aa,a*",
                    "output":"true"
                },
                {
                    "input":"mississippi,mis*is*p*.",
                    "output":"false"
                }
            ]
        },


        {
            "id":31,
            "title":"Merge k Sorted Lists",
            "difficulty":"Hard",
            "topic":"Linked List",
            "function_name":"solution",
            "description":"Merge k sorted linked lists.",
            "examples":"Input:[[1,4,5],[1,3,4],[2,6]]",
            "constraints":"k <= 10^4",
            "test_cases":[
                {
                    "input":"[[1,4,5],[1,3,4],[2,6]]",
                    "output":"[1,1,2,3,4,4,5,6]"
                }
            ]
        },


        {
            "id":32,
            "title":"Serialize and Deserialize Binary Tree",
            "difficulty":"Hard",
            "topic":"Trees",
            "function_name":"solution",
            "description":"Serialize tree into string and deserialize it.",
            "examples":"Input:[1,2,3,null,null,4,5]",
            "constraints":"Nodes <= 10^4",
            "test_cases":[
                {
                    "input":"[1,2,3,null,null,4,5]",
                    "output":"same tree"
                }
            ]
        },


        {
            "id":33,
            "title":"Longest Valid Parentheses",
            "difficulty":"Hard",
            "topic":"Stack",
            "function_name":"solution",
            "description":"Find longest valid parentheses substring.",
            "examples":"Input:'(()'",
            "constraints":"Length <= 3*10^4",
            "test_cases":[
                {
                    "input":"(()",
                    "output":"2"
                },
                {
                    "input":")()())",
                    "output":"4"
                }
            ]
        },


        {
            "id":34,
            "title":"Edit Distance",
            "difficulty":"Hard",
            "topic":"DP",
            "function_name":"solution",
            "description":"Minimum operations to convert one string to another.",
            "examples":"Input:'horse','ros'",
            "constraints":"Length <= 500",
            "test_cases":[
                {
                    "input":"horse,ros",
                    "output":"3"
                }
            ]
        },


        {
            "id":35,
            "title":"Maximal Rectangle",
            "difficulty":"Hard",
            "topic":"Stack",
            "function_name":"solution",
            "description":"Find largest rectangle containing only 1s.",
            "examples":"Input:binary matrix",
            "constraints":"Rows and columns <= 200",
            "test_cases":[
                {
                    "input":"[['1','0','1'],['1','1','1']]",
                    "output":"3"
                }
            ]
        },


        {
            "id":36,
            "title":"Wildcard Matching",
            "difficulty":"Hard",
            "topic":"DP",
            "function_name":"solution",
            "description":"Match string with wildcard pattern ? and *.",
            "examples":"Input:s='aa',p='*'",
            "constraints":"Length <= 2000",
            "test_cases":[
                {
                    "input":"aa,*",
                    "output":"true"
                },
                {
                    "input":"cb,?a",
                    "output":"false"
                }
            ]
        }
    ]
    for q in questions:
        add_question(q)

# ==========================================================
# GET ALL QUESTIONS
# ==========================================================
def get_questions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        difficulty,
        topic,
        description,
        examples,
        constraints,
        test_cases

    FROM coding_questions

    ORDER BY id
    """)


    rows = cursor.fetchall()

    conn.close()


    questions = []


    for row in rows:

        questions.append({

            "id": row[0],

            "title": row[1],

            "difficulty": row[2],

            "topic": row[3],

            "description": row[4],

            "examples": row[5],

            "constraints": row[6],

            # convert JSON string back to list
            "test_cases": json.loads(row[7])
            if row[7]
            else []

        })


    return questions
# ==========================================================
# COUNT SOLVED QUESTIONS
# ==========================================================

def solved_count(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)

    FROM coding_progress

    WHERE email=?
    AND status='Solved'

    """,
    (email,))


    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0



# ==========================================================
# DIFFICULTY COUNT
# ==========================================================

def difficulty_count(difficulty):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT COUNT(*)

    FROM coding_questions

    WHERE difficulty=?

    """,
    (difficulty,))


    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0



# ==========================================================
# SOLVED BY DIFFICULTY
# ==========================================================

def solved_by_difficulty(email, difficulty):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT COUNT(*)

    FROM coding_progress

    JOIN coding_questions

    ON coding_progress.question_id =
       coding_questions.id


    WHERE coding_progress.email=?

    AND coding_questions.difficulty=?

    AND coding_progress.status='Solved'

    """,
    (
        email,
        difficulty
    ))


    result = cursor.fetchone()

    conn.close()


    return result[0] if result else 0



# ==========================================================
# FILTER QUESTIONS
# ==========================================================

def get_filtered_questions(
        difficulty,
        topic
):

    conn = get_connection()
    cursor = conn.cursor()


    query = """
    SELECT *
    FROM coding_questions
    """

    params = []


    conditions = []


    if difficulty != "All":

        conditions.append(
            "difficulty=?"
        )

        params.append(difficulty)



    # Topic support
    # (Currently topic column is not in your table)
    # Ignore topic filter until topic column is added


    if conditions:

        query += " WHERE " + " AND ".join(conditions)



    cursor.execute(
        query,
        params
    )


    rows = cursor.fetchall()

    conn.close()


    questions=[]


    for row in rows:

        questions.append({

            "id": row[0],
            "title": row[1],
            "difficulty": row[2],
            "description": row[3],
            "example": row[4],
            "constraints": row[5],
            "topic": "Arrays"

        })


    return questions



# ==========================================================
# CHECK QUESTION SOLVED
# ==========================================================

def is_solved(email, question_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT status

    FROM coding_progress

    WHERE email=?

    AND question_id=?

    """,
    (
        email,
        question_id
    ))


    result = cursor.fetchone()


    conn.close()


    if result and result[0]=="Solved":

        return True


    return False



# ==========================================================
# GET SINGLE QUESTION
# ==========================================================
def get_question_by_id(question_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        difficulty,
        description,
        examples,
        constraints,
        topic,
        test_cases,
        function_name
    FROM coding_questions
    WHERE id=?
    """,
    (question_id,))


    row = cursor.fetchone()

    conn.close()


    if row:

        return {
            "id": row[0],
            "title": row[1],
            "difficulty": row[2],
            "description": row[3],
            "examples": row[4],
            "constraints": row[5],
            "topic": row[6],
            "test_cases": json.loads(row[7]) if row[7] else [],
            "function_name": row[8]
        }


    return None
# ==========================================================
# MARK QUESTION SOLVED
# ==========================================================

def mark_solved(email, question_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT id

    FROM coding_progress

    WHERE email=?

    AND question_id=?

    """,
    (
        email,
        question_id
    ))


    result = cursor.fetchone()



    if result:


        cursor.execute("""
        UPDATE coding_progress

        SET status='Solved',
            score=10

        WHERE id=?

        """,
        (result[0],))



    else:


        cursor.execute("""
        INSERT INTO coding_progress
        (
            email,
            question_id,
            status,
            score,
            attempts
        )

        VALUES (?,?,?,?,?)

        """,
        (
            email,
            question_id,
            "Solved",
            10,
            1
        ))



    conn.commit()

    conn.close()
def update_coding_progress_table():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        ALTER TABLE coding_progress
        ADD COLUMN attempts INTEGER DEFAULT 0
        """)

        conn.commit()

    except Exception as e:
        print(e)

    conn.close()
def create_saved_code_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_code(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        question_id INTEGER,

        language TEXT,

        code TEXT,

        UNIQUE(email, question_id, language)

    )
    """)

    conn.commit()
    conn.close()
def save_user_code(email, question_id, language, code):

    print("EMAIL:", email)
    print("QUESTION:", question_id)
    print("LANGUAGE:", language)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO saved_code
    (email, question_id, language, code)
    VALUES (?,?,?,?)
    ON CONFLICT(email, question_id, language)
    DO UPDATE SET code=excluded.code
    """, (
        email,
        question_id,
        language,
        code
    ))

    conn.commit()

    print("Saved Successfully")

    conn.close()
def get_saved_code(email, question_id, language):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
    SELECT code

    FROM saved_code

    WHERE email=?
    AND question_id=?
    AND language=?

    """,
    (
        email,
        question_id,
        language
    ))


    result = cursor.fetchone()

    conn.close()


    if result:
        return result[0]

    return None
