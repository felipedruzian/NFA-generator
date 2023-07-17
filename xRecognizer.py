from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Criar o objeto ExprVisitor e visitar a árvore sintática
    visitor = ExprVisitor()
    visitor.visit(tree)

    print(tree.toStringTree(recog=parser))

if __name__ == '__main__':
    main()
