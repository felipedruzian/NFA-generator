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
                left_expr = ctx.getChild(0)
                right_expr = ctx.getChild(2)

                self.states += 2  # Adiciona dois novos estados para acomodar a alternância
                self.afn.append({'from': self.states - 2, 'symbol': 'ε', 'to': self.states})  # Transição do estado atual para o estado da esquerda
                self.visitExpr(left_expr)
                self.afn.append({'from': self.states - 1, 'symbol': 'ε', 'to': self.states})  # Transição do estado atual para o estado da direita
                self.visitExpr(right_expr)

                self.states += 1  # Atualiza o contador de estados após a visita das expressões

            elif ctx.getChild(1).getText() == '*':
                # Operador de fechamento de Kleene
                expr = ctx.getChild(0)

                self.states += 2  # Adiciona dois novos estados para acomodar o fechamento de Kleene
                self.afn.append({'from': self.states - 2, 'symbol': 'ε', 'to': self.states})  # Transição do estado atual para o estado da expressão
                self.visitExpr(expr)
                self.afn.append({'from': self.states - 2, 'symbol': 'ε', 'to': self.states - 1})  # Transição do estado atual para o estado após o fechamento de Kleene
                self.afn.append({'from': self.states - 1, 'symbol': 'ε', 'to': self.states})  # Transição do estado após o fechamento de Kleene de volta ao estado atual

                self.states += 1  # Atualiza o contador de estados após a visita da expressão

    def generate_afn(self, input_string):
        from antlr4 import InputStream
        from ExprLexer import ExprLexer
        from ExprParser import ExprParser

        # Crie um analisador léxico
        lexer = ExprLexer(InputStream(input_string))
        stream = CommonTokenStream(lexer)

        # Crie um analisador sintático
        parser = ExprParser(stream)
        tree = parser.prog()

        self.visit(tree)  # Constrói o AFN a partir da árvore sintática

        return self.afn

    def save_afn_to_file(self, afn, output_file):
        with open(output_file, 'w') as file:
            for transition in afn:
                line = f"{transition['from']} {transition['symbol']} {transition['to']}\n"
                file.write(line)

if __name__ == '__main__':
    input_string = "((0|1)*)"
    afn_generator = AFNGenerator()
    afn = afn_generator.generate_afn(input_string)

    # Salva o AFN em um arquivo de texto
    afn_generator.save_afn_to_file(afn, 'afn_output.txt')
