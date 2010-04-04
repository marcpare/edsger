import unittest
from edsger import evaluate, _tokenize, validate_syntax

class TestEvaluator(unittest.TestCase):
	
	def test_tokenizer(self):
		# trailing decimal
		expr = '67.'
		self.assertEqual(_tokenize(expr), ['67.'])
		
		# one big expression
		expr = ' 12 + 10 - 0.1 / .1 * 1.'
		self.assertEqual(_tokenize(expr), ['12', '+', '10', '-', '0.1', '/', '.1', '*', '1.'])
		
		expr = "+++"
		self.assertEqual(_tokenize(expr), ['+', '+', '+'])
		
	def test_valid_syntax(self):
		expr = '67'
		self.assertTrue(validate_syntax(expr))
		
		expr = '67 + 10'
		self.assertTrue(validate_syntax(expr))
		
		expr = '67.0 - 1. + .1 * 2 / 4 ^ 10'
		self.assertTrue(validate_syntax(expr))
		
		expr = '(67.0 - 1. ) + .1 * 2 / 4 ^ 10'
		self.assertTrue(validate_syntax(expr))
		
	def test_invalid_syntax(self):
		syntax_errors = ['67+', 'adf', '67 + a', '5()', '5(+2)', '5+()', '()', '(', ')', '5+6+(10 * 2))']
		value_errors = ['.', '67++', '10..0', '10.0.']
		
		for x in syntax_errors:
			print x
			self.assertRaises(SyntaxError, validate_syntax, x)
		for x in value_errors:
			self.assertRaises(ValueError, validate_syntax, x)		
	
	def test_unary_minus_syntax(self):
		expr = '5--2'
		self.assertTrue(validate_syntax(expr))
		
		expr = '5+5--10-1*(-9^-3)'
		self.assertTrue(validate_syntax(expr))
		
	def test_unary_minus_errors(self):
		expr = '5--2-'
		self.assertRaises(SyntaxError, validate_syntax, expr)
		
		expr = '5-(2+4-)'
		self.assertRaises(SyntaxError, validate_syntax, expr)
		
		expr = '5-^2'
		self.assertRaises(ValueError, validate_syntax, expr)
	
	def test_addition(self):
		self.assertAlmostEqual(evaluate('1 + 2'), 3)
	def test_subtraction(self):
		self.assertAlmostEqual(evaluate('1 - 2'), -1)
	def test_multiplication(self):
		self.assertAlmostEqual(evaluate('2 * 3'), 6)
	def test_division(self):
		self.assertAlmostEqual(evaluate('10 / 2'), 5)
		self.assertAlmostEqual(evaluate('3 / 2'), 3.0/2.0)
	
	def test_assoc(self):
		self.assertAlmostEqual(evaluate('1 + 2 * 3'), 7)
		self.assertAlmostEqual(evaluate('1 + 2 * 3 ^ 2'), 19)
	def test_order_of_operations(self):
		self.assertAlmostEqual(evaluate("(1 + 2) * (4 - 1) ^ 2"), 27)
		self.assertAlmostEqual(evaluate("(1 + 2) * (4 - 2 ^ 3)"), -12)
		self.assertAlmostEqual(evaluate("10 / 2 / 3"), 10.0 / 2.0 / 3.0)
		
	def test_nested_par(self):
		self.assertAlmostEqual(evaluate("((10 - 8) * (2)) + (5 / 3)"), ((10 - 8) * (2)) + (5.0 / 3))
	
	def test_div_by_zero(self):
		self.assertRaises(ZeroDivisionError, evaluate, "1 / 0")
		self.assertRaises(ZeroDivisionError, evaluate, "1 / (2 - 2)")
	
	def test_unary_minus(self):
		self.assertAlmostEqual(evaluate('1--2'), 3)
		self.assertAlmostEqual(evaluate('-3+-2'), -5)
		self.assertAlmostEqual(evaluate('1+(-2*2)'), -3)
		self.assertAlmostEqual(evaluate('1--(-2^2)'), -3)
		self.assertAlmostEqual(evaluate('(1)-2'), -1)
		
if __name__ == '__main__':
	unittest.main()