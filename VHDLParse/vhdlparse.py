#!/usr/bin/env python3
import re
from ply import lex
from ply import yacc

#https://github.com/dabeaz/ply

source='/storage/Develop/fpga_prog/tang_ws1228_rndled/tang_ws1228_rndled.vhd'
f = open(source, "r")
body = f.read()
f.close()

reserved = (
	'LIBRARY', 'USE', 'ALL', 'ENTITY', 'IS', 'PORT', 'IN', 'OUT', 'INOUT', 'END', 'ARCHITECTURE', 'OF'
	'SIGNAL', 'VARIABLE', 'CONSTANT', 'BEGIN', 'PROCESS', 'COMPONENT', 'TO', 'DOWNTO', 'MAP',
	 'STD_LOGIC', 'STD_LOGIC_VECTOR', 'NATURAL',
 )
operators = ('EQUAL', )
identifiers = ('ID', 'INTVAL', 'BITVAL', 'BITSETVAL', 'HEXVAL')
assignemets = ('SYNCASGN', 'ASYNCASGN', 'CONASGN')
delimiters = ( 'LPAREN', 'RPAREN', 'COMMA', 'DOT', 'SEMI', 'COLON',)

tokens = reserved + identifiers + assignemets + delimiters + operators

t_ignore = ' \t\x0c'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

t_SYNCASGN = r':='
t_ASYNCASGN = r'<='
t_CONASGN = r'=>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_DOT = r'\.'
t_SEMI = r';'
t_COLON = r':'

t_EQUAL = r'='

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = reserved_map.get(t.value.lower(), "ID")
    return t

t_INTVAL = r'\d+'
t_BITVAL = r'\'(1|0)\''
t_BITSETVAL = r'\"(1|0)+\"'
t_HEXVAL = r'x\"[0-9A-Fa-f]+\"'

def t_comment(t):
    r'/--(.|\n)*?/'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Illegal character %s" % repr(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex(reflags=re.IGNORECASE, debug=True)

lexer.input(body)
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)


def p_modhead_1(t):
	'modhead : LIBRARY'
	print('>Lib')
	pass

def p_modhead_2(t):
	'modhead : label'
	print('>NextToName')
	pass

def p_importsec_1(t):
	'importsec : USE'
	pass

def p_importsec_2(t):
	'importsec : label'
	pass

def p_label_1(t):
	'label : ID'
	print(">Name")
	pass

def p_label_2(t):
	'label : DOT'
	print('>dot')
	pass

def p_label_3(t):
	'label : SEMI'
	print('>semi')
	pass
parser = yacc.yacc()
#while True:
yacc.parse(body)
