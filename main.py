from chimerik_lexer import Lexer
from chimerik_parser import Parser
from chimerik import Execute
from sys import argv
import os
import pprint


if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()
    names = {}

    # arg filename or default to main.chm
    filename = argv[1] if argv[1] != "" else 'main.chm'
    if not os.path.exists(filename):
        print(f"Source file named {filename} not present.")
        exit()
    source_file = open(filename, 'r')
    code = source_file.read()
    try: 
        code += "obid();" # hackish way to run head
        tree = parser.parse(lexer.tokenize(code))
        program = Execute(names)
        print(f"\nDebug:\n{tree}\n\n")
        program.evaluate(tree)
    except EOFError:
        print("Error with tree")
