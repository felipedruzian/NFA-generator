from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
import pygraphviz as pgv

# Classe para representar um estado do autômato
class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}  # Dicionário de transições: símbolo -> lista de estados de destino

# Função para construir o AFN a partir da árvore sintática
def build_afn(tree, state_counter, transitions_file):
    if tree.getChildCount() == 0:
        return State(tree.getText())

    if tree.getChildCount() == 1:  # Operador '*' possui apenas um filho
        return build_afn(tree.getChild(0), state_counter, transitions_file)

    if tree.getChildCount() == 2:  # Operadores '.' e '|'
        left_state = build_afn(tree.getChild(0), state_counter, transitions_file)
        right_state = build_afn(tree.getChild(1), state_counter, transitions_file)

        new_state = State(f'state{state_counter}')
        state_counter += 1

        new_state.transitions['-'] = [left_state, right_state]
        return new_state

    if tree.getText() == '*':  # Operador '*'
        left_state = build_afn(tree.getChild(0), state_counter, transitions_file)

        new_state = State(f'state{state_counter}')
        state_counter += 1

        new_state.transitions['-'] = [left_state]
        return new_state

# Função para gerar as transições em formato de arquivo de texto
def generate_transitions_file(state, transitions_file):
    for symbol, destinations in state.transitions.items():
        for dest in destinations:
            transitions_file.write(f"{state.name} {symbol} {dest.name}\n")
            generate_transitions_file(dest, transitions_file)

# Função principal
def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico e sintático como feito no teste anterior (não repetiremos o código aqui)

    # Obtém a árvore sintática
    tree = parser.prog()

    # Constrói o AFN
    state_counter = 0
    start_state = build_afn(tree, state_counter, transitions_file)

    # Gera as transições em um arquivo de texto
    with open('transitions.txt', 'w') as transitions_file:
        generate_transitions_file(start_state, transitions_file)

if __name__ == '__main__':
    main()
