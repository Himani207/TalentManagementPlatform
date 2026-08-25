import streamlit as st
import utils.coding_db as coding_db
from utils.coding_engine import judge_solution
# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Coding Problem",
    page_icon="📝",
    layout="wide"
)


# ==========================================================
# LOGIN CHECK
# ==========================================================

if "logged_in" not in st.session_state or not st.session_state.logged_in:

    st.warning("Please login first.")

    st.switch_page(
        "pages/login.py"
    )


email = st.session_state.email



# ==========================================================
# GET QUESTION ID
# ==========================================================

if "question_id" not in st.session_state:

    st.error(
        "No question selected"
    )

    st.stop()



question_id = st.session_state.question_id



# ==========================================================
# LOAD QUESTION
# ==========================================================

question = coding_db.get_question_by_id(
    question_id
)
if not question:

    st.error(
        "Question not found"
    )

    st.stop()



# ==========================================================
# HEADER
# ==========================================================


st.title(
    f"💻 {question['title']}"
)



if question["difficulty"] == "Easy":

    st.success(
        "🟢 Easy"
    )

elif question["difficulty"] == "Medium":

    st.warning(
        "🟡 Medium"
    )

else:

    st.error(
        "🔴 Hard"
    )



st.divider()



# ==========================================================
# PROBLEM STATEMENT
# ==========================================================


st.subheader(
    "📝 Problem Statement"
)


st.write(
    question["description"]
)



st.subheader(
    "Example"
)


st.code(
    question["examples"]
)



st.subheader(
    "📌 Constraints"
)


st.write(
    question["constraints"]
)



st.divider()
# ==========================================================
# CODE EDITOR
# ==========================================================

st.subheader("💻 Write Your Solution")


function_name = question.get(
    "function_name",
    "solution"
)
# ==============================
# LANGUAGE SELECTOR
# ==============================

language = st.selectbox(
    "Select Language",
    [
        "Python",
        "C",
        "C++",
        "Java"
    ]
)


# ==============================
# CODE TEMPLATE
# ==============================

if language == "Python":

    default_code = f"""
def {function_name}(input):

    # Write your code here

    pass
"""


elif language == "C++":

    default_code = """
#include <bits/stdc++.h>
using namespace std;

int main(){

    // Write your code here

    return 0;
}
"""


elif language == "C":

    default_code = """
#include <stdio.h>

int main(){

    // Write your code here

    return 0;
}
"""


elif language == "Java":

    default_code = """
class Solution {

    public static void main(String args[]){

        // Write your code here

    }

}
"""
editor_key = f"editor_{question_id}_{language}"

saved_code = coding_db.get_saved_code(
    email,
    question_id,
    language
)

if saved_code:
    st.session_state[editor_key] = saved_code
elif editor_key not in st.session_state:
    st.session_state[editor_key] = default_code
# Reset button

reset_key = f"reset_{question_id}"


if st.button(
    "🔄 Reset Code",
    key=reset_key,
    use_container_width=True
):

    st.session_state[editor_key] = default_code

    st.rerun()
# ==============================
# CODE EDITOR
# ==============================
code = st.text_area(
    "Write Your Solution",
    value=st.session_state.get(
        editor_key,
        default_code
    ),
    height=300
)
# ==========================================================
# RUN BUTTON
#===========================================================
if st.button(
    "▶ Run Code",
    use_container_width=True
):


    if not code.strip():

        st.warning(
            "⚠ Please write your solution first."
        )

        st.stop()
    coding_db.save_user_code(
        email,
        question_id,
        language,
        code
    )
    result = judge_solution(
        code,
        language,
        question

    )

    if result["status"] == "Accepted":

        st.success("✅ Accepted")

        st.write(
            f"Passed **{result['passed']} / {result['total']}** test cases."
        )

        st.metric(
            "XP Earned",
            f"{result['score']} XP"
        )


    elif result["status"] == "Wrong Answer":

        st.error("❌ Wrong Answer")

        st.write(
            f"✅ Passed : {result['passed']} / {result['total']}"
        )

        st.write("Expected Output")
        st.code(
            result.get(
                "expected",
                "Not available"
            )
        )


        st.write("Your Output")

        st.code(
            result.get(
                "your_output",
                "No output generated"
            )
        )
    elif result["status"] == "Runtime Error":

        st.error(
            "❌ Runtime Error"
        )


        st.write(
            "**Error Type:**",
            result.get(
                "error_type",
                "Runtime Error"
            )
        )


        st.write(
            "**Message:**"
        )


        st.code(
            result.get(
                "message",
                "Unknown Error"
            )
        )


    elif result["status"] == "Time Limit Exceeded":

        st.error(
            "⏱ Time Limit Exceeded"
        )


        st.write(
            result["message"]
        )


    else:

        st.error(
            result["status"]
        )
# ==========================================================
# SUBMIT BUTTON
# ==========================================================
if st.button("Submit"):
    coding_db.save_user_code(
            email,
            question_id,
            language,
            code
        )
    result = judge_solution(
        code,
        language,
        question
    )
    if result["status"] == "Accepted":
        if coding_db.is_solved(email, question_id):
            st.info("✅ You have already solved this question.")
        else:
            coding_db.mark_solved(
                email,
                question_id
            )
        st.balloons()
        st.success(
            f"🎉 Solution Accepted +{result['score']} XP Added"
        )


        st.switch_page(
            "pages/coding.py"
        )
    else:


        st.error(
            "Solve the problem before submitting"
        )



st.divider()

# ==========================================================
# BACK BUTTON
# ==========================================================
c1, c2 = st.columns(2)
with c1:

    if st.button("⬅ Back"):

        st.switch_page("pages/coding.py")

with c2:

    if st.button("➡ Next Question"):

        next_id = question_id + 1

        next_question = coding_db.get_question_by_id(next_id)

        if next_question:

            st.session_state.question_id = next_id

            st.rerun()

        else:

            st.info("No more questions available.")