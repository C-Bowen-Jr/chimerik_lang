from sly import Parser
from chimerik_lexer import Lexer


class Parser(Parser):
    tokens = Lexer.tokens
    #debugfile = "debug.log"
    precedence = (
        ('right', COLON, DOT),
        ('left', OR, AND), 
        ('left', EQ, LT , GT ,NE), 
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),   
        ('left', POW), 
        ('left', MOD),
        ('right', UMINUS),
        ('left', WHILE, DO),
        ('left', IF, ELIF, ELSE),  
        ('left', PRINT, INPUT)
        )

    def __init__(self):
        self.names = { }
        self.prompt = True

    ############################################################
    # MAIN
    ############################################################

    @_('statements')
    def main(self, p):
        return ('main', p.statements)

    @_('statement')
    def statements(self,p):
        return ('statements', [p.statement])

    @_('statements statement')
    def statements(self,p):
        return ('statements', p.statements[1] + [p.statement])


    ############################################################
    # STATEMENTS
    ############################################################

    @_('FUNC_DEFINE NAME LPAREN RPAREN LBRAC statements RBRAC')
    def statement(self, p):
        return ('func_define', p.NAME, p.statements)

    @_('FUNC_DEFINE NAME LPAREN params RPAREN LBRAC statements RBRAC')
    def statement(self, p):
        return ('func_define', p.NAME, p.statements, p.params)

    @_('NAME LPAREN RPAREN ";"')
    def statement(self, p):
        return ('func_call', p.NAME)

    @_('NAME LPAREN params RPAREN ";"')
    def statement(self, p):
        return ('func_call', p.NAME, p.params)

    @_('PRINT LPAREN statement RPAREN ";"')
    def statement(self, p):
        return ('print', p.statement)

    @_('INPUT LPAREN statement RPAREN ";"')
    def statement(self, p):
        return ('input', p.statement)

    @_('expr')
    def statement(self, p):
        return ('statement-expr', p.expr)

    @_('NAME ASSIGN statement ";"')
    def statement(self, p):
        return ('assign', p.NAME, p.statement)

    @_('IF expr LBRAC statements RBRAC [ ELIF expr LBRAC statements RBRAC ] [ ELSE LBRAC statements RBRAC ] ')
    def statement(self, p):
        return ('if-elif-else', p.expr0 ,p.statements0, p.expr1, p.statements1, p.statements2)

    @_('WHILE expr DO LBRAC statements RBRAC')
    def statement(self, p):
        return ('while', p.expr, p.statements)

    @_('PASS')
    def statement(self, p):
        return ('pass',)

    @_('BREAK')
    def statement(self, p):
        return ('break',)

    ############################################################
    # Expressions
    ############################################################

    @_(' "[" params "]"')
    def expr(self, p):
        return ('list', p.params)

    @_('params COMMA expr')
    def params(self, p):
        return ('params', p.params[1] + [p.expr])

    @_('expr')
    def params(self, p):
        return ('params', [p.expr])

    @_('BOOL')
    def expr(self, p):
        return('bool', p.BOOL)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return('uminus', p.expr)

    @_('expr PLUS expr')
    def expr(self, p):
        return ('plus', p.expr0, p.expr1)

    @_('expr MINUS expr')
    def expr(self, p):
        return ('minus', p.expr0, p.expr1)

    @_('expr TIMES expr')
    def expr(self, p):
        return ('times', p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return ('divide', p.expr0, p.expr1)

    @_('expr MOD expr')
    def expr(self, p):
        return ('mod', p.expr0, p.expr1)

    @_('expr POW expr')
    def expr(self, p):
        return ('pow', p.expr0, p.expr1)
   
    @_('expr EQ expr')
    def expr(self, p):
        return ('equals', p.expr0, p.expr1)

    @_('expr NE expr')
    def expr(self, p):
        return ('ne', p.expr0, p.expr1)

    @_('expr GT expr')
    def expr(self, p):
        return ('gt', p.expr0, p.expr1)

    @_('expr LT expr')
    def expr(self, p):
        return ('lt', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)


    @_('NAME DOT INC ";"')
    def statement(self, p):
        return ('inc', p.NAME)    

    @_('NAME DOT DEC ";"')
    def statement(self, p):
        return ('dec', p.NAME)    

    @_('expr ":" expr %prec COLON')
    def expr(self, p):
        return ('index', p.expr0, p.expr1)


    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return ('paren', p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('number', p.NUMBER)

    @_('FLOAT')
    def expr(self, p):
        return ('float', p.FLOAT)

    @_('STRING')
    def expr(self, p):
        return ('string', p.STRING)

    @_('NAME')
    def expr(self, p):
        return ('name', p.NAME)