from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from xNFA import NFA
from xVisitor import CustomExprVisitor

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    print(tree.toStringTree(recog=parser))

    # Criar o objeto ExprVisitor e visitar a árvore sintática
    visitor = CustomExprVisitor()
    #visitor.build_afn(tree)

    # Criar AFN para receber o resultado da visita
    afn = NFA()

    nfa = visitor.build_afn(tree);
    nfa.display_info()



if __name__ == '__main__':
    main()
