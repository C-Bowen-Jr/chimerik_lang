from sly import Parser
from chimerik_lexer import Lexer


class Parser(Parser):
    tokens = Lexer.tokens

    #debugfile = 'parser.log'

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS', '<', '>', 'GREATER_OR_EQUAL', 'LESS_OR_EQUAL'))

    def __init__(self):
        self.names = {}

    @_('IF "(" expr ")" "{" statement "}" ELSE "{" statement "}" ')
    def statement(self, p):
        return ('compare', p.expr, p.statement0, p.statement1)

    @_('ID "=" expr')
    def statement(self, p):
        self.names[p.ID] = p.expr[1]
        return ('var_assign', p.ID, p.expr)

    @_('expr')
    def statement(self, p):
        return (p.expr)

    @_('PRINT "(" expr ")" ')
    def statement(self, p):
        return ('print', p.expr)

    @_('ID "=" INPUT "(" ")" ')
    def statement(self, p):
        return ('input', p.ID, "")

    @_('ID "=" INPUT "(" STRING ")" ')
    def statement(self, p):
        return ('input', p.ID, p.STRING)

    @_('expr ">" expr')
    def expr(self, p):
        return ('greater', p.expr0, p.expr1)

    @_('expr "<" expr')
    def expr(self, p):
        return ('less', p.expr0, p.expr1)

    @_('expr GREATER_OR_EQUAL expr')
    def expr(self, p):
        return ('less_or_equal', p.expr0, p.expr1)

    @_('expr LESS_OR_EQUAL expr')
    def expr(self, p):
        return ('greater_or_equal', p.expr0, p.expr1)

    @_('DATATYPE "(" expr ")" ')
    def expr(self, p):
        return ('datatype', p.expr)

    @_('INT "(" expr ")" ')
    def expr(self, p):
        return ('int_con', p.expr)

    @_('STR "(" expr ")" ')
    def expr(self, p):
        return ('str_con', p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        try:
            return ('add', p.expr0, p.expr1)
        except TypeError:
            return f'Unsupported data type \'+\' for {p.expr0} and {p.expr1}'

    @_('expr "-" expr ')
    def expr(self, p):
        try:
            return ('sub', p.expr0, p.expr1)
        except TypeError:
            return f'Unsupported data type \'-\' for {p.expr0} and {p.expr1}'

    @_('expr "*" expr ')
    def expr(self, p):
        return ('times', p.expr0, p.expr1)

    @_('expr "/" expr ')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return (p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ('string', p.STRING)

    @_('ID')
    def expr(self, p):
        try:
            return ('var', p.ID)
        except:
            return f'Undefined name {p.ID}'
