from sly import Lexer


class Lexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, MOD, POW, ASSIGN, LPAREN, RPAREN,
               IF, ELIF, ELSE, WHILE, DO, BREAK, BOOL, STRING, PRINT, INPUT, INC, DEC, EQ, GT, LT, NE, PASS,
               LBRAC, RBRAC, OR, AND, COMMA, DOT}
    ignore = '\r \t'
    ignore_newline = r'\n+'
    ignore_comment = r'\//.*'
    ignore_block = r'\/\*[\w\d\s]*\*\/'
    literals = { '[', ']', '(' , ')', ':', ';' }

    # Tokens
    BOOL = r'trigus|viseld'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    NAME['if'] = IF 
    NAME['elif'] = ELIF
    NAME['else'] = ELSE
    NAME['while'] = WHILE
    NAME['do'] = DO
    NAME['break'] = BREAK
    NAME['trooden'] = PRINT
    NAME['input'] = INPUT
    NAME['ap'] = INC
    NAME['dek'] = DEC
    NAME['nothing'] = PASS
    NAME['and'] = AND
    NAME['or'] = OR

    NUMBER = r'\d+\.{0,1}\d*'

    # Operators
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRAC = r'\{'
    RBRAC = r'\}'
    MOD = r'%'
    POW = r'\^'
    EQ = r'=='
    GT = r'>'
    LT = r'<'
    NE = r'!='
    ASSIGN = r'='
    COMMA = r','
    DOT = r'\.'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'trigus|viseld')
    def BOOL(self, t):
        t.value = True if t.value == "trigus" else False
        return t

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Syntax error: {t.value[0]} on line {self.lineno}')
        self.index += 1
