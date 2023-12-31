import sys
from sly import Lexer, Parser

class Chimerik_Lexer(Lexer):
    tokens = { ID, MUTABLE, TYPE, IMMUTABLE, NUMBER, ASSIGN, IF, ELSE, END }
    literals = { '+', '-', '*', '/', '(', ')', '{', '}', '[', ']', '.', ';' }

    ignore = ' \t'
    ignore_comment = r'\\\\.'
    ignore_newline = r'\n+'
    
    MUTABLE = r'imil'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['ston'] = IMMUTABLE
    ID['int'] = TYPE
    NUMBER = r'\d+'
    ASSIGN = r'='
    END = r';'

    def __init__(self):
        self.para_nest_count = 0
        self.curly_nest_count = 0
        self.bracket_next_count = 0
        self.line_number = 0

    @_(r'\n+')
    def ignore_newline(self, t):
        self.line_number += len(t.value)


    def error(self, t):
        print(f"Line {self.line_number}: Bad character {t.value[0]}")
        self.index += 1

class Chimerik_Parser(Parser):
    tokens = Chimerik_Lexer.tokens

    def __init__(self):
        self.names = ()

    @_("MUTABLE TYPE ID ASSIGN NUMBER END")
    def numeric_assignment(self, p):
        print(f"{p.ID} is a {p.MUTABLE} {p.TYPE} containing {p.NUMBER}")

if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as source_file:
        code = source_file.read()
    lexer = Chimerik_Lexer()
    parser = Chimerik_Parser()
    for tok in lexer.tokenize(code):
        print(f"type={tok.type}: value={tok.value}")
    result = parser.parse(lexer.tokenize(code))