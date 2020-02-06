import sys
import ply.yacc as yacc
from SpanishLex import tokens

f = open("log.txt", "w")

def check_int_float_operands(p):
    if p[1] is None or p[3] is None:
        return False

    if (type(p[1]) not in {int, float}) or (type(p[3]) not in {int, float}):
        print("Operator is only defined for 'int' and 'float'")
        return False

    return True


def boolexpr(expr):
    if expr is None:
        return None

    if type(expr) is str:
        return True if len(expr) > 0 else False

    return True if expr != 0 else False


# A map that contains variables and their values
variables = {}
functions = {}
# Contains the last error number happened in runtime environment
runtime_err = 0
return_stack = []
# A stack containing running states
# It gets used for disabling interpreting in if and while statements
running = [True]
exec_function = [False]
return_pos = []

def get_symbol(p, i):
    if not p[i] in variables:
        print("Variable is not defined")
    else:
        return variables[p[i]]

    return None

precedence = (
    ('right', 'ASSIGN'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('right', 'UMINUS'),  # Unary minus operator
    ('left', 'OR'),
    ('left', 'AND'),
)


# Program's starting point
def p_s(p):
    """s : p"""
    pass


# Program's main body
def p_p(p):
    """
    p : stmt p
      | expr ';' p
      | boolexpr ';' p
      | 
    """
    pass

def p_stmt(p):
    """
    stmt : IMPRIME '(' print_arguments ')' ';'
    """

    if not running[-1]:
        return

    print(p[3])

    return p

def p_print_arguments(p):
    """
    print_arguments : expr ',' print_arguments
                    | boolexpr ',' print_arguments
                    | boolexpr
                    | expr
                    | 
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    if len(p) == 2:
        p[0] = str(p[1])
    else:
        if p[3] is not None and p[1] is not None:
            p[0] = str(p[1]) + p[3]
    return p

def p_stmt_if(p):
    """
    stmt : SI '(' boolexpr ')' '{' ifA p ifB '}'
         | SI '(' boolexpr ')' '{' ifA p ifB '}' SINO '{' ifC p ifB '}' """
    pass


def p_ifA(p):
    """
    ifA :
    """
    global running
    if not running[-1]:
        running.append(False)
    else:
        running.append(p[-3])
    return p

def p_ifB(p):
    """
    ifB :
    """
    global running
    running.pop()

    return p

def p_ifC(p):
    """
    ifC :
    """
    global running
    if not running[-1]:
        running.append(False)
    else:
        running.append(not p[-9])

    return p
def p_stmt_while(p):
    """
    stmt : MIENTRAS '(' boolexpr ')' '{' whileA p whileB '}'
    """
    pass

def p_alv(p):
    """
    expr : SYMBOL '.' ALV '(' expr ')'
    """
    
    if p[1] in variables and type(variables[p[1]]) == list and len(variables[p[1]]) > p[5]:
        del variables[p[1]][p[5]]
    else:
        print("Error: al remover el elemento de ", str(p[1]))
        sys.exit(-1)
    return p

def p_whileA(p):
    """
    whileA :
    """
    global running
    if not running[-1]:
        running.append(False)
    else:
        running.append(p[-3])
    return p

def p_whileB(p):
    """
    whileB :
    """
    global running
    running.pop()

    if running[-1] and p[-5]:
        p.lexer.lexpos = parser.symstack[-7].lexpos

    return p
def p_boolexpr_and(p):
    """
    boolexpr : boolexpr AND boolexpr
             | boolexpr OR boolexpr
    """
    if not running[-1]:
        return

    if p[2] == "y":
        if p[1] is not None and p[3] is not None:
            p[0] = p[1] and p[3]
    elif p[2] == "o":
        if p[1] is not None and p[3] is not None:
            p[0] = p[1] or p[3]
    return p
def p_boolexpr_paran(p):
    """
    boolexpr : '(' boolexpr ')'
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = p[2]
    return p
def p_boolexpr_comparison(p):
    """
    boolexpr : comparison
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    p[0] = True if type(p[1]) is not bool else False
    return p

def p_comparison_gt(p):
    """
    comparison : comparisonA '>' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] > p[3] else False
    return p

def p_comparison_lt(p):
    """
    comparison : comparisonA '<' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] < p[3] else False
    return p

def p_comparison_eq(p):
    """
    comparison : comparisonA '=' expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] == p[3] else False

    return p

def p_comparison_neq(p):
    """
    comparison : comparisonA NOTEQUAL expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] != p[3] else False

    return p

def p_comparison_le(p):
    """
    comparison : comparisonA LE expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] <= p[3] else False

    return p
def p_comparison_ge(p):
    """
    comparison : comparisonA GE expr
    """
    if not running[-1]:
        return

    if p[1] is None or p[3] is None:
        p[0] = None
    else:
        if type(p[1]) is bool:
            p[0] = False
        else:
            p[0] = p[3] if p[1] >= p[3] else False

    return p

def p_comparisonA(p):
    """
    comparisonA : comparison
                | expr
    """
    if not running[-1]:
        return

    p[0] = p[1]

    return p

def p_expr_plus(p):
    """
    expr : expr '+' expr
    """
    if not running[-1]:
        return

    if p[1] is not None and p[3] is not None:
        p[0] = p[1] + p[3]
    return p

def p_expr_minus(p):
    """
    expr : expr '-' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] - p[3]
    return p

def p_expr_mul(p):
    """
    expr : expr '*' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] * p[3]

    return p

def p_expr_div(p):
    """
    expr : expr '/' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] / p[3]
    return p

def p_expr_pow(p):
    """
    expr : expr '^' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = pow(p[1], p[3])

    return p
def p_expr_symbol(p):
    """
    expr : SYMBOL
    """
    if not running[-1]:
        return

    sym_val = get_symbol(p, 1)
    if sym_val is not None:
        p[0] = sym_val

    return p
def p_expr(p):
    """
    expr : INT
         | FLOAT
         | STRING
    """
    if not running[-1]:
        return

    p[0] = p[1]
    return p
def p_get_length(p):
    """
    expr : LEN '(' SYMBOL ')'
    """
    if type(variables[p[3]]) in {str, list}:
        p[0] = len(variables[p[3]])
    else:
        print("Error: No es posible obtener la longitud de un numero en la línea " ,parser.symstack[-1].lineno + 1)
    return p
def p_expr_paran(p):
    """
    expr : '(' expr ')'
    """
    if not running[-1]:
        return

    p[0] = p[2]
    return p

def p_expr_unary_minus(p):
    """
    expr : '-' expr %prec UMINUS
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = -p[2]
    return p


def p_expr_assign(p):
    """
    expr : SYMBOL ASSIGN expr
    """
    if not running[-1]:
        return

    if (isinstance(variables[p[1]], str) and isinstance(p[3], str)):
        variables[p[1]] = p[3]
    elif (isinstance(variables[p[1]], (int, float)) and isinstance(p[3], (int, float))):
        variables[p[1]] = p[3]
    else:
        print("Tipo de variable incorrecto en linea ",  parser.symstack[-1].lineno + 1)
        sys.exit(-1)
    return p
def p_expr_create_no_value(p):
    '''
    expr : TEXTO SYMBOL
          | NUM SYMBOL
    '''
    if not running[-1]:
        return
    if p[1] == 'num':    
        variables[p[2]] = sys.maxsize
        p[0] = None
    elif p[1] == 'texto':
        variables[p[2]] = ""
        p[0] = ""
    return p
def p_expr_create(p):
    """
    expr : TEXTO SYMBOL ASSIGN expr
         | NUM SYMBOL ASSIGN expr
    """
    print("definiendo variable")
    if not running[-1]:
        return
    if( p[1] == 'num' and type(p[4]) in {int,float}) or p[4] == None:    
        variables[p[2]] = p[4]
        p[0] = p[4]
    elif (p[1] == 'texto' and type(p[4]) in {str}):
        if p[4] is not None:
            variables[p[2]] = p[4]
            p[0] = p[4]
    else:
        print("Tipo de variable incorrecto en linea ",  parser.symstack[-1].lineno + 1)
        sys.exit(-1)
    return p
def p_expr_create_arr(p):
    ''' expr : NUM '[' ']' SYMBOL
             | TEXTO '[' ']' SYMBOL
    '''
    if p[1] == "num":
        variables[p[4]] = []
        variables[p[4]].append(sys.maxsize)
    elif p[1] == "texto":
        variables[p[4]] = []
        variables[p[4]].append("FIRST_MIGHTY_STRING")
    return p
def p_expr_arr_append(p):
    '''expr : SYMBOL '.' APPEND '(' expr ')'
    '''
    if p[1] in variables:
        if type(variables[p[1]])==list:
            if isinstance(variables[p[1]][0], str) and isinstance(p[5], str):
                if len(variables[p[1]]) == 1 and variables[p[1]][0] == "FIRST_MIGHTY_STRING":
                    variables[p[1]][0] = p[5]
                else:
                    variables[p[1]].append(p[5])
            elif isinstance(variables[p[1]][0], (int, float)) and isinstance(p[5], (int, float)):
                if len(variables[p[1]]) == 1 and variables[p[1]][0] == sys.maxsize:
                    variables[p[1]][0] = p[5]
                else:
                    variables[p[1]].append(p[5])
            else:
                print("Error: Tipo de dato incorrecto a la hora de agregar a arreglo")
                sys.exit(-1)    
        else:
            print("Error: La variable no es de tipo arreglo")
            sys.exit(-1)
    else:
        print("Error: variable no declarada: ",p[1]," en linea ",parser.symstack[-1].lineno + 1)
        sys.exit(-1)
    return p
def p_expr_arr_get(p):
    '''expr : SYMBOL '.' GET '(' expr ')'
    '''
    if(len(variables[p[1]]) <= p[5]):
        print("Error: indice fuera de rango para " + str(p[1]) + " en la linea " + parser.symstack[-1].lineno + 1 )
    elif (len(variables[p[1]]) == 1 and p[5] == 0):
        #print("Entré a la condición de no hacer nada")
        if (variables[p[1]][p[5]] ==sys.maxsize):
            p[0] = None
        elif (variables[p[1]][p[5]] =="FIRST_MIGHTY_STRING"):
            p[0] = ""
        else:
            p[0] = variables[p[1]][p[5]]
    else:
        p[0] = variables[p[1]][p[5]]


def p_func_def(p):
    '''
        stmt : FUNC SYMBOL '{' funcA p funcB '}'
    '''
    global return_pos
    f.write("\nSOY UNA FUNCION")
    print("soy func main")
    #print(p[4])
    if(len(return_pos)>0):
            print("Regresando a la normalidad: ")
            p.lexer.lexpos = return_pos[-1] -2
            return_pos.pop()
    return p
 
def p_expr_or_empty(p):
    """
    expr_or_empty : expr
                  |
    """
    if not running[-1]:
        return

    if len(p) == 2:
        p[0] = p[1]
    return p

def p_funcA(p):
    """
    funcA :
        
    """
    global running, exec_function
    print("estoy en funcA")
    f.write("soy func A")
    if not p[-2] in functions:
        functions[p[-2]] = parser.symstack[-3].lexpos
        f.write("\nfunctions tiene " +str( functions))
    if not exec_function[-1]:
        running.append(False)
    else:
        running.append(True)
    return p
    
#def p_error(p):
#    if p:
#        print("parsed an error...continuing")
#        p.lexer.lexpos = p.lexer.lexpos +1
#    pass
def p_call_func(p):
    '''
    stmt : LLAMA SYMBOL ';'

    '''
    global return_pos
    print("estoy en llama func")
    f.write("\nDebo llamar a la función")
    f.write("Estoy en la pos" + str(p.lexer.lexpos))
    return_pos.append(p.lexer.lexpos)
    if p[2] in functions:
        f.write("\nLa función " + str(p[2]) + " sí existe y está en el char " + str(functions[p[2]]))
        exec_function.append(True)
        f.write("\nexec function tiene " +str( exec_function))
        #debo cambiar de línea. Este salto no está funcionando. 
        p.lexer.lexpos = functions[p[2]] -2
        print("jejeje")
        #p.parser.restart()
        #parser.lexer.lexpos = functions[p[2]]
        f.write("obj" + str(parser.symstack))
    
        
    return p
def p_funcB(p):
    """
    funcB :
    """
    global running, exec_function, return_pos
    running.pop()
    print("estoy en funcB")
    f.write("\nA running le queda " +str( running))
    f.write("\nsoy func b")
    if exec_function[-1]:
        #p.lexer.lexpos = parser.symstack[-5].lexpos
        f.write("\nMi función se va a ejectuar y está en la linea " +str( p.lexer.lexpos))
        exec_function.pop()
        print("Debo regresar a mi posición original",return_pos[-1] + 1)
        #I must return my parser to the regular state. 
        #sys.exit(-1)
        
    return p

# Build the parser
parser = yacc.yacc(errorlog=yacc.NullLogger())