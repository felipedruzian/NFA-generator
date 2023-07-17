from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

class Visitor(ExprVisitor):
    def __init__(self):
        self.states = set()
        self.transitions = []
        self.start_state = None
        self.accept_states = set()

    def generate_afn(self, input_string):
        lexer = ExprLexer(InputStream(input_string))
        stream = CommonTokenStream(lexer)
        parser = ExprParser(stream)
        tree = parser.prog()

        self.visit(tree)
        return self.states, self.transitions, self.start_state, self.accept_states

    def add_state(self, state_name):
        self.states.add(state_name)

    def add_transition(self, from_state, symbol, to_state):
        self.transitions.append((from_state, symbol, to_state))

    def set_start_state(self, state_name):
        self.start_state = state_name

    def add_accept_state(self, state_name):
        self.accept_states.add(state_name)

    def visitAtomic(self, ctx:ExprParser.AtomicContext):
        if ctx.expr():
            self.visit(ctx.expr())
        elif ctx.getText() == '0':
            state_name = f'state{len(self.states)}'
            self.add_state(state_name)
            self.add_accept_state(state_name)
        elif ctx.getText() == '1':
            state_name = f'state{len(self.states)}'
            self.add_state(state_name)
            self.add_accept_state(state_name)

    def visitExpr(self, ctx:ExprParser.ExprContext):
        if ctx.atomic():
            self.visit(ctx.atomic())
        elif ctx.expr():
            left = ctx.expr(0)
            right = ctx.expr(1)
            if ctx.getChild(1).getText() == '.':
                self.visit(left)
                self.visit(right)
            elif ctx.getChild(1).getText() == '|':
                state_name = f'state{len(self.states)}'
                self.add_state(state_name)
                self.add_transition(state_name, '-', left)
                self.add_transition(state_name, '-', right)
                self.set_start_state(state_name)
            elif ctx.getChild(1).getText() == '*':
                state_name = f'state{len(self.states)}'
                self.add_state(state_name)
                self.add_transition(state_name, '-', left)
                self.set_start_state(state_name)
                self.add_transition(left, '-', state_name)
                self.add_accept_state(state_name)

def main():
    input_string = "((0|1)*)"
    visitor = Visitor()
    states, transitions, start_state, accept_states = visitor.generate_afn(input_string)
    print("States:", states)
    print("Transitions:", transitions)
    print("Start State:", start_state)
    print("Accept States:", accept_states)

if __name__ == '__main__':
    main()
