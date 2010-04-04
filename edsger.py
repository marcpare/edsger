import re
import inspect
from collections import deque

class OpenToken:
	pass
class CloseToken:
	pass

class NumberToken:
	def __init__(self, raw):
		self.value = float(raw)
	def __add__(self, other):
		return self.value + other.value
	def __sub__(self, other):
		return self.value - other.value
	def __mul__(self, other):
		return self.value * other.value
	def __div__(self, other):
		return self.value / other.value
	def __pow__(self, other):
		return self.value ** other.value
	def __neg__(self):
		return -1.0 * self.value
	def __str__(self):
		return str(self.value)
		
class OperatorToken:	
	pass
	
class AdditionToken(OperatorToken):
	def __init__(self):
		self.assoc = 'left'
		self.precedence = 0
		
	def do_op(self, a, b):
		return a + b
	def __str__(self):
		return "+"
class SubtractionToken(OperatorToken):
	def __init__(self):
		self.assoc = 'left'
		self.precedence = 0
		
	def do_op(self, a, b):
		return a - b
	def __str__(self):
		return "-"
class UnaryMinusToken(OperatorToken):
	def __init__(self):
		self.assoc = 'na'
		self.precedence = 0
		
	def do_op(self, a):
		return -a
	def __str__(self):
		return "-"
class MultiplicationToken(OperatorToken):
	def __init__(self):
		self.assoc = 'left'
		self.precedence = 1
		
	def do_op(self, a, b):
		return a * b
	def __str__(self):
		return "*"
class DivisionToken(OperatorToken):
	def __init__(self):
		self.assoc = 'left'
		self.precedence = 1
		
	def do_op(self, a, b):
		return a / b
	def __str__(self):
		return "/"
class ExponentToken(OperatorToken):
	def __init__(self):
		self.assoc = 'right'
		self.precedence = 2
		
	def do_op(self, a, b):
		return a ** b
	def __str__(self):
		return "^"

OPERATORS = '+-*/^'
OPERATOR_CLASS = [AdditionToken, SubtractionToken, MultiplicationToken,
					DivisionToken, ExponentToken]

def create_token(raw):
	""" Create a token from a raw string. Assumes input is valid. """
	j = OPERATORS.find(raw)
	if j == -1:
		if raw == '(':
			return OpenToken()
		elif raw == ')':
			return CloseToken()
		else:
			return NumberToken(raw)
	else:
		return OPERATOR_CLASS[j]()
		
def _eval_op(rpn_stack, op):
	arg_spec = inspect.getargspec(op.do_op)
	arg_count = len(arg_spec[0]) - 1
	
	args = [rpn_stack.pop() for i in range(arg_count)]
	# remember, this is a stack
	args.reverse()
	
	rpn_stack.append(NumberToken(op.do_op(*args)))

def evaluate(expr):
	""" Evaluate a mathematic expression in infix notation. """
	
	validate_syntax(expr)
	tokens = _tokenize(expr)
	
	rpn_stack = deque()
	op_stack = deque()
	
	# Implementation of Edsger Dijkstra's "shunting yard" algorithm for
	# parsing a mathematical expression in infix notation. Evaluates as
	# it goes along.
	prev_tok = None
	for raw_tok in tokens:
		tok = create_token(raw_tok)
		if isinstance(tok, NumberToken):
			rpn_stack.append(tok)
		elif isinstance(tok, OperatorToken):
			# change subtraction token to minus token if necessary
			if isinstance(tok, SubtractionToken) and  \
				(prev_tok is None or not isinstance(prev_tok, NumberToken)):
				tok = UnaryMinusToken()
			
			while len(op_stack) > 0:
				op2 = op_stack.pop()
				if not isinstance(op2, OperatorToken):
					op_stack.append(op2)
					break
				if (tok.assoc == 'left' and tok.precedence <= op2.precedence) or \
				   (tok.assoc == 'right' and tok.precedence < op2.precedence):
					# evaluate op2
					_eval_op(rpn_stack, op2)
				else:
					# put back onto the stack
					op_stack.append(op2)
					break
			op_stack.append(tok)
		elif isinstance(tok, OpenToken):
			op_stack.append(tok)
		elif isinstance(tok, CloseToken):
			# Pop and eval until (
			op2 = op_stack.pop()
			while not isinstance(op2, OpenToken):
				# evaluate op2
				_eval_op(rpn_stack, op2)
				op2 = op_stack.pop()
		
		prev_tok = tok
				
	# push rest of op_stack onto output
	while len(op_stack) > 0:
		op2 = op_stack.pop()
		_eval_op(rpn_stack, op2)
	
	return rpn_stack.pop().value

def _tokenize(expr):
	""" Split expression into a list of tokens. """
	
	tokens = map(re.escape, list(OPERATORS + "()"))	
	# concat the tokens with pipes between each one
	token_pattern = reduce(lambda x,y : y + "|" + x, tokens)
	token_pattern = "(%s)" % token_pattern
	
	res = re.split(token_pattern, expr)
	res = map(str.strip, res)
	# clean up the empty items
	res = filter(lambda x : len(x) > 0, res)
	
	return res
	
def validate_syntax(expr):
	""" Raises an exception if there is a syntax error. """
	
	# Step 1: make sure there are only digits, operators, and spaces
	valid_chars = " \.\d"
	valid_chars += "".join(map(re.escape, OPERATORS + "()"))
	invalid_chars = "[^%s]" % (valid_chars)
	les_invalides = re.findall(invalid_chars, expr)
		
	if len(les_invalides) > 0:
		raise SyntaxError("Invalid character %s" % les_invalides[0])
	
	# Step 2: make sure numbers in the string are valid and that it
	#		  alternates between operands and operators
	expecting_number = True
	opened_par = 0
	prev_tok = ''
	for tok in _tokenize(expr):
		par_match = re.match('[\(\)]', tok)
		if len(tok) == 1 and par_match:
			if par_match.group(0) == '(':
				opened_par += 1
				if len(prev_tok) > 0 and not expecting_number:
					raise SyntaxError("Can only open ( at beginning or after operator")
			else:
				opened_par -= 1
				if prev_tok == ')':
					raise SyntaxError("Missing expression inside ()")
				if len(prev_tok) == 0:
					raise SyntaxError("Can't start expression with )")

			if opened_par < 0:
				raise SyntaxError("Unbalanced parentheses")
			continue
			
		if expecting_number:
			# unary operators are allowed
			if tok == '-':
				# still looking for a number
				expecting_number = not expecting_number
			else:
				float(tok)
		else:
			if len(tok) > 1:
				raise SyntaxError("Invalid operator %s" % tok)
			elif tok not in OPERATORS:
				raise SyntaxError("Unknown operator %s" % tok)
				
		expecting_number = not expecting_number
		prev_tok = tok
			
	# Step 3: can't end with an operator
	if expecting_number:
		raise SyntaxError("Can't end expression with an operator")
	
	# Step 4: make sure not unclosed parentheses
	if opened_par > 0:
		raise SyntaxError("Unclosed (")
	
	return True

if __name__ == "__main__":
	s = "235. + ( 10 - 70) * 2"
	s = "3.0 + 4.0 * 2.0 / (1.0 - 5.0) ^ 2.0 ^ 3.0"
	s = "5 + (5 / 5)"
	print evaluate(s)	