import sys

class State:
    def __init__(self, state_id, isEnd: bool):
        self.id = state_id
        self.isEnd = isEnd
        self.transition = {}
        self.epsilonTransitions = []

    def addEpsilonTransition(self, to):
        self.epsilonTransitions.append(to)

    def addTransition(self, to, symbol):
        self.transition[symbol] = to


class NFA:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

    def fromEpsilon(self, state_id) -> 'NFA':
        start = State(state_id, False)
        end = State(state_id + 1, True)
        start.addEpsilonTransition(end)

        return NFA(start, end), state_id + 2

    def fromSymbol(self, state_id, symbol) -> 'NFA':
        start = State(state_id, False)
        end = State(state_id + 1, True)
        start.addTransition(end, symbol)

        return NFA(start, end), state_id + 2

    def concatenate(self, first: 'NFA', second: 'NFA', state_id) -> 'NFA':
        first.end.addEpsilonTransition(second.start)
        first.end.isEnd = False

        return NFA(first.start, second.end), state_id

    def union(self, first: 'NFA', second: 'NFA', state_id) -> 'NFA':
        start = State(state_id, False)
        start.addEpsilonTransition(first.start)
        start.addEpsilonTransition(second.start)

        end = State(state_id + 1, True)
        first.end.addEpsilonTransition(end)
        first.end.isEnd = False
        second.end.addEpsilonTransition(end)
        second.end.isEnd = False

        return NFA(start, end), state_id + 2

    def closure(self, nfa: 'NFA', state_id) -> 'NFA':
        start = State(state_id, False)
        end = State(state_id + 1, True)

        start.addEpsilonTransition(nfa.start)
        start.addEpsilonTransition(end)

        nfa.end.addEpsilonTransition(nfa.start)
        nfa.end.addEpsilonTransition(end)
        nfa.end.isEnd = False

        return NFA(start, end), state_id + 2

    def toNFA(self, posfixExpr: str) -> 'NFA':
        if posfixExpr == '':
            return self.fromEpsilon(1)[0]

        stack = []  # stack dos NFAs
        state_id = 1

        try:
            for symb in posfixExpr:
                if symb == '*':
                    nfa, state_id = self.closure(stack.pop(), state_id)
                    stack.append(nfa)
                elif symb == '|':
                    right = stack.pop()
                    left = stack.pop()
                    nfa, state_id = self.union(left, right, state_id)
                    stack.append(nfa)
                elif symb == '.':
                    right = stack.pop()
                    left = stack.pop()
                    nfa, state_id = self.concatenate(left, right, state_id)
                    stack.append(nfa)
                else:
                    nfa, state_id = self.fromSymbol(state_id, symb)
                    stack.append(nfa)

        except IndexError:
            # if indexError, then the NFA could not be built correctly
            sys.stderr.write("Invalid regex pattern.\n")
            sys.exit(64)
        else:
            return stack.pop()

    # Função para imprimir as informações do NFA
    def print_info(self, output_file):
        states = {}
        queue = [self.start]
        while queue:
            current_state = queue.pop(0)
            states[current_state.id] = current_state
            for _, to_state in current_state.transition.items():
                if to_state.id not in states and to_state not in queue:
                    queue.append(to_state)
            for epsilon_state in current_state.epsilonTransitions:
                if epsilon_state.id not in states and epsilon_state not in queue:
                    queue.append(epsilon_state)

        with open(output_file, 'w') as f:
            f.write("Estados do AFN:\n")
            for state_id, state in states.items():
                f.write(f"q{state_id} (Final)\n" if state.isEnd else f"q{state_id}\n")

            f.write("\nEstado Inicial:\n")
            f.write(f"q{self.start.id}\n")

            f.write("\nEstados Finais:\n")
            for state_id, state in states.items():
                if state.isEnd:
                    f.write(f"q{state_id}\n")

            f.write("\nTransições:\n")
            for state_id, state in states.items():
                for symbol, to_state in state.transition.items():
                    f.write(f"q{state_id} --('{symbol}')--> q{to_state.id}\n")

                for epsilon_state in state.epsilonTransitions:
                    f.write(f"q{state_id} --(&)--> q{epsilon_state.id}\n")

