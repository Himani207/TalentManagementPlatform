# utils/coding_engine.py

import traceback
import ast

from utils.coding_runner import run_code



# ==========================================================
# EXECUTE USER CODE
# ==========================================================

def execute_code(
        code,
        language,
        function_name,
        test_input
):

    try:

        result = run_code(
            code,
            language,
            test_input
        )


        return result



    except Exception as e:

        print(
            traceback.format_exc()
        )


        return {

            "status":"Runtime Error",

            "error_type":
            type(e).__name__,

            "message":
            str(e)

        }





# ==========================================================
# NORMALIZE OUTPUT
# ==========================================================
def normalize(value):

    # If output is string representation of list
    if isinstance(value, str):

        try:
            value = ast.literal_eval(value)

        except:
            pass


    if isinstance(value, list):

        return [
            str(x).lower()
            if isinstance(x, str)
            else x
            for x in value
        ]


    return str(value).lower().replace(" ","")
# ==========================================================
# MAIN JUDGE
# ==========================================================

def judge_solution(
        code,
        language,
        question
):

    function_name = question.get(
        "function_name",
        "solution"
    )


    test_cases = question.get(
        "test_cases",
        []
    )



    if not test_cases:


        return {

            "status":"No Test Cases",

            "message":
            "No test cases available"

        }





    passed = 0



    expected = ""
    actual = ""



    for case in test_cases:



        raw_input = case["input"]



        try:


            test_input = ast.literal_eval(
                raw_input
            )


        except:


            test_input = raw_input






        result = execute_code(

            code,

            language,

            function_name,

            test_input

        )





        # ==========================
        # ERROR HANDLING
        # ==========================


        if result["status"] != "Success":


            return {


                "status":
                result["status"],


                "error_type":
                result.get(
                    "error_type",
                    "Error"
                ),


                "message":
                result.get(
                    "message",
                    ""
                )

            }





        actual = normalize(
            result["output"]
        )


        expected = normalize(
            case["output"]
        )





        if actual == expected:

            passed += 1






    total = len(test_cases)





    if passed == total:


        return {

            "status":
            "Accepted",

            "passed":
            passed,

            "total":
            total,

            "score":
            10

        }





    else:


        return {


            "status":
            "Wrong Answer",


            "passed":
            passed,


            "total":
            total,


            "expected":
            expected,


            "your_output":
            actual

        }