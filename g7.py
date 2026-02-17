# Rule 1     expression -> expression PLUS term
# Rule 2     expression -> expression MINUS term
# Rule 3     expression -> term
# Rule 4     term -> term TIMES factor
# Rule 5     term -> term DIVIDE factor
# Rule 6     term -> factor
# Rule 7     factor -> NUMBER
# Rule 8     factor -> LPAREN expression RPAREN
grammar = {
        'expression':   [['expression', 'PLUS', 'term'],
                         ['expression', 'MINUS', 'term'],
                         ['term']
                        ],
        'term':         [['term', 'TIMES', 'factor'],
                         ['term', 'DIVIDE', 'factor'],
                         ['factor']
                        ],
        'factor':       [['NUMBER'],
                         ['LPAREN', 'expression', 'RPAREN']
                        ]
}
