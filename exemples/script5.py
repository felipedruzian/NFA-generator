# Importe as classes necessárias
import antlr4
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

def construir_afn(node, estado_atual):
    if node is not None:
        if isinstance(node, tree.Tree.TerminalNodeImpl):
            simbolo = node.getSymbol().text
            if simbolo == 'EOF':
                return estado_atual, []  # Chegou ao final, não há transições
            proximo_estado = estado_atual + 1
            return proximo_estado, [(estado_atual, simbolo, proximo_estado)]
        else:
            if node.getText() == '|':
                # Nó representa o operador '|'
                estado_atual, transicoes_esquerda = construir_afn(node.getChild(0), estado_atual)
                proximo_estado, transicoes_direita = construir_afn(node.getChild(1), estado_atual)
                return proximo_estado, transicoes_esquerda + transicoes_direita
            elif node.getText() == '*':
                # Nó representa o operador '*'
                estado_atual, transicoes_expr = construir_afn(node.getChild(0), estado_atual)
                proximo_estado = estado_atual + 1
                transicoes = [(estado_atual, '', proximo_estado), (estado_atual, '', estado_atual + 1)]
                transicoes_expr += [(estado_atual + 1, '', proximo_estado), (proximo_estado - 1, '', estado_atual + 1)]
                return proximo_estado, transicoes_expr + transicoes
            else:
                # Nó representa a concatenação ou símbolo
                for child in node.children:
                    estado_atual, transicoes = construir_afn(child, estado_atual)
                return estado_atual, transicoes

def print_tree(node, indent=0):
    if node is not None:
        if isinstance(node, tree.Tree.TerminalNodeImpl):
            print(' ' * indent + node.getSymbol().text)
        else:
            print(' ' * indent + node.getText())
            for child in node.children:
                print_tree(child, indent + 4)
            
def main():
    input_string = "01|100*1"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()
    #print_tree(tree)
    estado_inicial = 0
    estado_final, transicoes = construir_afn(tree, estado_inicial)

    # Lista para armazenar os estados do AFN
    #afn_states = []

    # Supondo que a variável 'tree' contenha a árvore sintática gerada pelo reconhecedor
    #afn = construir_afn(tree)

    # Construa o AFN a partir da árvore sintática
    #build_afn(tree, afn_states)

    # Escrever as transições do AFN em um arquivo de texto chamado 'output.txt'
    #write_transitions_to_file(nfa, 'output.txt')

    # Escreva as transições do AFN em um arquivo de texto
    #with open('afn_transitions.txt', 'w') as file:
    #    for state in afn_states:
    #        for symbol, next_state in state.transitions.items():
    #            file.write(f"{state.name},{symbol},{next_state.name}\n")
   # Verificando se o AFN foi construído corretamente
    #if afn:
        # Escrevendo as transições do AFN em um arquivo de texto
    with open('automato.txt', 'w') as arquivo:
        for origem, simbolo, destino in transicoes:
            arquivo.write(f"{origem} {simbolo} {destino}\n")
    #else:
    #    print("A árvore sintática não corresponde a uma expressão regular válida.")

if __name__ == '__main__':
    main()