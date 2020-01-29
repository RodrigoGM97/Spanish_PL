# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:20:54 2020

@author: beto_
"""

import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
        'INT',
        'FLOAT',
        'NAME', #VARIABLE NAMES,
        'PLUS',
        'MINUS',
        'DIVIDE',
        'MULTIPLY',
        'EQUALS'
        ]

t_PLUS = r'\+' #matches name of token. Im defining what is a PLUS to laxer. 
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
#if I were to have two equals, I want the == first. Otherwise ply will ignore it.
t_EQUALS = r'\='
#anything on ignore will not be taken into account. 
t_ignore = r' '

#we need to create functions for int float and name because they are more complex
def t_FLOAT(t): #we put float above integer because otherwise it will check if it is an int first and crash on floats.
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t): #receives a regex
    r'\d+' #any characters that are more than one. 
    t.value = int(t.value) #it literally becomes an int.
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' #regex
    t.type='NAME'
    return t

def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1) #skips this token
    

lexer = lex.lex() #created my lexer.

def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(p[1])

def p_empty(p):
    '''
    empty : 
    '''
    p[0] = None
    
def p_expression(p): #on these strings I need to determine my grammar free sintax
    '''
    expression : expression MULTIPLY expression 
               | expression PLUS expression
               | expression MINUS expression
               | expression DIVIDE expression
    '''
    p[0] = (p[2], p[1], p[3]) #this is to make a read tree of the operations. Might be useful alternative.
def p_expression_int_float(p):
    '''
    expression : INT
                | FLOAT
    '''
    p[0] = p[1]
#Now we need some input. 
#lexer.input("1+2")
lexer.input("abc=1+2")

#NOTE: THE FOLLOWING COMMENT HELPS US IDENTIFY IF OUR REGEX IS OK.
#while True:
#    tok = lexer.token() #this will recognize my tokens one by one. 
#    if not tok:
#        break
#    print(tok)
parser = yacc.yacc()

while True:
    try:
        s=input('')
    except EOFError:
        break
    parser.parse(s)