# Importe as classes necessárias
import antlr4
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

# Classe que representa um estado do autômato
class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, symbol, next_state):
        if symbol in self.transitions:
            self.transitions[symbol].append(next_state)
        else:
            self.transitions[symbol] = [next_state]

# Função que constrói o AFN a partir da árvore sintática
def build_nfa(tree):
    if isinstance(tree, antlr4.tree.Tree.TerminalNode):
        # Caso seja um nó terminal (folha), obtemos o valor do nó com getText()
        value = tree.getText()
        state = State(value)
        next_state = State('q_accept')
        state.add_transition(value, next_state)
        return state

    elif tree.getChildCount() == 1:  # atomic
        return build_nfa(tree.getChild(0))

    elif tree.getChild(1).getText() == '.':
        return concat(build_nfa(tree.getChild(0)), build_nfa(tree.getChild(2)))
    elif tree.getChild(1).getText() == '|':
        return union(build_nfa(tree.getChild(0)), build_nfa(tree.getChild(2)))
    elif tree.getChild(1).getText() == '*':
        return closure(build_nfa(tree.getChild(0)))

def concat(nfa1, nfa2):
    # Adicionar transição vazia do último estado de nfa1 para o primeiro estado de nfa2
    last_state_nfa1 = State('q_accept_nfa1')
    last_state_nfa1.transitions['-'] = [nfa2]
    nfa1.transitions['-'] = [last_state_nfa1]
    return nfa1

def union(nfa1, nfa2):
    # Criar novo estado inicial e adicionar transições vazias para os autômatos originais
    start_state = State('q_start')
    start_state.transitions['-'] = [nfa1, nfa2]

    # Criar novo estado de aceitação e adicionar transições vazias dos autômatos originais para ele
    accept_state = State('q_accept')
    nfa1.transitions['-'].append(accept_state)
    nfa2.transitions['-'].append(accept_state)

    return start_state

def closure(nfa):
    # Criar novo estado inicial e adicionar transições vazias para o autômato original
    start_state = State('q_start')
    start_state.transitions['-'] = [nfa]

    # Criar novo estado de aceitação e adicionar transições vazias do autômato original para ele
    accept_state = State('q_accept')
    nfa.transitions['-'] = [start_state, accept_state]

    return start_state

# Função para escrever as transições do AFN em um arquivo de texto
def write_transitions_to_file(afn, output_file):
    if afn is None:
        print("AFN inválido. Não foi possível escrever as transições.")
        return

    with open(output_file, 'w') as f:
        for state in afn.transitions:
            for symbol, next_states in afn.transitions[state].items():
                for next_state in next_states:
                    f.write(f"{state} {symbol} {next_state.name}\n")

# Exemplo de uso:
# Supondo que a variável 'tree' contenha a árvore sintática gerada pelo reconhecedor
#nfa = build_nfa(tree)

# Escrever as transições do AFN em um arquivo de texto chamado 'output.txt'
#write_transitions_to_file(nfa, 'output.txt')

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Lista para armazenar os estados do AFN
    #afn_states = []

    # Supondo que a variável 'tree' contenha a árvore sintática gerada pelo reconhecedor
    nfa = build_nfa(tree)

    # Construa o AFN a partir da árvore sintática
    #build_afn(tree, afn_states)

    # Escrever as transições do AFN em um arquivo de texto chamado 'output.txt'
    write_transitions_to_file(nfa, 'output.txt')

    # Escreva as transições do AFN em um arquivo de texto
    #with open('afn_transitions.txt', 'w') as file:
    #    for state in afn_states:
    #        for symbol, next_state in state.transitions.items():
    #            file.write(f"{state.name},{symbol},{next_state.name}\n")

if __name__ == '__main__':
    main()