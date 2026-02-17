# Follow tortutre test grammar
# S  → A B C
# A  → a A | ε
# B  → b B | D | ε
# C  → c C | ε
# D  → d | ε
grammar = {
    "S" : [["A", "B", "C"]],
    "A" : [["a", "A"], []],
    "B" : [["b", "B"], ["D"], []],
    "C" : [["c","C"],  []],
    "D" : [["d"],      []],
}
