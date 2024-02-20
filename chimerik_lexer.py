from sly import Lexer


class Lexer(Lexer):
    tokens = { NAME, FLOAT, NUMBER, FUNC_DEFINE, TYPE_DEF, PLUS, TIMES, MINUS, DIVIDE, MOD, POW, ASSIGN, LPAREN, RPAREN,
               IF, ELIF, ELSE, WHILE, DO, BREAK, BOOL, STRING, PRINT, INPUT, INC, DEC, EQ, GT, LT, NE, PASS,
               LBRAC, RBRAC, OR, AND, COMMA, DOT}
    ignore = '\r \t'
    ignore_newline = r'\n+'
    ignore_comment = r'\/\/.*'
    ignore_block = r'\/\*[\w\d\s]*\*\/'
    literals = { '[', ']', '(' , ')', ':', ';' }

    # Tokens
    BOOL = r'trigus|viseld'
    TYPE_DEF = r'zviisida|triisida|intach|esach|tonabich'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    NAME['hir'] = IF 
    NAME['lefir'] = ELIF
    NAME['entir'] = ELSE
    NAME['veeil'] = WHILE
    NAME['duu'] = DO
    NAME['leev'] = BREAK
    NAME['trooden'] = PRINT
    NAME['inforse'] = INPUT
    NAME['ap'] = INC
    NAME['dek'] = DEC
    NAME['forbise'] = PASS
    NAME['und'] = AND
    NAME['lef'] = OR
    NAME['drovok'] = FUNC_DEFINE

    FLOAT = r'\d+\.\d*'
    NUMBER = r'\d+'

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

    @_(r'\d+\.\d*')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = t.value[1:-1]
        ansiTable = ["garu", "rath", "gires", "mesich", "bleos", "donchir", "etechopir", "viiest"]

        # Standard Foreground
        if "\\a1." in t.value:
            for color in ansiTable:
                colorCode = 30 + ansiTable.index(color)
                t.value = t.value.replace(f"\\a1.{color}:", f"\033[{colorCode}m")
        # Light Foreground
        if "\\a2." in t.value:
            for color in ansiTable:
                colorCode = 90 + ansiTable.index(color)
                t.value = t.value.replace(f"\\a2.{color}:", f"\033[{colorCode}m")
        # Standard Background
        if "\\a3." in t.value:
            for color in ansiTable:
                colorCode = 40 + ansiTable.index(color)
                t.value = t.value.replace(f"\\a3.{color}:", f"\033[{colorCode}m")
        # Light Background
        if "\\a4." in t.value:
            for color in ansiTable:
                colorCode = 100 + ansiTable.index(color)
                t.value = t.value.replace(f"\\a4.{color}:", f"\033[{colorCode}m")
        # Restore
        t.value = t.value.replace("\\a.baas:", "\033[m")

        t.value = t.value.encode().decode("unicode_escape")
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
