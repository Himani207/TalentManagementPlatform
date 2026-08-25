import subprocess
import tempfile
import os


def run_code(code, language, test_input):


    try:


        # ================= PYTHON =================

        if language == "Python":

            local_scope = {}

            exec(
                code,
                {},
                local_scope
            )


            func = local_scope.get(
                "solution"
            )


            if func is None:

                return {
                    "status":"Runtime Error",
                    "message":"solution function not found"
                }


            if isinstance(test_input,(list, tuple)):

                output = func(*test_input)

            else:

                output = func(test_input)



            return {

                "status":"Success",
                "output":output

            }




        # ================= C =================


        elif language == "C":


            with tempfile.TemporaryDirectory() as d:


                c_file = os.path.join(
                    d,
                    "main.c"
                )


                exe = os.path.join(
                    d,
                    "main.exe"
                )


                open(
                    c_file,
                    "w"
                ).write(code)



                compile_result = subprocess.run(

                    [
                        "gcc",
                        c_file,
                        "-o",
                        exe
                    ],

                    capture_output=True,
                    text=True

                )


                if compile_result.returncode != 0:

                    return {

                        "status":"Runtime Error",

                        "message":
                        compile_result.stderr

                    }



                run_result = subprocess.run(

                    [exe],

                    input=str(test_input),

                    capture_output=True,

                    text=True

                )



                return {

                    "status":"Success",

                    "output":
                    run_result.stdout.strip()

                }





        # ================= C++ =================


        elif language == "C++":


            with tempfile.TemporaryDirectory() as d:


                cpp_file=os.path.join(
                    d,
                    "main.cpp"
                )


                exe=os.path.join(
                    d,
                    "main.exe"
                )


                open(
                    cpp_file,
                    "w"
                ).write(code)



                compile_result=subprocess.run(

                    [
                        "g++",
                        cpp_file,
                        "-o",
                        exe
                    ],

                    capture_output=True,

                    text=True

                )


                if compile_result.returncode !=0:

                    return {

                    "status":"Runtime Error",

                    "message":
                    compile_result.stderr

                    }




                run_result=subprocess.run(

                    [exe],

                    input=str(test_input),

                    capture_output=True,

                    text=True

                )


                return {

                    "status":"Success",

                    "output":
                    run_result.stdout.strip()

                }





        # ================= JAVA =================


        elif language=="Java":


            with tempfile.TemporaryDirectory() as d:


                java_file=os.path.join(
                    d,
                    "Solution.java"
                )


                open(
                    java_file,
                    "w"
                ).write(code)



                compile_result=subprocess.run(

                    [
                        "javac",
                        java_file
                    ],

                    capture_output=True,

                    text=True

                )


                if compile_result.returncode !=0:

                    return {

                    "status":"Runtime Error",

                    "message":
                    compile_result.stderr

                    }




                run_result=subprocess.run(

                    [
                        "java",
                        "-cp",
                        d,
                        "Solution"
                    ],

                    input=str(test_input),

                    capture_output=True,

                    text=True

                )


                return {

                    "status":"Success",

                    "output":
                    run_result.stdout.strip()

                }




        else:


            return {

                "status":"Runtime Error",

                "message":
                "Language not supported"

            }



    except Exception as e:


        return {

            "status":"Runtime Error",

            "message":
            str(e)

        }