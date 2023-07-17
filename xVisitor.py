from ExprVisitor import ExprVisitor

class CustomExprVisitor(ExprVisitor):
    def visitProg(self, ctx):
        print("Visiting 'prog' node:", ctx.getText())
        return self.visitChildren(ctx)

    def visitExpr(self, ctx):
        print("Visiting 'expr' node:", ctx.getText())
        return self.visitChildren(ctx)

    def visitAtomic(self, ctx):
        print("Visiting 'atomic' node:", ctx.getText())
        return self.visitChildren(ctx)

    def visitSymbol(self, ctx):
        print("Visiting 'symbol' node:", ctx.getText())
        return self.visitChildren(ctx)

