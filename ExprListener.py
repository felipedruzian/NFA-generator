# Generated from Expr.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser
from xNFA import NFA

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):
    def __init__(self):
        self.nfa_stack = []  # Pilha para armazenar os NFAs temporários durante o percurso

    # Métodos para processar a entrada
    def enterProg(self, ctx:ExprParser.ProgContext):
        pass

    def exitProg(self, ctx:ExprParser.ProgContext):
        # Ao sair do programa, a pilha deve conter somente um NFA, que é o NFA final
        if len(self.nfa_stack) != 1:
            raise ValueError("Erro ao construir o autômato")
        self.nfa = self.nfa_stack[0]

    def enterExpr(self, ctx:ExprParser.ExprContext):
        pass

    def exitExpr(self, ctx:ExprParser.ExprContext):
        # Quando sair de um nó de expressão, verifique o operador e construa o NFA correspondente
        if ctx.getChildCount() == 1:  # atomic
            pass  # Nada a fazer, pois o NFA correspondente já foi construído no método enterAtomic
        elif ctx.getChildCount() == 2:  # Unary operator
            op = ctx.getChild(0).getText()
            if op == '*':
                self.star()
        elif ctx.getChildCount() == 3:  # Binary operator
            op = ctx.getChild(1).getText()
            if op == '|':
                self.union()

    def enterAtomic(self, ctx:ExprParser.AtomicContext):
        pass

    def exitAtomic(self, ctx:ExprParser.AtomicContext):
        # Ao sair de um nó atomic, construir o NFA correspondente
        if ctx.getChildCount() == 1:  # symbol
            symbol = ctx.getChild(0).getText()
            self.symbol(symbol)
        elif ctx.getChildCount() == 3:  # ( expr )
            # Quando encontrar parênteses, não é necessário fazer nada, pois o NFA está sendo construído nas regras de expressão
            pass

    def enterSymbol(self, ctx:ExprParser.SymbolContext):
        pass

    def exitSymbol(self, ctx:ExprParser.SymbolContext):
        pass

    # Métodos auxiliares para construir o NFA

    def symbol(self, symbol):
        # Cria um NFA com 2 estados: inicial e final
        nfa = NFA()
        initial_state = 'q0'
        final_state = 'q1'
        nfa.add_state(initial_state)
        nfa.add_state(final_state)
        nfa.add_initial_state(initial_state)
        nfa.add_accept_state(final_state)
        nfa.add_symbol(symbol)
        nfa.add_transition(initial_state, symbol, final_state)
        self.nfa_stack.append(nfa)

    def union(self):
        # Realiza a operação de união dos dois últimos NFAs da pilha
        if len(self.nfa_stack) < 2:
            raise ValueError("Erro na operação de união")
        nfa2 = self.nfa_stack.pop()
        nfa1 = self.nfa_stack.pop()

        nfa = NFA()
        new_initial_state = 'q0'
        new_final_state = 'qf'

        # Adiciona os estados e símbolos ao novo NFA
        nfa.add_state(new_initial_state)
        nfa.add_state(new_final_state)
        nfa.add_initial_state(new_initial_state)
        nfa.add_accept_state(new_final_state)
        nfa.add_states(nfa1.states)
        nfa.add_states(nfa2.states)
        # Adiciona símbolos do nfa1 ao novo NFA
        for symbol in nfa1.alphabet:
            nfa.add_symbol(symbol)

        # Adiciona símbolos do nfa2 ao novo NFA
        for symbol in nfa2.alphabet:
            nfa.add_symbol(symbol)

        # Adiciona transições do novo estado inicial para os estados iniciais antigos
        nfa.add_transition(new_initial_state, None, nfa1.initial_states)
        nfa.add_transition(new_initial_state, None, nfa2.initial_states)

        # Adiciona transições dos estados antigos de aceitação para o novo estado final
        for accept_state in nfa1.accept_states:
            nfa.add_transition(accept_state, None, new_final_state)
        for accept_state in nfa2.accept_states:
            nfa.add_transition(accept_state, None, new_final_state)

        self.nfa_stack.append(nfa)

    def star(self):
        # Realiza a operação de fecho de Kleene no último NFA da pilha
        if len(self.nfa_stack) < 1:
            raise ValueError("Erro na operação de fecho de Kleene")
        nfa = self.nfa_stack.pop()

        new_initial_state = 'q0'
        new_final_state = 'qf'

        # Adiciona os novos estados e símbolos ao NFA
        nfa.add_state(new_initial_state)
        nfa.add_state(new_final_state)
        nfa.add_initial_state(new_initial_state)
        nfa.add_accept_state(new_final_state)

        # Adiciona transições do novo estado inicial para os estados iniciais antigos
        nfa.add_transition(new_initial_state, None, nfa.initial_states)

        # Adiciona transições dos estados antigos de aceitação para o novo estado final e para os estados iniciais antigos
        nfa.add_transition(nfa.accept_states, None, new_final_state)
        nfa.add_transition(nfa.accept_states, None, nfa.initial_states)

        self.nfa_stack.append(nfa)

    def get_nfa(self):
        return self.nfa