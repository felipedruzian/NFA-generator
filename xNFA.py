class NFA:
    def __init__(self):
        self.states = set()           # Conjunto de estados do AFN
        self.alphabet = set()         # Conjunto de símbolos do alfabeto
        self.initial_states = set()   # Conjunto de estados iniciais
        self.accept_states = set()    # Conjunto de estados de aceitação
        self.transitions = {}         # Dicionário com as transições do AFN

    # Métodos para adicionar estados, símbolos e transições ao AFN
    def add_state(self, state):
        self.states.add(state)

    def add_symbol(self, symbol):
        self.alphabet.add(symbol)

    def add_transition(self, state_from, symbol, state_to):
        if state_from not in self.transitions:
            self.transitions[state_from] = {}
        if symbol not in self.transitions[state_from]:
            self.transitions[state_from][symbol] = set()
        self.transitions[state_from][symbol].add(state_to)

    # Métodos para definir estados iniciais e de aceitação
    def add_initial_state(self, state):
        self.initial_states.add(state)

    def add_accept_state(self, state):
        self.accept_states.add(state)

    def display_info(self):
        print("Estados:", self.states)
        print("Símbolos do alfabeto:", self.alphabet)
        print("Estados iniciais:", self.initial_states)
        print("Estados de aceitação:", self.accept_states)
        print("Transições:")
        for state_from, transitions in self.transitions.items():
            for symbol, states_to in transitions.items():
                for state_to in states_to:
                    print(f"{state_from} --({symbol})--> {state_to}")

def main():
    # Criar um autômato finito não determinístico (AFN) de exemplo
    nfa = NFA()

    # Adicionar estados
    nfa.add_state('q0')
    nfa.add_state('q1')
    nfa.add_state('q2')

    # Adicionar símbolos do alfabeto
    nfa.add_symbol('0')
    nfa.add_symbol('1')

    # Adicionar estados iniciais e de aceitação
    nfa.add_initial_state('q0')
    nfa.add_accept_state('q2')

    # Adicionar transições
    nfa.add_transition('q0', '0', 'q1')
    nfa.add_transition('q1', '1', 'q2')
    nfa.add_transition('q2', '0', 'q2')
    nfa.add_transition('q2', '1', 'q0')

    # Exibir informações do autômato
    print("Estados:", nfa.states)
    print("Símbolos do alfabeto:", nfa.alphabet)
    print("Estados iniciais:", nfa.initial_states)
    print("Estados de aceitação:", nfa.accept_states)
    print("Transições:")
    for state_from, transitions in nfa.transitions.items():
        for symbol, states_to in transitions.items():
            for state_to in states_to:
                print(f"{state_from} --({symbol})--> {state_to}")

if __name__ == '__main__':
    main()