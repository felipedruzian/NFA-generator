from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from xNFA import NFA  # Importe a classe NFA que criamos anteriormente

class ExprVisitor(ParseTreeVisitor):
    def __init__(self):
        # Inicialize os atributos para armazenar as informações do autômato
        self.nfa_initial_states = set()
        self.nfa_accept_states = set()
        self.nfa_transitions = {}
        self.nfa = NFA()  # Criar uma instância da classe NFA para representar o autômato

    def visitAtomic(self, ctx: ExprParser.AtomicContext):
        if ctx.expr():
            # Visitar um atomic que é uma expressão
            self.visit(ctx.expr())
        elif ctx.getText() == '0':
            # Visitar um atomic que é o símbolo '0'
            state = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
            self.nfa.initial_states.add(state)
            self.nfa.accept_states.add(state)
        elif ctx.getText() == '1':
            # Visitar um atomic que é o símbolo '1'
            state = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
            self.nfa.initial_states.add(state)
            self.nfa.accept_states.add(state)

    def visitExpr(self, ctx: ExprParser.ExprContext):
        if ctx.atomic():
            # Visitar um expr que é um atomic
            self.visit(ctx.atomic())
        elif ctx.getChildCount() == 1:
            # É um atomic, já foi tratado acima
            pass
        else:
            left = ctx.expr(0)
            right = ctx.expr(1)
            operator = ctx.getChild(1).getText()

            if operator == '|':
                # Visitar um expr que é uma alternância (|)
                self.visit(left)
                self.visit(right)

                # Criação de um novo estado para a alternância
                state = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
                self.nfa.initial_states.add(state)

                # Adicionar transições vazias dos estados iniciais das expressões para o novo estado
                for initial_state in self.nfa.initial_states:
                    self.add_transition(initial_state, '', state)

                # Criação de um novo estado para o estado de aceitação da alternância
                state_accept = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
                self.nfa.accept_states.add(state_accept)

                # Adicionar transições vazias dos estados de aceitação das expressões para o novo estado de aceitação
                for accept_state in self.nfa.accept_states:
                    self.add_transition(accept_state, '', state_accept)

                # Limpar os estados iniciais e de aceitação antigos e adicionar os novos
                self.nfa.initial_states.clear()
                self.nfa.accept_states.clear()
                self.nfa.initial_states.add(state)
                self.nfa.accept_states.add(state_accept)

            elif operator == '*':
                # Visitar um expr que é uma fechamento de Kleene (*)
                self.visit(left)

                # Criação de um novo estado para a fechamento de Kleene
                state = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
                self.nfa.initial_states.add(state)

                # Criação de um novo estado de aceitação para a fechamento de Kleene
                state_accept = f"q{len(self.nfa.initial_states) + len(self.nfa.accept_states)}"
                self.nfa.accept_states.add(state_accept)

                # Adicionar transições vazias dos estados iniciais das expressões para o novo estado
                for initial_state in self.nfa.initial_states:
                    self.add_transition(initial_state, '', state)

                # Adicionar transições vazias do novo estado para o estado de aceitação
                self.add_transition(state, '', state_accept)

                # Adicionar transições vazias do estado de aceitação das expressões para o novo estado de aceitação
                for accept_state in self.nfa.accept_states:
                    self.add_transition(accept_state, '', state_accept)

                # Adicionar transições vazias do novo estado para o estado inicial das expressões
                for accept_state in self.nfa.accept_states:
                    self.add_transition(state, '', accept_state)
                
                # Limpar os estados iniciais e de aceitação antigos e adicionar os novos
                self.nfa.initial_states.clear()
                self.nfa.accept_states.clear()
                self.nfa.initial_states.add(state)
                self.nfa.accept_states.add(state_accept)

            elif operator == '*':
                # Visitar um expr que é uma fechamento de Kleene (*)
                self.visit(left)

                # Criação de um novo estado para a fechamento de Kleene
                state = f"q{len(self.nfa_initial_states) + len(self.nfa_accept_states)}"
                self.nfa_initial_states.add(state)

                # Criação de um novo estado de aceitação para a fechamento de Kleene
                state_accept = f"q{len(self.nfa_initial_states) + len(self.nfa_accept_states)}"
                self.nfa_accept_states.add(state_accept)

                # Adicionar transições vazias dos estados iniciais das expressões para o novo estado
                for initial_state in self.nfa_initial_states:
                    self.add_transition(initial_state, '', state)

                # Adicionar transições vazias do novo estado para o estado de aceitação
                self.add_transition(state, '', state_accept)

                # Adicionar transições vazias do estado de aceitação das expressões para o novo estado de aceitação
                for accept_state in self.nfa_accept_states:
                    self.add_transition(accept_state, '', state_accept)

                # Adicionar transições vazias do novo estado para o estado inicial das expressões
                for accept_state in self.nfa_accept_states:
                    self.add_transition(state, '', accept_state)
                
                # Limpar os estados iniciais e de aceitação antigos e adicionar os novos
                self.nfa_initial_states.clear()
                self.nfa_accept_states.clear()
                self.nfa_initial_states.add(state)
                self.nfa_accept_states.add(state_accept)

    def add_transition(self, state_from, symbol, state_to):
        self.nfa.add_transition(state_from, symbol, state_to)

    def add_initial_state(self, state):
        self.nfa.add_initial_state(state)

    def add_accept_state(self, state):
        self.nfa.add_accept_state(state)

    def build_nfa(self, ctx: ExprParser.ProgContext) -> NFA:
        # Criar uma instância da classe NFA para representar o autômato
        
        # Percorrer a árvore sintática gerada pelo parser
        self.visit(ctx)

        # Retornar o autômato finito não determinístico construído
        return self.nfa
