# Generated from Expr.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):

    # Enter a parse tree produced by ExprParser#prog.
    def enterProg(self, ctx:ExprParser.ProgContext):
        print('Entrou no prog', ctx.getText())
        pass

    # Exit a parse tree produced by ExprParser#prog.
    def exitProg(self, ctx:ExprParser.ProgContext):
        print('Saiu do prog', ctx.getText())
        pass


    # Enter a parse tree produced by ExprParser#expr.
    def enterExpr(self, ctx:ExprParser.ExprContext):
        print('Entrou no expr', ctx.getText())
        pass

    # Exit a parse tree produced by ExprParser#expr.
    def exitExpr(self, ctx:ExprParser.ExprContext):
        print('Saiu do expr', ctx.getText())
        pass


    # Enter a parse tree produced by ExprParser#atomic.
    def enterAtomic(self, ctx:ExprParser.AtomicContext):
        print('Entrou no atomic', ctx.getText())
        pass

    # Exit a parse tree produced by ExprParser#atomic.
    def exitAtomic(self, ctx:ExprParser.AtomicContext):
        print('Saiu do atomic', ctx.getText())
        pass


    # Enter a parse tree produced by ExprParser#symbol.
    def enterSymbol(self, ctx:ExprParser.SymbolContext):
        print('Entrou no symbol', ctx.getText())
        pass

    # Exit a parse tree produced by ExprParser#symbol.
    def exitSymbol(self, ctx:ExprParser.SymbolContext):
        print('Saiu do symbol', ctx.getText())
        pass



del ExprParser