# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS', 'EOC'),
    ('left', 'NUM'),
    )

# dictionary of names
variables = { }
def p_code(t):
    '''
    code : statement
         | statement code
    '''
    #print("I received " + str(t))
def p_statement_expr(t):
    '''statement : empty
                 | condition
                 | assign 
                 | arrayOP 
                 | expression EOC'''
    
    #print(t)

def p_statement_empty(t):
    '''empty : '''
    t[0] = None

def p_assign_existing_var_name(t):
    '''
    assign : NAME EQUALS NAME EOC
    '''
    if t[1] in variables and t[3] in variables:
        #siguiente validación es checar sus conetidos:
        #caso de strings: 
        if variables[t[1]][0] == variables[t[3]][0]:
            #cubre string-string, int-int, float-float, arr-arr
            print("entered to var = var: " + str(variables[t[1]]) + " " + str(t[1]))
            variables[t[1]] = variables[t[3]]
        else:
            print("Cannot assign " + str(variables[t[3]][0]) + " to " + str(variables[t[1]][0]))
    else:
        if not t[1] in variables:
            print("Error: unknown variable " + str(t[1]))
        else:
            print("Error: unknown variable " + str(t[3]))
def p_assign_existing_var(t):
    '''assign : NAME EQUALS expression EOC
    '''
    #we need to distinguish between var types.
    if t[1] in variables:
        
        variables[t[1]] = t[3]    
        print("successfully assigned var value" )
    else:
        print("Error: var " + t[1] + " has not been declared")
def p_statement_assign_with_value(t):
    '''assign : NUM NAME EQUALS expression EOC
              | TEXTO NAME EQUALS string_expression EOC'''
    #print("Asigna: "+str(t[4]))
    if t[2] in variables:
        print("Error: Cannot declare two variables with the same name. Var " + str(t[2]) + " already exists.")
        
    else:
        variables[t[2]] = (str(t[1]),t[4])
        print("Assigned value " + str(t[4]) + " to " + str(t[2]))
def p_statement_assign(t):
    '''assign : NUM NAME EOC
              | TEXTO NAME EOC'''
    #print("Asigna: "+str(t[4]))
    if t[2] in variables:
        print("Error. Cannot declare two variables with the same name. " + str(t[2]) + " already exists.")
    else:
        variables[t[2]] = (str(t[1]),None)
        print("Successfully declared " + str(t[2]))

def p_statement_assign_array(t):
    '''assign : NUM LBRACKET RBRACKET NAME EOC
              | TEXTO LBRACKET RBRACKET NAME EOC'''

    variables[t[4]] = (str(t[1]) + "_ARR" , [])

def p_arrayOP_append(t):
    '''arrayOP : NAME APPEND LPAREN expression RPAREN EOC
               | NAME APPEND LPAREN string_expression RPAREN EOC'''

    if t[1] in variables:
        #My var exists. 
        print("My var does exist. I can append.")
        if (variables[t[1]][0] == "NUM_ARR" and str(t[4]).isnumeric()) or (variables[t[1]][0] == "TEXTO_ARR" and isinstance(t[4], str)):
            variables[t[1]][1].append(t[4])
            print("Appended " + str(t[4]) + " to " + str(t[1]))
        else:
            print("Cannot append " + str(variables[t[1]][0]) + " with " + str(type(t[4])))
    else:
        print("Error: var b has not been declared")
        
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

def p_condition_si(t):
    '''condition : SI LPAREN RPAREN LBRACE code RBRACE EOC
    '''
                

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
        print("Var " + str(t[1]) + " has " + str(t[0]))
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0

def p_error(t):
    print("Syntax error at '%s'" % t.value)