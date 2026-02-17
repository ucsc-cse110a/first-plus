# Grammar 3: Classic Ambiguous (nullable A)
grammar = {
    "S" : [["A", "a"],
           ["b", "A", "c"],
           ["d", "c"],
           ["b", "d", "a"]],
    "A" : [[]],
}

