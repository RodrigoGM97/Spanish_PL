from spanishPL_Syntax import *
from spanishPL_Grammar import *

import ply.lex as lex
lexer = lex.lex()

import ply.yacc as yacc
parser = yacc.yacc()
'''
while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    '''
f= open("test_code.mighty","r")
contents =f.read()
    #s = s.split(';')
contents = contents.split(';')
''' for i in s[:-1]:
        i = i+';'
        print("sent to parse: "+i)       
        parser.parse(i)'''

for i in contents[:-1]:
        i = i+';'
        print("sent to parse: "+i)       
        parser.parse(i)
    