from LR1GetTable import LR1Table
from C_word_process import WordProcess

alias_dict = {
		# Alias for Vn:
		'program' : 'S',
		'block' : 'K',
		'stmts' : 'N',
		'stmt' : 'M',
		'bool' : 'B',
		'T' : 'T',
		'E' : 'E',
		'F' : 'F',
		'G' : 'G',
		# Alias for Vt:
		'main' : 'm',
		'episilon' : 'e',
		'{' : 'l',
		'}' : 'r',
		'id' : 'i',
		'=' : 'q',
		'while' : 'w',
		'(' : 'a',
		')' : 'b',
		'<=' : 'o',
		'>=' : 'p',
		'num' : 'n',
		'+' : 's',
		'*' : 'x',
	}
original_names = list(alias_dict.keys())
alias_names = list(alias_dict.values())

MyGram = [
			'^::=S$',
			'S::=mK',
			'K::=lNr',
			'N::=MN',
			'N::=e',
			'M::=iqE',
			'M::=waBbM',
			'M::=K',
			'B::=ToT',
			'B::=TpT',
			'B::=T',
			'T::=i',
			'T::=n',
			'E::=EsF',
			'E::=F',
			'F::=FxG',
			'F::=G',
			'G::=aEb',
			'G::=T' ]

LR1 = LR1Table(MyGram)


state_stack = [0]
parse_stack = ['$']
input_stack = []

