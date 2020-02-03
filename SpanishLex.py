
from re import UNICODE as RE_UNICODE
import ply.lex as lex




# Prints an error output for illegal token
def token_error(t):
    print("Illegal character  in line ")
          
    t.lexer.skip(1)


# Track line numbers
def token_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Juicy's reserved keywords
reserved = {
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'imprime': 'IMPRIME',
    'len': 'LEN',
    'to_str': 'TO_STR',
    'err': 'ERR',
    'to_int': 'TO_INT',
    'to_float': 'TO_FLOAT',
    'y': 'AND',
    'o': 'OR',
    'num': 'NUM',
    'texto': 'TEXTO',
    'noes' : 'NOTEQUAL',
}

# Juicy's tokens
tokens = (
             #'NOTEQUAL',
             'GE',
             'LE',
             'ASSIGN',
             'SYMBOL',
             'FLOAT',
             'INT',
             'STRING',
             'IMPRIME',
             'SI'            
         ) + tuple(reserved.values())
#print(tokens)
#t_NOTEQUAL = r'<>'
t_ASSIGN = r':='

literals = (
    '>',
    '<',
    '=',
    '+',
    '-',
    '*',
    '/',
    '^',
    '{',
    '}',
    '[',
    ']',
    '(',
    ')',
    ':',
    ';',
    ',',
)

t_GE = r'>='
t_LE = r'<='

# Read in a float. This rule has to be done before the int rule.
def t_FLOAT(t):
    r'\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t


# Read in an int
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Read in a string, as in C. The following backslash sequences have their usual special meaning: \", \\, \n, and \t
def t_STRING(t):
    r'\"([^\\"]|(\\.))*\"'
    escaped = 0
    # Remove first and last double quotations
    old_str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(old_str)):
        c = old_str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
            else:
                new_str += c
    t.value = new_str
    return t


# Read in a symbol. This rule must be practically last since there are so
# few rules concerning what constitutes a symbol
def t_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # See if symbol is a reserved keyword
    t.type = reserved.get(t.value, 'SYMBOL')
    return t


t_newline = token_newline

t_ignore = ' \t'

t_error = token_error

# Build the lexer
lex.lex(reflags=RE_UNICODE, errorlog=lex.NullLogger())

if __name__ == '__main__':
    lex.runmain()
