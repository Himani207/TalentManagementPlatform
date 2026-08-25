QUESTION_BANK = {

# ==========================================================
# 1. Two Sum
# ==========================================================

"Two Sum":{

    "function":"solution",
    "template":"def solution(nums, target):",
    "xp":10,

    "tests":[
        {
            "args":([2,7,11,15],9),
            "expected":[0,1]
        },
        {
            "args":([3,2,4],6),
            "expected":[1,2]
        }
    ]
},


# ==========================================================
# 2. Reverse String
# ==========================================================

"Reverse String":{

    "function":"solution",
    "template":"def solution(s):",
    "xp":10,

    "tests":[
        {
            "args":("hello",),
            "expected":"olleh"
        },
        {
            "args":("python",),
            "expected":"nohtyp"
        }
    ]
},


# ==========================================================
# 3. Palindrome Number
# ==========================================================

"Palindrome Number":{

    "function":"solution",
    "template":"def solution(x):",
    "xp":10,

    "tests":[
        {
            "args":(121,),
            "expected":True
        },
        {
            "args":(123,),
            "expected":False
        },
        {
            "args":(-121,),
            "expected":False
        }
    ]
},


# ==========================================================
# 4. Valid Parentheses
# ==========================================================

"Valid Parentheses":{

    "function":"solution",
    "template":"def solution(s):",
    "xp":10,

    "tests":[
        {
            "args":("()[]{}",),
            "expected":True
        },
        {
            "args":("(]",),
            "expected":False
        }
    ]
},


# ==========================================================
# 5. Merge Sorted Array
# ==========================================================

"Merge Sorted Array":{

    "function":"solution",
    "template":"def solution(nums1, nums2):",
    "xp":10,

    "tests":[
        {
            "args":([1,2,3],[2,5,6]),
            "expected":[1,2,2,3,5,6]
        }
    ]
},


# ==========================================================
# 6. Best Time to Buy and Sell Stock
# ==========================================================

"Best Time to Buy and Sell Stock":{

    "function":"solution",
    "template":"def solution(prices):",
    "xp":10,

    "tests":[
        {
            "args":([7,1,5,3,6,4],),
            "expected":5
        },
        {
            "args":([7,6,4,3,1],),
            "expected":0
        }
    ]
},


# ==========================================================
# 7. Contains Duplicate
# ==========================================================

"Contains Duplicate":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":10,

    "tests":[
        {
            "args":([1,2,3,1],),
            "expected":True
        },
        {
            "args":([1,2,3],),
            "expected":False
        }
    ]
},


# ==========================================================
# 8. Move Zeroes
# ==========================================================

"Move Zeroes":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":10,

    "tests":[
        {
            "args":([0,1,0,3,12],),
            "expected":[1,3,12,0,0]
        }
    ]
},


# ==========================================================
# 9. Maximum Subarray
# ==========================================================

"Maximum Subarray":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":10,

    "tests":[
        {
            "args":([-2,1,-3,4,-1,2,1,-5,4],),
            "expected":6
        }
    ]
},


# ==========================================================
# 10. Remove Duplicates from Sorted Array
# ==========================================================

"Remove Duplicates from Sorted Array":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":10,

    "tests":[
        {
            "args":([1,1,2],),
            "expected":2
        }
    ]
},


# ==========================================================
# 11. Fizz Buzz
# ==========================================================

"Fizz Buzz":{

    "function":"solution",
    "template":"def solution(n):",
    "xp":10,

    "tests":[
        {
            "args":(5,),
            "expected":["1","2","Fizz","4","Buzz"]
        }
    ]
},


# ==========================================================
# 12. Search Insert Position
# ==========================================================

"Search Insert Position":{

    "function":"solution",
    "template":"def solution(nums,target):",
    "xp":10,

    "tests":[
        {
            "args":([1,3,5,6],5),
            "expected":2
        },
        {
            "args":([1,3,5,6],2),
            "expected":1
        }
    ]
},
# ==========================================================
# MEDIUM QUESTIONS
# ==========================================================


"Merge Intervals":{

    "function":"solution",
    "template":"def solution(intervals):",
    "xp":20,

    "tests":[
        {
            "args":([[1,3],[2,6],[8,10]],),
            "expected":[[1,6],[8,10]]
        }
    ]
},


"3Sum":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":20,

    "tests":[
        {
            "args":([-1,0,1,2,-1,-4],),
            "expected":[[-1,-1,2],[-1,0,1]]
        }
    ]
},


"Product of Array Except Self":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":20,

    "tests":[
        {
            "args":([1,2,3,4],),
            "expected":[24,12,8,6]
        }
    ]
},


"Longest Substring Without Repeating Characters":{

    "function":"solution",
    "template":"def solution(s):",
    "xp":20,

    "tests":[
        {
            "args":("abcabcbb",),
            "expected":3
        },
        {
            "args":("bbbbb",),
            "expected":1
        }
    ]
},


"Group Anagrams":{

    "function":"solution",
    "template":"def solution(strs):",
    "xp":20,

    "tests":[
        {
            "args":(["eat","tea","tan","ate"],),
            "expected":[
                ["eat","tea","ate"],
                ["tan"]
            ]
        }
    ]
},


"Rotate Array":{

    "function":"solution",
    "template":"def solution(nums,k):",
    "xp":20,

    "tests":[
        {
            "args":([1,2,3,4,5],2),
            "expected":[4,5,1,2,3]
        }
    ]
},


"Container With Most Water":{

    "function":"solution",
    "template":"def solution(height):",
    "xp":20,

    "tests":[
        {
            "args":([1,8,6,2,5,4,8,3,7],),
            "expected":49
        }
    ]
},


"Binary Tree Level Order Traversal":{

    "function":"solution",
    "template":"def solution(root):",
    "xp":20,

    "tests":[
        {
            "args":([3,9,20,None,None,15,7],),
            "expected":[[3],[9,20],[15,7]]
        }
    ]
},


"Number of Islands":{

    "function":"solution",
    "template":"def solution(grid):",
    "xp":20,

    "tests":[
        {
            "args":([
                ["1","1","0"],
                ["1","0","0"],
                ["0","0","1"]
            ],),
            "expected":2
        }
    ]
},


"Coin Change":{

    "function":"solution",
    "template":"def solution(coins,amount):",
    "xp":20,

    "tests":[
        {
            "args":([1,2,5],11),
            "expected":3
        }
    ]
},


"Course Schedule":{

    "function":"solution",
    "template":"def solution(numCourses,prerequisites):",
    "xp":20,

    "tests":[
        {
            "args":(2,[[1,0]]),
            "expected":True
        }
    ]
},


"House Robber":{

    "function":"solution",
    "template":"def solution(nums):",
    "xp":20,

    "tests":[
        {
            "args":([1,2,3,1],),
            "expected":4
        },
        {
            "args":([2,7,9,3,1],),
            "expected":12
        }
    ]
},



# ==========================================================
# HARD QUESTIONS
# ==========================================================


"Trapping Rain Water":{

    "function":"solution",
    "template":"def solution(height):",
    "xp":30,

    "tests":[
        {
            "args":([0,1,0,2,1,0,1,3,2,1,2,1],),
            "expected":6
        }
    ]
},


"Median of Two Sorted Arrays":{

    "function":"solution",
    "template":"def solution(nums1,nums2):",
    "xp":30,

    "tests":[
        {
            "args":([1,3],[2]),
            "expected":2
        }
    ]
},


"Word Ladder":{

    "function":"solution",
    "template":"def solution(beginWord,endWord,wordList):",
    "xp":30,

    "tests":[
        {
            "args":(
                "hit",
                "cog",
                ["hot","dot","dog","lot","log","cog"]
            ),
            "expected":5
        }
    ]
},


"N Queens":{

    "function":"solution",
    "template":"def solution(n):",
    "xp":30,

    "tests":[
        {
            "args":(4,),
            "expected":2
        }
    ]
},


"Sudoku Solver":{

    "function":"solution",
    "template":"def solution(board):",
    "xp":30,

    "tests":[
        {
            "args":(
                [
                    ["5","3",".",".","7",".",".",".","."],
                    ["6",".",".","1","9","5",".",".","."],
                    [".","9","8",".",".",".",".","6","."],
                    ["8",".",".",".","6",".",".",".","3"],
                    ["4",".",".","8",".","3",".",".","1"],
                    ["7",".",".",".","2",".",".",".","6"],
                    [".","6",".",".",".",".","2","8","."],
                    [".",".",".","4","1","9",".",".","5"],
                    [".",".",".",".","8",".",".","7","9"]
                ],
            ),
            "expected":True
        }
    ]
},


"Regular Expression Matching":{

    "function":"solution",
    "template":"def solution(s,p):",
    "xp":30,

    "tests":[
        {
            "args":("aa","a*"),
            "expected":True
        },
        {
            "args":("mississippi","mis*is*p*."),
            "expected":False
        }
    ]
},


"Merge k Sorted Lists":{

    "function":"solution",
    "template":"def solution(lists):",
    "xp":30,

    "tests":[
        {
            "args":([[1,4,5],[1,3,4],[2,6]],),
            "expected":[1,1,2,3,4,4,5,6]
        }
    ]
},


"Serialize and Deserialize Binary Tree":{

    "function":"solution",
    "template":"def solution(root):",
    "xp":30,

    "tests":[
        {
            "args":([1,2,3,None,None,4,5],),
            "expected":[1,2,3,None,None,4,5]
        }
    ]
},


"Longest Valid Parentheses":{

    "function":"solution",
    "template":"def solution(s):",
    "xp":30,

    "tests":[
        {
            "args":("(()",),
            "expected":2
        },
        {
            "args":(")()())",),
            "expected":4
        }
    ]
},


"Edit Distance":{

    "function":"solution",
    "template":"def solution(word1,word2):",
    "xp":30,

    "tests":[
        {
            "args":("horse","ros"),
            "expected":3
        }
    ]
},


"Maximal Rectangle":{

    "function":"solution",
    "template":"def solution(matrix):",
    "xp":30,

    "tests":[
        {
            "args":([
                ["1","0","1"],
                ["1","1","1"]
            ],),
            "expected":3
        }
    ]
},


"Wildcard Matching":{

    "function":"solution",
    "template":"def solution(s,p):",
    "xp":30,

    "tests":[
        {
            "args":("aa","*"),
            "expected":True
        },
        {
            "args":("cb","?a"),
            "expected":False
        }
    ]
}

}
