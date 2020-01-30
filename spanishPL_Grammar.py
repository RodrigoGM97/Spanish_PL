# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS', 'EOC'),
    ('left', 'NUM'),
    )

# dictionary of names
variables = { }

def p_statement_expr(t):
    '''statement : empty
                 | assign
                 | arrayOP
                 | expression EOC statement'''
    
    #print(t)

def p_statement_empty(t):
    '''empty : '''
    t[0] = None

def p_statement_assign(t):
    '''assign : NUM NAME EQUALS expression EOC statement
              | TEXTO NAME EQUALS string_expression EOC statement'''
    #print("Asigna: "+str(t[4]))
    variables[t[2]] = t[4]

def p_statement_assign_array(t):
    '''assign : NUM LBRACKET RBRACKET NAME EOC statement
              | TEXTO LBRACKET RBRACKET NAME EOC statement'''

    variables[t[4]] = []

def p_arrayOP_append(t):
    '''arrayOP : NUM NAME APPEND LPAREN expression RPAREN EOC statement
               | TEXTO NAME APPEND LPAREN string_expression RPAREN EOC statement'''

    variables[t[2]].append(t[5])

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_string_expression_binop(t):
    '''string_expression : string_expression PLUS string_expression'''
    if t[2] == '+'  : t[0] = t[1] + t[3]


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]

def p_expression_for(t):
    'expression : FOR INT INT INT'
    print("Entro con "+str(t[1])+" "+str(t[2])+" "+str(t[3])+" ")

def p_expression_si(t):
    'expression : SI LPAREN RPAREN LBRACE statement RBRACE'

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    '''expression : INT
                  | FLOAT'''
    
    t[0] = t[1]

def p_string_expression_string(t):
    '''string_expression : STRING'''   
    if (isinstance(t[1], str)):
        t[0] = t[1][1:-1]


def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = variables[t[1]]
        print(t[0])
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)