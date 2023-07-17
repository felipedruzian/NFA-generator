from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from automaton import NondeterministicFiniteAutomaton

def build_nfa(tree):
    if isinstance(tree, ExprParser.SymbolContext):
        # Se for um símbolo, cria um autômato simples para representá-lo
        symbol = tree.getText()
        automaton = NondeterministicFiniteAutomaton()
        automaton.add_state('q0')
        automaton.set_initial_state('q0')
        automaton.add_state('q1')
        automaton.set_final_state('q1')
        automaton.add_transition('q0', symbol, 'q1')
        return automaton
    elif isinstance(tree, ExprParser.AtomicContext):
        # Se for um átomo (parênteses), retorna o autômato do interior do parêntese
        return build_nfa(tree.expr())
    elif isinstance(tree, ExprParser.ExprContext):
        if tree.getChildCount() == 1:
            # Se for uma expressão atômica, retorna o autômato correspondente
            return build_nfa(tree.atomic())
        elif tree.getChildCount() == 2:
            # Se for uma concatenação, constrói os autômatos das expressões
            left_automaton = build_nfa(tree.expr(0))
            right_automaton = build_nfa(tree.expr(1))
            if left_automaton and right_automaton:
                left_automaton.concat(right_automaton)
                return left_automaton
        elif tree.getChildCount() == 3:
            if tree.getChild(1).getText() == '|':
                # Se for uma alternância, constrói os autômatos das expressões
                left_automaton = build_nfa(tree.expr(0))
                right_automaton = build_nfa(tree.expr(1))
                if left_automaton and right_automaton:
                    left_automaton.alternate(right_automaton)
                    return left_automaton
            elif tree.getChild(1).getText() == '*':
                # Se for um fechamento de Kleene, constrói o autômato da expressão
                expression_automaton = build_nfa(tree.expr(0))
                if expression_automaton:
                    expression_automaton.kleene_closure()
                    return expression_automaton

def main():
    input_string = "((0|1)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(input_string))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()

    # Construa o autômato finito não determinístico (AFN) a partir da árvore sintática
    automaton = build_nfa(tree)

    # Teste o autômato com algumas palavras
    print("Automaton accepts '0':", automaton.accepts("0"))
    print("Automaton accepts '1':", automaton.accepts("1"))
    print("Automaton accepts '00000':", automaton.accepts("00000"))
    print("Automaton accepts '1010':", automaton.accepts("1010"))
    print("Automaton accepts '111':", automaton.accepts("111"))
    print("Automaton accepts '10':", automaton.accepts("10"))
    print("Automaton accepts '011':", automaton.accepts("011"))

if __name__ == '__main__':
    main()
