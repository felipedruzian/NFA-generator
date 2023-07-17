# Importe as classes necessárias
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

# Classe para representar um estado do AFN
class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

# Função para construir o AFN a partir da árvore sintática
def build_afn(node, afn_states):
    if node.getChildCount() == 0:
        # Nó terminal (símbolo ou operador)
        if node.symbol.type in [ExprParser.T__4, ExprParser.T__5]:
            return State(node.getText())
        else:
            if node.getText() == '*':
                # Operador de fechamento de Kleene
                state = State('E*')
                state.transitions[''] = afn_states[-1]
                return state
            else:
                # Operador de alternância ou concatenação
                return afn_states[-1]
    else:
        # Nó não-terminal (expressão regular)
        if node.getText() == '(':
            afn_states.append(None)  # Placeholder para o estado final do grupo
        afn_states.append(State(node.getText()))  # Estado inicial do grupo

        for i in range(node.getChildCount()):
            child = node.getChild(i)
            if child.getText() == '|':
                afn_states.append(State('E*'))
                afn_states[-3].transitions[''] = afn_states[-1]
                afn_states[-2].transitions[''] = afn_states[-1]
            build_afn(child, afn_states)

        if node.getText() == '(':
            afn_states[-3].transitions[''] = afn_states[-1]
            afn_states.pop()
        elif node.getText() == '.':
            afn_states[-3].transitions[''] = afn_states[-2]
            afn_states.pop()
        afn_states.pop()

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Lista para armazenar os estados do AFN
    afn_states = []

    # Construa o AFN a partir da árvore sintática
    build_afn(tree, afn_states)

    # Escreva as transições do AFN em um arquivo de texto
    with open('afn_transitions.txt', 'w') as file:
        for state in afn_states:
            for symbol, next_state in state.transitions.items():
                file.write(f"{state.name},{symbol},{next_state.name}\n")

if __name__ == '__main__':
    main()
