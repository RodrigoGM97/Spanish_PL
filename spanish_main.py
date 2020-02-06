from sys import exit, argv, stdin
from SpanishYacc import yacc

# Reading a source file
with open('func.mighty', 'rt', encoding='utf-8') as file:
        source = file.read()
yacc.parse(source)
