from pyparsing import Word, Literal, alphas, nums, alphanums, OneOrMore, Optional, SkipTo, ParseException, Group, ZeroOrMore, Suppress, Combine, delimitedList, quotedString, nestedExpr, ParseResults, oneOf

from string import capitalize

#Qualifier to go in front of type in the argument list (unsigned const int foo)
qualifier = OneOrMore(Literal('const') | Literal('unsigned') | Literal('typename'))

def turn_parseresults_to_list(s, loc, toks):
	return ParseResults(normalise_templates(s, loc, toks[0].asList()))

def normalise_templates(s, loc, toks):
	s_list = ['<']
	for i, tok in enumerate(toks):
		try: #See if it's a string
			capitalize(tok)
			s_list.append(' ')
			s_list.append(tok)
		except AttributeError:
			#If it's not a string
			s_list.append(normalise_templates(s, loc, tok))
	s_list.append(' >')
	return ''.join(s_list)

#Skip pairs of brackets.
angle_bracket_pair = nestedExpr(opener='<',closer='>').setParseAction(turn_parseresults_to_list)
#TODO Fix for nesting brackets
parentheses_pair = Literal('(') + SkipTo(')') + Literal(')')
square_bracket_pair = Literal('[') + SkipTo(']') + Literal(']')

#The raw type of the input, i.e. 'int' in (unsigned const int * foo)
#TODO I guess this should be a delimited list (by '::') of name and angle brackets 
input_type = Combine(Word(alphanums + ':_') + Optional(angle_bracket_pair + Optional(Word(alphanums + ':_'))))

#A number. e.g. -1, 3.6 or 5
number = Word('-.' + nums)

#The name of the argument. We will ignore this but it must be matched anyway.
input_name = OneOrMore(Word(alphanums + '_') | angle_bracket_pair | parentheses_pair | square_bracket_pair)

#Grab the '&', '*' or '**' type bit in (const QString & foo, int ** bar)
pointer_or_reference = oneOf('* &')

#The '=QString()' or '=false' bit in (int foo = 4, bool bar = false)
default_value = Literal('=') + OneOrMore(number | quotedString | input_type | parentheses_pair | angle_bracket_pair | square_bracket_pair | Word('|&^'))

#A combination building up the interesting bit -- the argument type, e.g. 'const QString &', 'int' or 'char*'
argument_type = Optional(qualifier, default='').setResultsName("qualifier") + \
                input_type.setResultsName("input_type") + \
                Optional(pointer_or_reference, default='').setResultsName("pointer_or_reference1") + \
                Optional(Literal('const')).setResultsName('const_pointer_or_reference') + \
                Optional(pointer_or_reference, default='').setResultsName("pointer_or_reference2")

#Argument + variable name + default
argument = Group(argument_type.setResultsName('argument_type') + Optional(input_name) + Optional(default_value))

#List of arguments in parentheses with an optional 'const' on the end
arglist = Literal('(') + delimitedList(argument).setResultsName('arg_list') + Optional(Literal(',') + Literal('...')).setResultsName('var_args') + Literal(')')

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
		bracket_location = symbol.index('(')
		#Split the input string into everything before the opening bracket and everything else
		function_name = symbol[:bracket_location]
		arglist_input_string = symbol[bracket_location:]
	except ValueError:
		#If there's no brackets, then there's no function signature. This means the passed in symbol is just a type name
		return symbol, ''
	
	#This is a very common signature so we'll make a special case for it. It requires no parsing anyway
	if arglist_input_string.startswith('()'):
		if arglist_input_string == '()' or arglist_input_string == '()=0':
			return function_name, arglist_input_string
		elif arglist_input_string == '() const ' or arglist_input_string == '() const' or arglist_input_string == '() const =0':
			return function_name, '() const'
	
	#By now we're left with something like "(blah, blah)", "(blah, blah) const" or "(blah, blah) const =0"
	try:
		closing_bracket_location = arglist_input_string.rindex(')')
		arglist_suffix = arglist_input_string[closing_bracket_location+1:]
		arglist_input_string = arglist_input_string[:closing_bracket_location+1]
	except ValueError:
		#This shouldn't happen.
		print 'Could not find closing bracket'
		raise
	
	try:
		result = arglist.parseString(arglist_input_string)
	except ParseException as pe:
		print symbol
		print pe
		raise
	else:
		#Will be a list or normalised string arguments
		#e.g. ['OBMol&', 'vector< int >&', 'OBBitVec&', 'OBBitVec&', 'int', 'int']
		normalised_arg_list = []
		
		#Cycle through all the matched arguments
		for arg in result.arg_list:
			#Here is where we build up our normalised form of the argument
			argument_string_list = ['']
			if arg.qualifier:
				argument_string_list.append(arg.qualifier)
				argument_string_list.append(' ')
			argument_string_list.append(arg.input_type)
			
			#Functions can have a funny combination of *, & and const between the type and the name so build up a list of theose here:
			const_pointer_ref_list = []
			if arg.pointer_or_reference1:
				const_pointer_ref_list.append(arg.pointer_or_reference1)
			if arg.const_pointer_or_reference:
				const_pointer_ref_list.append(' ')
				const_pointer_ref_list.append(arg.const_pointer_or_reference)
				const_pointer_ref_list.append(' ')
			if arg.pointer_or_reference2:
				const_pointer_ref_list.append(arg.pointer_or_reference2)
			#And combine them into a single normalised string and add them to the argument list
			argument_string_list.append(''.join(const_pointer_ref_list))
			
			#Finally we join our argument string and add it to our list
			normalised_arg_list += [''.join(argument_string_list)]
		
		#If the function contains a variable number of arguments (int foo, ...) then add them on.
		if result.var_args:
			normalised_arg_list.append('...')
		
		#Combine all the arguments and put parentheses around it
		normalised_arg_list_string = ''.join(['(', ', '.join(normalised_arg_list), ')'])
		
		#Add a const onto the end
		if 'const' in arglist_suffix:
			normalised_arg_list_string += ' const'
		
		return function_name, normalised_arg_list_string
	
	#TODO Maybe this should raise an exception?
	return None
