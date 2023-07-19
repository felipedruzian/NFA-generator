import sys
from antlr4 import *
from ExprLexer import ExprLexer
from ExprParser import ExprParser
from ExprListener import ExprListener
from xNFA import NFA, State

def makeRange(start, end):
	out = ['(']
	
	for s in range(ord(start), ord(end)) :
		out.append(chr(s))
		out.append('|')
		
	out.append(end)
	
	return out

def preProcess(expr : str) -> list:
	#add . (NFA Concat operator)
	#add range
	out = []
	i = 0

	while i < len(expr) :
		
		if expr[i] == '[':
					
			start = expr[i+1]
			end = expr[i+3]
			
			out += makeRange(start, end)			
			i += 4			
	
		else :
			out.append(expr[i] if expr[i] != ']' else ')')

			if expr[i] in {'(', '|'} :
				i += 1; continue
	
			elif i < len(expr) - 1 :
				if expr[i+1] not in {'*', '?', '+', ')', '|', ']'} :
					out.append('.')					
			i += 1			

	return out

#operator precedence table

Precedence = {
	'|' : 0, #NFA Union Operator
	'.' : 1, #NFA Concat Operator
	'?' : 2, #NFA zero or one Operator
	'*' : 2, #NFA Closure Operator
	'+' : 2  #NFA one or more Operator
}

def toPosfix(expr : list) -> str:
	
	out, stack = [], []
	
	for symb in expr :
		if symb == '(' :
			stack.append(symb)
		
		elif symb == ')' :
			try :
				while stack[-1] != '(' :
					out.append(stack.pop())
			except IndexError:
				#if IndexError, then there are some missing parentheses
				sys.stderr.write("Invalid regex pattern.\n")
				sys.exit(64)						
			else : 
				stack.pop() #pop '('
					
		elif symb in {'+', '*', '?', '.', '|'} :
			
			while len(stack) > 0 : 
				if stack[-1] == '(' : 
					break
				elif Precedence[symb] > Precedence[stack[-1]] :
					break
				else : 
					out.append(stack.pop())
			
			stack.append(symb)			
		
		else :
			out.append(symb)
	
	while len(stack) > 0 :
		out.append(stack.pop())
	
	return "".join(out)



if __name__ == '__main__':
    expr = input("Enter with the regex pattern: ")
    input_string = "((0|01)*)"

    # Crie um analisador léxico
    lexer = ExprLexer(InputStream(expr))
    stream = CommonTokenStream(lexer)

    # Crie um analisador sintático
    parser = ExprParser(stream)
    tree = parser.prog()
    print(tree.toStringTree(recog=parser))

    # Imprima a árvore de análise sintática (para fins de depuração)
    #listener = ExprListener()
    #walker = ParseTreeWalker()
    #walker.walk(listener, tree)

    prefixExpr = preProcess(expr)
    posfixExpr = toPosfix(prefixExpr)
    #print('Expresao regular:', expr)
    #print('Expressao prefixa:', prefixExpr)
    #print('Expressao posfixa:', posfixExpr)
    nfa = NFA(State(0, False), State(1, False))

    output_file = "output.txt"
    with open(output_file, "w") as f:
        f.write('Expresao regular: {}\n'.format(expr))
        f.write('Expressao prefixa: {}\n'.format(prefixExpr))
        f.write('Expressao posfixa: {}\n'.format(posfixExpr))

    nfa = nfa.toNFA(posfixExpr)
    nfa.print_info(output_file)

    print("Output written to {}".format(output_file))

