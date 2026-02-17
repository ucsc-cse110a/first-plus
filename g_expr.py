# From slides
# 1. Expr  ::= Unit, Expr2
# 2. Expr2 ::= Op Unit Expr2
# 3.       | "": 
# 4. Unit  ::= ‘(‘ Expr ‘)’
# 5:       |    ID
# 6: Op    ::= ‘+’
# 7:       |   ‘*’

# Define grammar
grammar = {
    "Expr"   : [ ["Unit", "Expr2"]],
    "Expr2"  : [ ["Op", "Unit", "Expr2"], 
                 [] ],
    "Unit"   : [ ["(", "Expr", ")"],
                 ["ID"] ],
    "Op"     : [ ["+"], 
                 ["*"] ]
}
