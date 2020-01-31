from spanishPL_Syntax import *
from spanishPL_Grammar import *

import ply.lex as lex
lexer = lex.lex()
import sys
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
#contents = contents.split(';')
#print("new contents: " + str(contents))
open_bracket_count=0
check_for_brackets = False
parsed_contents = []
new_contents = []
print(contents)
#print("*********starting cycle ****************")
#i = 0
#while( i <len(contents)):
#    print("+++++++++my i is " + str(i) + "+++++++++")
#    temp_string = ""
#    if '{' in contents[i]:
#        check_for_brackets=True
#    else:
#        temp_string = contents[i] + ';'
#    while( check_for_brackets):
#        print("contents in [i] has " + str(contents[i]))
#        print("My x is " + str(i))
#        print("*******************************************")
#        if(i>=len(contents)):
#            print("ERROR IN CODE. BRACKET NOT CLOSED")
#            sys.exit(-1)
#        if('}' in contents[i]):
#            open_bracket_count-= contents[i].count('}')
#            print("closed bracket count is now " + str(open_bracket_count))
#        if('{' in contents[i]):
#            open_bracket_count+= contents[i].count('{')
#            print("added bracket. count is now " + str(open_bracket_count))
#        if(open_bracket_count == 0):
#            check_for_brackets=False
#            
#        if(check_for_brackets):   
#            temp_string = temp_string + contents[i] + ';'
#        else:
#            temp_string = temp_string + contents[i]
#        i+=1
#        print("My is added to " + str(i))
#    print("My temp string has " + temp_string)
#    parsed_contents.append(temp_string)
#    print("parsed contents now has " + str(parsed_contents))
#    i+=1
#        
#            
#        if condition then
#            
#        end if;

parser.parse(contents)
            
''' for i in s[:-1]:
        i = i+';'
        print("sent to parse: "+i)       
        parser.parse(i)'''
#
#for i in contents:
#        i = i+ ';'
#        print("sent to parse: "+i)       
#        parser.parse(i)
#    