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
        pass

    # Exit a parse tree produced by ExprParser#prog.
    def exitProg(self, ctx:ExprParser.ProgContext):
        pass


    # Enter a parse tree produced by ExprParser#expr.
    def enterExpr(self, ctx:ExprParser.ExprContext):
        pass

    # Exit a parse tree produced by ExprParser#expr.
    def exitExpr(self, ctx:ExprParser.ExprContext):
        pass


    # Enter a parse tree produced by ExprParser#atomic.
    def enterAtomic(self, ctx:ExprParser.AtomicContext):
        pass

    # Exit a parse tree produced by ExprParser#atomic.
    def exitAtomic(self, ctx:ExprParser.AtomicContext):
        pass


    # Enter a parse tree produced by ExprParser#symbol.
    def enterSymbol(self, ctx:ExprParser.SymbolContext):
        pass

    # Exit a parse tree produced by ExprParser#symbol.
    def exitSymbol(self, ctx:ExprParser.SymbolContext):
        pass



del ExprParser