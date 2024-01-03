from chimerik_lexer import Lexer
from chimerik_parser import Parser
from chimerik import Execute
from sys import argv
import os


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
	lines = source_file.read().split(';')
	for line in lines:
		if line:
			tree = parser.parse(lexer.tokenize(line))
			Execute(tree, names)
