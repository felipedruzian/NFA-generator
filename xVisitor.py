from antlr4 import *

# Importe a gramática gerada pelo ANTLR4 (ExprParser e ExprVisitor)
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor
from xNFA import NFA

class CustomExprVisitor(ExprVisitor):
    def __init__(self):
        super().__init__()
        self.nfa = NFA()  # Crie uma instância da classe NFA para construir o AFN
        self.state_counter = 0  # Contador para gerar nomes únicos para os estados

    def generate_state_name(self):
        # Função auxiliar para gerar nomes únicos para os estados do AFN
        self.state_counter += 1
        return f'q{self.state_counter}'

    def visitProg(self, ctx:ExprParser.ProgContext):
        # Visite o nó 'prog' e retorne o resultado de visitChildren
        return self.visitChildren(ctx)

    def visitExpr(self, ctx:ExprParser.ExprContext):
        if ctx.getChildCount() == 1:
            # O nó 'expr' tem apenas um filho, que é um nó 'atomic'
            return self.visitAtomic(ctx.atomic())

        elif ctx.getChildCount() == 3:
            # O nó 'expr' tem três filhos: expr op expr
            left_result = self.visit(ctx.expr(0))
            right_result = self.visit(ctx.expr(1))

            if ctx.op.type == ExprParser.CONCAT:
                # O operador é o símbolo de concatenação '.'
                for accept_state in left_result['accept_states']:
                    for initial_state in right_result['initial_states']:
                        # Adicione uma transição do estado de aceitação do primeiro expr
                        # para o estado inicial do segundo expr, consumindo o símbolo vazio '-'
                        self.nfa.add_transition(accept_state, '-', initial_state)

                return {
                    'initial_states': left_result['initial_states'],
                    'accept_states': right_result['accept_states']
                }

            elif ctx.op.type == ExprParser.ALTER:
                # O operador é o símbolo de alternância '|'
                initial_state = self.generate_state_name()
                accept_state = self.generate_state_name()

                # Adicione transições para os estados iniciais de cada expr
                for state in left_result['initial_states']:
                    self.nfa.add_transition(initial_state, '-', state)
                for state in right_result['initial_states']:
                    self.nfa.add_transition(initial_state, '-', state)

                # Adicione transições dos estados de aceitação de cada expr
                for state in left_result['accept_states']:
                    self.nfa.add_transition(state, '-', accept_state)
                for state in right_result['accept_states']:
                    self.nfa.add_transition(state, '-', accept_state)

                return {
                    'initial_states': {initial_state},
                    'accept_states': {accept_state}
                }

        elif ctx.getChildCount() == 2:
            # O nó 'expr' tem dois filhos: expr op
            expr_result = self.visit(ctx.expr(0))

            if ctx.op.type == ExprParser.CLOSURE:
                # O operador é o símbolo de fechamento de Kleene '*'
                initial_state = self.generate_state_name()
                accept_state = self.generate_state_name()

                # Adicione transições dos estados iniciais e de aceitação do expr
                for state in expr_result['initial_states']:
                    self.nfa.add_transition(initial_state, '-', state)
                for state in expr_result['accept_states']:
                    self.nfa.add_transition(state, '-', accept_state)

                # Adicione transições para consumir o símbolo vazio '-' e retornar ao estado inicial
                self.nfa.add_transition(initial_state, '-', accept_state)
                self.nfa.add_transition(accept_state, '-', initial_state)

                return {
                    'initial_states': {initial_state},
                    'accept_states': {accept_state}
                }

    def visitAtomic(self, ctx:ExprParser.AtomicContext):
        # O nó 'atomic' tem apenas um filho, que é um nó 'symbol'
        return self.visitSymbol(ctx.symbol())

    def visitSymbol(self, ctx:ExprParser.SymbolContext):
        # O nó 'symbol' representa um símbolo do alfabeto (0 ou 1)
        state = self.generate_state_name()
        self.nfa.add_state(state)
        symbol_text = ctx.getText()
        self.nfa.add_symbol(symbol_text)

        return {
            'initial_states': {state},
            'accept_states': {state}
        }
    
    def build_afn(self, tree: ExprParser.ProgContext):
        # Constrói o AFN a partir da árvore sintática
        self.visit(tree)
        return self.nfa
