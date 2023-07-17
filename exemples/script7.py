from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

class AFGenerator(ExprVisitor):
    def __init__(self):
        self.states = set()
        self.transitions = []

    def visitExpr(self, ctx):
        # Visita os nós do tipo expr
        if ctx.getChildCount() == 1:
            # Expressão atômica (symbol ou atomic)
            return self.visit(ctx.getChild(0))

        if ctx.getChildCount() == 3:
            # Operador de concatenação
            left_state = self.visit(ctx.getChild(0))
            right_state = self.visit(ctx.getChild(2))
            self.transitions.append((left_state, '', right_state))

            return left_state, right_state

        if ctx.getChild(1).getText() == '|':
            # Operador de alternância
            left_state = self.visit(ctx.getChild(0))
            right_state = self.visit(ctx.getChild(2))

            # Novo estado inicial com transições vazias para os dois operandos
            initial_state = 'q{}'.format(len(self.states))
            self.states.add(initial_state)
            self.transitions.append((initial_state, '', left_state))
            self.transitions.append((initial_state, '', right_state))

            # Novo estado final com transições vazias a partir dos operandos
            final_state = 'q{}'.format(len(self.states))
            self.states.add(final_state)
            self.transitions.append((left_state, '', final_state))
            self.transitions.append((right_state, '', final_state))

            return initial_state, final_state

        if ctx.getChild(1).getText() == '*':
            # Operador de fechamento de Kleene
            inner_state = self.visit(ctx.getChild(0))

            # Novo estado inicial com transição vazia para o estado interno
            initial_state = 'q{}'.format(len(self.states))
            self.states.add(initial_state)
            self.transitions.append((initial_state, '', inner_state))

            # Novo estado final com transição vazia para o estado interno e transição vazia para o próprio estado final
            final_state = 'q{}'.format(len(self.states))
            self.states.add(final_state)
            self.transitions.append((inner_state, '', final_state))
            self.transitions.append((initial_state, '', final_state))

            return initial_state, final_state

    def visitAtomic(self, ctx):
        # Visita os nós do tipo atomic
        if ctx.getChildCount() == 1:
            if ctx.getChild(0).getText() in ['0', '1']:
                # Símbolo
                state = 'q{}'.format(len(self.states))
                self.states.add(state)
                return state

        if ctx.getChildCount() == 3:
            # Parênteses
            return self.visit(ctx.getChild(1))

    def build_af(self):
        # Retorna o AF construído
        return self.states, self.transitions


def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Crie o visitor e faça a visita na árvore sintática
    af_generator = AFGenerator()
    af_generator.visit(tree)

    # Obtenha o AF construído
    states, transitions = af_generator.build_af()
    print("Estados:", states)
    print("Transições:", transitions)


if __name__ == '__main__':
    main()
