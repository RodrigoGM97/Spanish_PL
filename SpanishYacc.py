import ply.yacc as yacc
from SpanishLex import tokens


# Check types for operator and operands
def check_int_float_operands(p):
    # If something is none then it's error has been reported
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
# Contains the last error number happened in runtime environment
runtime_err = 0
# A stack containing running states
# It gets used for disabling interpreting in if and while statements
running = [True]


# Get's a symbol from variables dictionary and shows error if not exists
def get_symbol(p, i):
    # Get symbol's value form variables dictionary
    symbol_val = variables.get(p[i], None)
    # If symbol does not exist
    if symbol_val is None:
        print("Variable is not defined")
    else:
        return symbol_val

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

    if p[3] is not None:
        print(p[3])


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

    # Second rule
    if len(p) == 2:
        p[0] = str(p[1])
    # First rule
    else:
        if p[3] is not None and p[1] is not None:
            p[0] = str(p[1]) + p[3]


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
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push evaluated value as running state
    else:
        running.append(p[-3])


def p_ifB(p):
    """
    ifB :
    """
    global running
    running.pop()


def p_ifC(p):
    """
    ifC :
    """
    global running
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push not(evaluated value) as running state
    else:
        running.append(not p[-9])


def p_stmt_while(p):
    """
    stmt : MIENTRAS '(' boolexpr ')' '{' whileA p whileB '}'
    """
    pass


def p_whileA(p):
    """
    whileA :
    """
    global running
    # If current state is not running
    if not running[-1]:
        running.append(False)
    # Push evaluated value as running state
    else:
        running.append(p[-3])


def p_whileB(p):
    """
    whileB :
    """
    global running
    running.pop()

    if running[-1] and p[-5]:
        p.lexer.lexpos = parser.symstack[-7].lexpos


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

def p_boolexpr_paran(p):
    """
    boolexpr : '(' boolexpr ')'
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = p[2]

def p_boolexpr_comparison(p):
    """
    boolexpr : comparison
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    p[0] = True if type(p[1]) is not bool else False


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


def p_comparisonA(p):
    """
    comparisonA : comparison
                | expr
    """
    if not running[-1]:
        return

    p[0] = p[1]


def p_expr_plus(p):
    """
    expr : expr '+' expr
    """
    if not running[-1]:
        return

    if p[1] is not None and p[3] is not None:
        p[0] = p[1] + p[3]


def p_expr_minus(p):
    """
    expr : expr '-' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] - p[3]


def p_expr_mul(p):
    """
    expr : expr '*' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] * p[3]


def p_expr_div(p):
    """
    expr : expr '/' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = p[1] / p[3]


def p_expr_pow(p):
    """
    expr : expr '^' expr
    """
    if not running[-1]:
        return

    if check_int_float_operands(p):
        p[0] = pow(p[1], p[3])


def p_expr_symbol(p):
    """
    expr : SYMBOL
    """
    if not running[-1]:
        return

    # Get symbol's value
    sym_val = get_symbol(p, 1)
    # If symbol does not exist
    if sym_val is not None:
        p[0] = sym_val


def p_expr(p):
    """
    expr : INT
         | FLOAT
         | STRING
    """
    if not running[-1]:
        return

    p[0] = p[1]


def p_expr_paran(p):
    """
    expr : '(' expr ')'
    """
    if not running[-1]:
        return

    p[0] = p[2]


def p_expr_unary_minus(p):
    """
    expr : '-' expr %prec UMINUS
    """
    if not running[-1]:
        return

    if p[2] is not None:
        p[0] = -p[2]


def p_expr_len(p):
    """
    expr : LEN '(' expr ')'
    """
    if not running[-1]:
        return

    if p[3] is not None:
        if type(p[3]) is str:
            p[0] = len(p[3])
        else:
            print("'len' only accepts string ")


def p_expr_to_str(p):
    """
    expr : TO_STR '(' expr ')'
    """
    if not running[-1]:
        return

    if p[3] is not None:
        p[0] = str(p[3])


def p_expr_err(p):
    """
    expr : ERR '(' ')'
    """
    global runtime_err

    if not running[-1]:
        return

    p[0] = runtime_err


def p_expr_to_int(p):
    """
    expr : TO_INT '(' expr ')'
    """
    global runtime_err

    if not running[-1]:
        return

    if p[3] is not None:
        try:
            p[0] = int(p[3])
        except ValueError:
            runtime_err = 1
        else:
            runtime_err = 0


def p_expr_to_float(p):
    """
    expr : TO_FLOAT '(' expr ')'
    """
    global runtime_err

    if not running[-1]:
        return

    if p[3] is not None:
        try:
            p[0] = float(p[3])
        except ValueError:
            runtime_err = 1
        else:
            runtime_err = 0

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
        print("Not a correct variable type in line",  parser.symstack[-1].lineno + 1)
        exit()

def p_expr_create(p):
    """
    expr : TEXTO SYMBOL ASSIGN expr
         | NUM SYMBOL ASSIGN expr
    """
    if not running[-1]:
        return
    if( p[1] == 'num' and type(p[4]) in {int,float}):
        if p[4] is not None:
            variables[p[2]] = p[4]
            p[0] = p[4]
    elif (p[1] == 'texto' and type(p[4]) in {str}):
        if p[4] is not None:
            variables[p[2]] = p[4]
            p[0] = p[4]
    else:
        print("Not a correct variable type in line",  parser.symstack[-1].lineno + 1)
        exit()

def p_expr_create_arr(p):
    ''' expr : NUM '[' ']' SYMBOL
             | TEXTO '[' ']' SYMBOL
    '''
    if p[1] == "num":
        variables[p[4]] = [0]
    elif p[1] == "texto":
        variables[p[4]] = [""]

def p_expr_arr_append(p):
    '''expr : SYMBOL '.' APPEND '(' expr ')'
    '''
    if p[1] in variables:
        if isinstance(p[1][0], str) and isinstance(p[5], str):
            variables[p[1]].append(p[5])
        elif isinstance(p[1][0], (int, float)) and isinstance(p[5], (int, float)):
            variables[p[1]].append(p[5])            
        else:
            print("Error: Tipo de dato incorrecto a la hora de agregar a arreglo")    
    else:
        print("Error: var b has not been declared")
    

def p_expr_str_subscript(p):
    """
    expr : expr '[' expr_or_empty ':' expr_or_empty ']'
    """
    if not running[-1]:
        return

    if p[1] is None:
        return

    if type(p[1]) is not str:
        print("Value is not subscriptable in line ")
    else:
        if p[3] is not None and type(p[3]) is not int:
            print("Index is not 'int' in line")
            return
        if p[5] is not None and type(p[5]) is not int:
            print("Index is not 'int'")
            return
        # Everything is ok
        else:
            p[0] = p[1][p[3]:p[5]]


def p_expr_or_empty(p):
    """
    expr_or_empty : expr
                  |
    """
    if not running[-1]:
        return

    if len(p) == 2:
        p[0] = p[1]


# Build the parser
parser = yacc.yacc(errorlog=yacc.NullLogger())
