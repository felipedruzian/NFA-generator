from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

def main():
    # Crie o lexer e o parser
    lexer = ExprLexer(InputStream("((0|1)*)"))
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)

    # Obtenha o contexto raiz da árvore sintática
    tree = parser.prog()

    # Crie uma instância da classe ExprVisitor
    visitor = ExprVisitor()

    # Construa o autômato finito não determinístico
    nfa = visitor.build_nfa(tree)

    # Agora você pode usar o autômato 'nfa' para outras operações
    # como testar se uma palavra é aceita pelo autômato ou realizar
    # transformações adicionais no autômato.

    # Testar palavras no autômato
    '''word1 = "(0|1)*"  # Palavra que deve ser aceita
    word2 = "010"     # Palavra que não deve ser aceita

    print(f"A palavra '{word1}' é aceita pelo autômato: {nfa.is_accepted(word1)}")
    print(f"A palavra '{word2}' é aceita pelo autômato: {nfa.is_accepted(word2)}")
    print(f"A palavra '((0|1)*)' é aceita pelo autômato: {nfa.is_accepted('((0|1)*)')}")'''
     # Exibir informações do autômato
    nfa.display_info()

    # Testar algumas palavras no autômato
    test_words = ["", "0", "00", "0110", "1111", "101010", "11011011"]
    for word in test_words:
        is_accepted = nfa.is_accepted(word)
        print(f"A palavra '{word}' é aceita pelo autômato: {is_accepted}")

if __name__ == '__main__':
    main()
