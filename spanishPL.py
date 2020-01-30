tokens = (
    'NAME','INT', 'FLOAT', 'STRING', 'NUM', 'TEXTO',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN','FOR', 'SI', 'LBRACE', 'RBRACE',
    'EOC', 'LBRACKET', 'RBRACKET', 'APPEND'
    )

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING  = r'\"[a-zA-Z0-9_ ]*\"'
t_EOC     = r'\;'

def t_FLOAT(t): #we put float above integer because otherwise it will check if it is an int first and crash on floats.
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_FOR(t):
    r'FOR'
    try:
        print("asdf")
    except ValueError:
        print("ERR")
    return t

def t_SI(t):
    r'SI'
    try:
        print("Entro NUM")
    except ValueError:
        print("ERR")
    return t

def t_NUM(t):
    r'NUM'
    try:
        print("Entro SI sintaxis")
    except ValueError:
        print("ERR")
    return t

def t_TEXTO(t):
    r'TEXTO'
    try:
        print("Entro TEXTO sintaxis")
    except ValueError:
        print("ERR")
    return t

def t_APPEND(t):
    r'.anadefin'
    try:
        print("Entro append sintaxis")
    except ValueError:
        print("ERR")
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

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
    #print("Enter assign")
    print("Asigna: "+str(t[4]))
    variables[t[2]] = t[4]

def p_statement_assign_array(t):
    '''assign : NUM LBRACKET RBRACKET NAME EOC statement
              | TEXTO LBRACKET RBRACKET NAME EOC statement'''

    variables[t[4]] = []

def p_arrayOP_append(t):
    '''arrayOP : NUM NAME APPEND LPAREN expression RPAREN EOC statement
               | TEXTO NAME APPEND LPAREN string_expression RPAREN EOC statement'''

    print("append: "+str(t[5]))
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

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    s = s.split(';')
    print(s)
    for i in s[:-1]:
        i = i+';'
        print("sent to parse: "+i)       
        parser.parse(i)
    