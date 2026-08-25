# ==========================================================
# CODING PRACTICE QUESTIONS DATABASE
# ==========================================================

CODING_QUESTIONS = [

    # ======================================================
    # EASY QUESTIONS
    # ======================================================

    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "description": """
Given an array of integers nums and an integer target,
return indices of the two numbers such that they add up to target.

You may assume that each input has exactly one solution.
""",
        "examples": """
Input:
nums = [2,7,11,15]
target = 9

Output:
[0,1]
""",
        "constraints": """
1 <= nums.length <= 10^4
""",
        "test_cases": [
            {
                "input": {
                    "nums":[2,7,11,15],
                    "target":9
                },
                "output":[0,1]
            }
        ]
    },


    {
        "id": 2,
        "title": "Palindrome Number",
        "difficulty": "Easy",
        "description": """
Given an integer x, return true if x is a palindrome,
and false otherwise.
""",
        "examples": """
Input:
121

Output:
True
""",
        "constraints": """
-2^31 <= x <= 2^31-1
""",
        "test_cases":[
            {
                "input":{
                    "x":121
                },
                "output":True
            }
        ]
    },


    {
        "id":3,
        "title":"Reverse String",
        "difficulty":"Easy",
        "description":"""
Write a function that reverses a string.
""",
        "examples":"""
Input:
["h","e","l","l","o"]

Output:
["o","l","l","e","h"]
""",
        "constraints":"""
1 <= s.length <= 10^5
""",
        "test_cases":[
            {
                "input":{
                    "s":["h","e","l","l","o"]
                },
                "output":["o","l","l","e","h"]
            }
        ]
    },


    {
        "id":4,
        "title":"Valid Parentheses",
        "difficulty":"Easy",
        "description":"""
Given a string containing brackets,
determine if the input string is valid.
""",
        "examples":"""
Input:
"()"

Output:
True
""",
        "constraints":"""
1 <= length <= 10^4
""",
        "test_cases":[
            {
                "input":{
                    "s":"()"
                },
                "output":True
            }
        ]
    },


    {
        "id":5,
        "title":"Maximum Subarray",
        "difficulty":"Easy",
        "description":"""
Find the contiguous subarray which has the largest sum.
""",
        "examples":"""
Input:
[-2,1,-3,4,-1,2,1,-5,4]

Output:
6
""",
        "constraints":"""
1 <= nums.length <= 10^5
""",
        "test_cases":[
            {
                "input":{
                    "nums":[-2,1,-3,4,-1,2,1,-5,4]
                },
                "output":6
            }
        ]
    },


    {
        "id":6,
        "title":"Best Time To Buy Stock",
        "difficulty":"Easy",
        "description":"""
Find maximum profit from buying and selling stock.
""",
        "examples":"""
Input:
[7,1,5,3,6,4]

Output:
5
""",
        "constraints":"",
        "test_cases":[
            {
                "input":{
                    "prices":[7,1,5,3,6,4]
                },
                "output":5
            }
        ]
    },


    {
        "id":7,
        "title":"Fizz Buzz",
        "difficulty":"Easy",
        "description":"""
Return Fizz for multiples of 3,
Buzz for multiples of 5.
""",
        "examples":"",
        "constraints":"",
        "test_cases":[
            {
                "input":{
                    "n":3
                },
                "output":["1","2","Fizz"]
            }
        ]
    },


    {
        "id":8,
        "title":"Search Insert Position",
        "difficulty":"Easy",
        "description":"""
Find the index where target should be inserted.
""",
        "examples":"",
        "constraints":"",
        "test_cases":[
            {
                "input":{
                    "nums":[1,3,5,6],
                    "target":5
                },
                "output":2
            }
        ]
    },


    {
        "id":9,
        "title":"Move Zeroes",
        "difficulty":"Easy",
        "description":"",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":10,
        "title":"Contains Duplicate",
        "difficulty":"Easy",
        "description":"",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":11,
        "title":"Missing Number",
        "difficulty":"Easy",
        "description":"",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":12,
        "title":"Climbing Stairs",
        "difficulty":"Easy",
        "description":"",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },
    # ======================================================
    # MEDIUM QUESTIONS
    # ======================================================


    {
        "id":13,
        "title":"Add Two Numbers",
        "difficulty":"Medium",
        "description":"Add two numbers represented by linked lists.",
        "examples":"Input: l1=[2,4,3], l2=[5,6,4]\nOutput:[7,0,8]",
        "constraints":"1 <= nodes <= 100",
        "test_cases":[]
    },


    {
        "id":14,
        "title":"Longest Substring Without Repeating Characters",
        "difficulty":"Medium",
        "description":"Find the length of the longest substring without repeating characters.",
        "examples":"Input: abcabcbb\nOutput:3",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":15,
        "title":"Container With Most Water",
        "difficulty":"Medium",
        "description":"Find maximum water container area.",
        "examples":"Input:[1,8,6,2,5,4,8,3,7]\nOutput:49",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":16,
        "title":"3Sum",
        "difficulty":"Medium",
        "description":"Find all unique triplets whose sum is zero.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":17,
        "title":"Merge Intervals",
        "difficulty":"Medium",
        "description":"Merge all overlapping intervals.",
        "examples":"Input:[[1,3],[2,6],[8,10]]\nOutput:[[1,6],[8,10]]",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":18,
        "title":"Group Anagrams",
        "difficulty":"Medium",
        "description":"Group strings that are anagrams.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":19,
        "title":"Product of Array Except Self",
        "difficulty":"Medium",
        "description":"Return array where each element is product of all elements except itself.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":20,
        "title":"Search in Rotated Sorted Array",
        "difficulty":"Medium",
        "description":"Search target in rotated sorted array.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":21,
        "title":"Maximum Product Subarray",
        "difficulty":"Medium",
        "description":"Find maximum product contiguous subarray.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":22,
        "title":"Coin Change",
        "difficulty":"Medium",
        "description":"Find minimum coins required for amount.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":23,
        "title":"House Robber",
        "difficulty":"Medium",
        "description":"Find maximum money without robbing adjacent houses.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":24,
        "title":"Number of Islands",
        "difficulty":"Medium",
        "description":"Count number of islands in a grid.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },



    # ======================================================
    # HARD QUESTIONS
    # ======================================================


    {
        "id":25,
        "title":"Merge k Sorted Lists",
        "difficulty":"Hard",
        "description":"Merge k sorted linked lists.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":26,
        "title":"Trapping Rain Water",
        "difficulty":"Hard",
        "description":"Calculate trapped rain water.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":27,
        "title":"Median of Two Sorted Arrays",
        "difficulty":"Hard",
        "description":"Find median of two sorted arrays.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":28,
        "title":"Longest Valid Parentheses",
        "difficulty":"Hard",
        "description":"Find longest valid parentheses substring.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":29,
        "title":"Regular Expression Matching",
        "difficulty":"Hard",
        "description":"Implement regex matching.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":30,
        "title":"Word Ladder",
        "difficulty":"Hard",
        "description":"Find shortest transformation sequence.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":31,
        "title":"N Queens",
        "difficulty":"Hard",
        "description":"Place N queens on chess board.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":32,
        "title":"Sudoku Solver",
        "difficulty":"Hard",
        "description":"Solve Sudoku puzzle.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":33,
        "title":"Serialize and Deserialize Binary Tree",
        "difficulty":"Hard",
        "description":"Convert binary tree to string and back.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":34,
        "title":"Alien Dictionary",
        "difficulty":"Hard",
        "description":"Find ordering of alien language.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":35,
        "title":"Largest Rectangle in Histogram",
        "difficulty":"Hard",
        "description":"Find largest rectangle area.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    },


    {
        "id":36,
        "title":"Minimum Window Substring",
        "difficulty":"Hard",
        "description":"Find smallest substring containing all characters.",
        "examples":"",
        "constraints":"",
        "test_cases":[]
    }

]
