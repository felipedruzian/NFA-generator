from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprVisitor import ExprVisitor

class AFNGenerator(ExprVisitor):
    def __init__(self):
        self.states = 1  # Contador de estados
        self.afn = []  # Lista de transições do AFN


    def visitAtomic(self, ctx:ExprParser.AtomicContext):
        if ctx.getChildCount() == 1:
            # Símbolo
            symbol = ctx.getChild(0).getText()
            self.afn.append({'from': self.states, 'symbol': symbol, 'to': self.states + 1})
            self.states += 2
        else:
            # Expressão entre parênteses
            self.visitExpr(ctx.expr())

    def visitExpr(self, ctx:ExprParser.ExprContext):
        if ctx.getChildCount() == 1:
            # Expressão atômica
            self.visitAtomic(ctx.getChild(0))
        else:
            if ctx.getChild(1).getText() == '|':
                # Operador de alternância
                self.visitExpr(ctx.getChild(0))
                self.visitExpr(ctx.getChild(2))
            elif ctx.getChild(1).getText() == '*':
                # Operador de fechamento de Kleene
                self.visitExpr(ctx.getChild(0))
                self.afn.append({'from': self.states, 'symbol': 'ε', 'to': self.states - 1})
                self.afn.append({'from': self.states - 1, 'symbol': 'ε', 'to': self.states})
                self.states += 1

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Crie um visitante personalizado e percorra a árvore sintática
    afn_generator = AFNGenerator()
    afn_generator.visit(tree)

    # Autômato finito construído
    afn = afn_generator.afn
    print(afn)

if __name__ == '__main__':
    main()
