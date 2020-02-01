tokens = (
    'NAME','INT', 'FLOAT', 'STRING', 'NUM', 'TEXTO',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN','FOR', 'SI', 'LBRACE', 'RBRACE',
    'EOC', 'LBRACKET', 'RBRACKET', 'APPEND', 'MIENTRAS'
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
    return t

def t_SI(t):
    r'SI'
    return t

def t_NUM(t):
    r'NUM'

    return t

def t_TEXTO(t):
    r'TEXTO'
    return t

def t_APPEND(t):
    r'.agrega'

    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)