# Grammar 4: Expression Grammar (with left recursion)
grammar = {
    "E" : [["E", "+", "T"],
           ["T"]],
    "T" : [["T", "*", "F"],
           ["F"]],
    "F" : [["(", "E", ")"],
           ["id"]],
}


