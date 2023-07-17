# Generated from Expr.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#prog.
    def visitProg(self, ctx:ExprParser.ProgContext):
        print("Visiting 'prog' node:", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx:ExprParser.ExprContext):
        print("Visiting 'expr' node:", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#atomic.
    def visitAtomic(self, ctx:ExprParser.AtomicContext):
        print("Visiting 'atomic' node:", ctx.getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#symbol.
    def visitSymbol(self, ctx:ExprParser.SymbolContext):
        print("Visiting 'symbol' node:", ctx.getText())
        return self.visitChildren(ctx)



del ExprParser