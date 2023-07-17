from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from xNFA import NFA
from ExprListener import ExprListener

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Crie um objeto do tipo ExprListener e faça o percurso na árvore
    listener = ExprListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)

    # Obtenha o NFA resultante
    nfa = listener.get_nfa()

    # Exiba informações sobre o NFA
    nfa.display_info()

if __name__ == '__main__':
    main()
