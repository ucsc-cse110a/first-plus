# Diagnostic Stress Grammar 6
# S  → A B C D
# A  → a A | ε
# B  → b B | ε
# C  → c | ε
# D  → d D | e
grammar = {
    "S" : [["A", "B", "C", "D"]],
    "A" : [["a", "A"], []],
    "B" : [["b", "B"], []],
    "C" : [["c"],      []],
    "D" : [["d","D"],  []],
}


