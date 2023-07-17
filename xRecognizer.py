from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()
