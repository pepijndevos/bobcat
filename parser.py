from ply import lex
from ply.lex import TOKEN

tokens = [
    # Identifiers
    'ID',

    # constants
    'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN',
    'FLOAT_CONST', 'HEX_FLOAT_CONST',
    'CHAR_CONST',
    #'WCHAR_CONST',

    # String literals
    'STRING_LITERAL',
    #'WSTRING_LITERAL',
]

literals = "[](),:"

# valid C identifiers (K&R2: A.2.3), plus '$' (supported by some compilers)
identifier = r'[a-zA-Z_$][0-9a-zA-Z_$]*'

hex_prefix = '0[xX]'
hex_digits = '[0-9a-fA-F]+'
bin_prefix = '0[bB]'
bin_digits = '[01]+'

# integer constants (K&R2: A.2.5.1)
integer_suffix_opt = r'(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
decimal_constant = '(0'+integer_suffix_opt+')|([1-9][0-9]*'+integer_suffix_opt+')'
octal_constant = '0[0-7]*'+integer_suffix_opt
hex_constant = hex_prefix+hex_digits+integer_suffix_opt
bin_constant = bin_prefix+bin_digits+integer_suffix_opt

bad_octal_constant = '0[0-7]*[89]'

# character constants (K&R2: A.2.5.2)
# Note: a-zA-Z and '.-~^_!=&;,' are allowed as escape chars to support #line
# directives with Windows paths as filenames (..\..\dir\file)
# For the same reason, decimal_escape allows all digit sequences. We want to
# parse all correct code, even if it means to sometimes parse incorrect
# code.
#
simple_escape = r"""([a-zA-Z._~!=&\^\-\\?'"])"""
decimal_escape = r"""(\d+)"""
hex_escape = r"""(x[0-9a-fA-F]+)"""
bad_escape = r"""([\\][^a-zA-Z._~^!=&\^\-\\?'"x0-7])"""

escape_sequence = r"""(\\("""+simple_escape+'|'+decimal_escape+'|'+hex_escape+'))'
cconst_char = r"""([^'\\\n]|"""+escape_sequence+')'
char_const = "'"+cconst_char+"'"
wchar_const = 'L'+char_const
unmatched_quote = "('"+cconst_char+"*\\n)|('"+cconst_char+"*$)"
unmatched_doublequote = "(\""+cconst_char+"*\\n)|(\""+cconst_char+"*$)"
bad_char_const = r"""('"""+cconst_char+"""[^'\n]+')|('')|('"""+bad_escape+r"""[^'\n]*')"""

# string literals (K&R2: A.2.6)
string_char = r"""([^"\\\n]|"""+escape_sequence+')'
string_literal = '"'+string_char+'*"'
wstring_literal = 'L'+string_literal
bad_string_literal = '"'+string_char+'*?'+bad_escape+string_char+'*"'

# floating constants (K&R2: A.2.5.3)
exponent_part = r"""([eE][-+]?[0-9]+)"""
fractional_constant = r"""([0-9]*\.[0-9]+)|([0-9]+\.)"""
floating_constant = '(((('+fractional_constant+')'+exponent_part+'?)|([0-9]+'+exponent_part+'))[FfLl]?)'
binary_exponent_part = r'''([pP][+-]?[0-9]+)'''
hex_fractional_constant = '((('+hex_digits+r""")?\."""+hex_digits+')|('+hex_digits+r"""\.))"""
hex_floating_constant = '('+hex_prefix+'('+hex_digits+'|'+hex_fractional_constant+')'+binary_exponent_part+'[FfLl]?)'

t_ignore = ' \t'

# Newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

t_STRING_LITERAL = string_literal

# The following floating and integer constants are defined as
# functions to impose a strict order (otherwise, decimal
# is placed before the others because its regex is longer,
# and this is bad)
#
@TOKEN(floating_constant)
def t_FLOAT_CONST(t):
    return t

@TOKEN(hex_floating_constant)
def t_HEX_FLOAT_CONST(t):
    return t

@TOKEN(hex_constant)
def t_INT_CONST_HEX(t):
    return t

@TOKEN(bin_constant)
def t_INT_CONST_BIN(t):
    return t

@TOKEN(bad_octal_constant)
def t_BAD_CONST_OCT(t):
    print("Invalid octal constant")
    t.lexer.skip(1)

@TOKEN(octal_constant)
def t_INT_CONST_OCT(t):
    return t

@TOKEN(decimal_constant)
def t_INT_CONST_DEC(t):
    return t

# Must come before bad_char_const, to prevent it from
# catching valid char constants as invalid
#
@TOKEN(char_const)
def t_CHAR_CONST(t):
    return t

@TOKEN(wchar_const)
def t_WCHAR_CONST(t):
    return t

@TOKEN(unmatched_quote)
def t_UNMATCHED_QUOTE(t):
    print("Unmatched '")
    t.lexer.skip(1)

@TOKEN(bad_char_const)
def t_BAD_CHAR_CONST(t):
    print("Invalid char constant %s" % t.value)
    t.lexer.skip(1)

@TOKEN(wstring_literal)
def t_WSTRING_LITERAL(t):
    return t

@TOKEN(unmatched_doublequote)
def t_UNMATCHED_DOUBLEQUOTE(t):
    print("Unmatched \"")
    t.lexer.skip(1)

@TOKEN(bad_string_literal)
def t_BAD_STRING_LITERAL(t):
    print("Invalid string literal")
    t.lexer.skip(1)

@TOKEN(identifier)
def t_ID(t):
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()



import ply.yacc as yacc
from collections import namedtuple

class Juxt(list):
    def __repr__(self):
        return "Juxt"+list.__repr__(self)

Def  = namedtuple("Def", ["name", "quotation"])
Lit  = namedtuple("Lit", ["type", "value"])
Node = namedtuple("Node", ["type", "quotation"])

def p_expression(p):
    """expression : empty
                  | expression part"""
    if len(p) > 2:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = []

def p_part(p):
    """part : definition
            | word
            | juxt
            | quotation
            | node"""
    p[0] = p[1]

def p_word_id(p):
    """word : ID"""
    p[0] = p[1]

def p_word_char(p):
    """word : CHAR_CONST"""
    p[0] = Lit('char', p[1])

def p_word_float(p):
    """word : FLOAT_CONST
               | HEX_FLOAT_CONST"""
    p[0] = Lit('float', p[1])

def p_word_int(p):
    """word : INT_CONST_BIN
               | INT_CONST_DEC
               | INT_CONST_HEX
               | INT_CONST_OCT"""
    p[0] = Lit('int', p[1])

def p_word_string(p):
    """word : STRING_LITERAL"""
    p[0] = Lit('char*', p[1])

def p_juxt(p):
    """juxt : word ',' word
            | juxt ',' word"""
    if isinstance(p[1], Juxt):
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = Juxt([p[1], p[3]])

def p_quotation(p):
    """quotation : '[' expression ']'"""
    p[0] = p[2]

def p_definition(p):
    """definition : ID ':' quotation"""
    p[0] = Def(p[1], p[3])

def p_node(p):
    """node : ID '(' expression ')'"""
    p[0] = Node(p[1], p[3])

def p_empty(p):
    'empty :'
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

if __name__ == "__main__":
    while True:
       try:
           s = input('> ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print(result)
