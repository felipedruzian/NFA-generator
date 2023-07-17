from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser

class ExprVisitor(ParseTreeVisitor):
    def visitAtomic(self, ctx:ExprParser.AtomicContext):
        if ctx.expr():
            print("Visiting atomic: (expr)")
            self.visit(ctx.expr())
        elif ctx.getText() == '0':
            print("Visiting atomic: 0")
        elif ctx.getText() == '1':
            print("Visiting atomic: 1")

    def visitExpr(self, ctx:ExprParser.ExprContext):
        if ctx.atomic():
            print("Visiting expr: atomic")
            self.visit(ctx.atomic())
        elif ctx.expr():
            left = ctx.expr(0)
            right = ctx.expr(1)
            if ctx.getChild(1).getText() == '.':
                print("Visiting expr: (expr . expr)")
            elif ctx.getChild(1).getText() == '|':
                print("Visiting expr: (expr | expr)")
            elif ctx.getChild(1).getText() == '*':
                print("Visiting expr: expr*")
            self.visit(left)
            self.visit(right)
