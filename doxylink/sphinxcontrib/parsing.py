from pyparsing import Word, Literal, alphas, nums, alphanums, OneOrMore, Optional, SkipTo, ParseException, Group, ZeroOrMore, Suppress, Combine

#Qualifier to go in front of type in the argument list (unsigned const int foo)
qualifier = OneOrMore(Literal('const') ^ Literal('unsigned'))

#Skip pairs of brackets.
#TODO Fix for nesting brackets
angle_bracket_pair = Literal('<') + SkipTo('>') + Literal('>')
parentheses_pair = Literal('(') + SkipTo(')') + Literal(')')
square_bracket_pair = Literal('[') + SkipTo(']') + Literal(']')

#The raw type of the input, i.e. 'int' in (unsigned const int * foo)
input_type = Combine(Word(alphanums + ':_') + Optional(angle_bracket_pair))

#A fully qualified name. Used when it is not a function passed in (i.e. no parentheses)
symbol = Combine(OneOrMore(Word(alphanums + ':_') ^ angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair))

#A number. e.g. -1, 3.6 or 5
number = Word('-.' + nums)

#The name of the argument. We will ignore this but it must be matched anyway.
input_name = OneOrMore(Word(alphanums + '_') ^ angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair)

#Grab the '&', '*' or '**' type bit in (const QString & foo, int ** bar)
pointer_or_reference = Word('*&')

#The '=QString()' or '=false' bit in (int foo = 4, bool bar = false)
default_value = Literal('=') + OneOrMore(angle_bracket_pair ^ parentheses_pair ^ square_bracket_pair ^ input_type ^ number ^ Word('|&^'))

#A combination building up the interesting bit -- the argument type, e.g. 'const QString &', 'int' or 'char*'
argument_type = Optional(qualifier, default='').setResultsName("qualifier") + input_type.setResultsName("input_type") + Optional(pointer_or_reference, default='').setResultsName("pointer_or_reference")

#Argument + variable name + default
argument = Group(argument_type.setResultsName('argument_type') + Optional(input_name) + Optional(default_value))

#List of arguments in parentheses with an optional 'const' on the end
arglist = Literal('(') + Group(ZeroOrMore(argument + Suppress(Literal(','))) + Optional(argument)).setResultsName('arg_list') + Literal(')') + Optional(Literal('const'), default='').setResultsName('const_function')

full_symbol = (SkipTo('(').setResultsName('function_name') + Optional(arglist)) ^ symbol.setResultsName('symbol') #In this case 'input_type' is the function name

def normalise(symbol):
	"""
	Takes a c++ symbol or funtion and splits it into symbol and a normalised argument list.
	
	:Parameters:
		symbol : string
			A C++ symbol or function definition like ``PolyVox::Volume``, ``Volume::printAll() const``
	
	:return:
		a tuple consisting of two strings: ``(qualified function name or symbol, normalised argument list)``
	"""
	try:
		result = full_symbol.parseString(symbol)
	except ParseException, pe:
		print sample
		print pe
	else:
		normalised_arg_list = []
		
		for arg in result.arg_list:
			argument = ''
			if arg.qualifier:
				argument += arg.qualifier + ' '
			argument += arg.input_type
			if arg.pointer_or_reference:
				argument += arg.pointer_or_reference
			
			normalised_arg_list += [argument]
		
		normalised_arg_list_string = '(' + ', '.join(normalised_arg_list) + ')'
		
		if result.const_function:
			normalised_arg_list_string += ' ' + result.const_function
		
		#If we found a 'symbol' then there were no brackets after the requested name. Therefore it is not necessarily a function
		if result.symbol:
			return result.symbol, ''
		
		return result.function_name, normalised_arg_list_string
	
	return None
