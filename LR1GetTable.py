from LRGetFirstSet import First
import pandas as pd

# from test_key import get_key

class LR1Table:
	''' Grammar rules must be augmented beforehand by the user 
		with '^::=.S$'. Where ^ denotes S', S is the first Vn.
	'''	
	def shift_pos(self,item):
		'''
			将.向后移动一位
		'''
		Item = ''.join(item).replace(' ','')
		listItem = list(Item)
		index = listItem.index('.')

		if len(listItem[index:]) != 1:
			return (Item[:index]+''+Item[index+1]+'.'+Item[index+2:])
		return item
	
	def check(self,item,N):
		'''
		Check if the grammar is not completely parsed or not
		Input: Item, GrammarSymbol
		Output: True if . can be shifted else False

		Example1:
		Input:['A::=B.b$'],b
		Output:True
		'''
		try:
			index = item.index('.')

			if N == item[index+1] and item[index+1] != 'e':
				return True

		except:
			return False

	def parse_shift(self, I, symbol):
		'''
		Input: (Item, GrammarSymbol)
		Output: Items after shift symbol is performed

		Example: 
		Input: ['S::=.CC$'], C
		Output: ['S::=C.C$', 'C::=.cC$', 'C::=.d$']

		'''
		J = []
		for item in I:
			if self.check(item,symbol): #True if . can still be shifted else False
				new = self.shift_pos(item)
				J.append(new)

		if len(J) == 0:
			return([])

		return(J)


	def find_productions(self,A):
		'''
		Input: Vn A
		Output: All alphas of A (A -> alpha)

		Example
		Input : 'C'
		Output: ['cC','d']
		'''
		if A == '$':
			return 1
		if A not in self.entryOfGram.keys(): #if NOT a Vn
			return 1
		return self.entryOfGram[A]

	def find_terminals_of(self,gram):
		'''
		Input : gram
		output : {
			'^':['S$']
			'S':['aAd', 'bAc', 'aec', 'bed']
			'A':['e']
		}
		'''
		newList = {}
		for i in gram:
			n = i.replace(' ', '').split('::=')
			if n[0] not in newList.keys():
				newList[n[0]]=[''.join(n[1])]
			else:
				newList[n[0]].append(''.join(n[1]))
		return newList


	def next_dot_pos(self,item):
		'''
		input: An item
		output: The element to be executed

		Example
		input:'A::=.A$'
		output :'A'

		'''
		try:
			index = item.index('.')
			return item[index+1]
		except:
			return '$'

	def get_beta_follow(self,item):
		'''
		input: An item
		output: The next non-terminal to be opened up

		Example
		input:'^::.S$'
		output: '$'

		'''
		# Item = item.replace(' ','')
		# listItem = list(Item)
		try:
			index = item.index('.')
			return item[index+2:]
		except IndexError:  #input:'A::.B'
			return '$'

	def find_closure(self,I):
		'''
		Input: Grammar I
		Output : Closure of Grammar

		Input: ['^::=.S$']
		Output : [['^::=.S$'], ['S::=.aAd$'], ['S::=.bAc$'], ['S::=.aec$'], ['S::=.bed$']]

		where last element is the follow element.
		Example:
		In ['^::=.S$'] , $ is the follow of '^::=.S'
		'''
		add=1
		while (add!=0):
			add=0
			for item in I:
				alpha = item.split("::=")[-1]
				A = item.split("::=")[0]

				next_ch_to_parse = self.next_dot_pos(alpha)
				findPr = self.find_productions(next_ch_to_parse)
				if findPr == 1: #如果.后的符号是Vt
					pass
				else:#如果.后的符号是Vn
					for productions in findPr:
						beta_and_follow = self.get_beta_follow(item) #like input'S->.AB$', get 'B$'
						first_follow = self.first_set[beta_and_follow[0]]
						if len(first_follow) == 0:
							first_follow = self.first_set[beta_and_follow[1]]
						for b in first_follow:
							new_item = next_ch_to_parse + '::=.' + productions + b
							if new_item not in I:
								I.append(new_item)
								add=1
			return(I)
			
	def get_candidates(self,I):
		'''
		Input: ['S::=.C$','C::=.d$]
		Output: ['C','d']
		'''
		candidates = []
		for item in I:
			index = item.index(".")
			next_to_dot = item[index+1]
			if index+2 < len(item) and (next_to_dot not in candidates):
				candidates.append(item[index+1])
		
		return candidates

	def is_reduce_item(self,item):
		'''
		Input: 'S::=.C$'  Output: 0
		Input: 'S::=C.$'  Output: 1
		'''
		index = item.index(".")
		if index == len(item)-2:
			return True
		else: 
			return False

	def is_reduce_set(self,I):
		'''
		判断一个集合是否全部为规约事件
		'''
		reduce_item_count = 0
		for item in I:
			reduce_item_count =+ self.is_reduce_item(item)
		if len(I) == reduce_item_count:
			return True
		else:
			return False

	def get_key (self, dict, value):
		'''
		get key in dict based on a given value
		'''
		for k,v in dict.items():
			if v == value:
				return k
		return -1   

	def get_DFA(self): 
		'''
		Input : I0
		Output : state sets,
				 DFA relations,
				 ACTIONGOTO table
		'''
		self.state_set_dict = {}
		self.DFA_relations = [] #Element example: {'Si':0 , 'Sj':2, 'x': 'a'}
		
		starting = "^::=.S$"
		#DFS build state sets
		I0 = self.find_closure([starting])
		self.state_set_dict[0] = I0
		
		I = [I0] #状态集栈, 压入I0

		count = 0

		while(len(I) != 0):
			# current_I = I[0]
			# I = I[1:]
			current_I = I.pop()

			original_count = count
			candidate_chs = self.get_candidates(current_I)
			for ch in candidate_chs: #如果是全规约集，候选元素为空，不会进入此循环
				moved = self.parse_shift(current_I,ch)
				new_state_set = self.find_closure(moved)
				
				if new_state_set not in self.state_set_dict.values(): #避免重复状态集合
					I.append(new_state_set) #入栈
					count += 1
					index = count
					if index not in self.state_set_dict.keys(): #存入状态集字典
						self.state_set_dict[index] = new_state_set
				
				
				Si = self.get_key(self.state_set_dict,current_I)
				Sj = self.get_key(self.state_set_dict,new_state_set)
				if(new_state_set != current_I): #Si != Sj 直接进入
					self.DFA_relations.append({'Si':Si , 'Sj':Sj, 'x': ch})#存入DFA箭头
				else: #如果Si = Sj
					loop_count = original_count-1
					is_reduce_set = self.is_reduce_set(new_state_set)
					if(not is_reduce_set): #Si = Sj, 但是为循环箭头
						self.DFA_relations.append({'Si':Si , 'Sj':Sj, 'x': ch})#存入DFA箭头
						# I.pop() #循环状态集不能入状态集栈


	def ACTIONGOTO_table_function(self,item, i, j = -1):
		dot_index = item.index(".")
		if (self.is_reduce_item(item)):
			r = item[:dot_index]
			return {'State': i, 'V': item[-1], 'value': "reduce " + r }

		else:
			x = item[dot_index+1]
			if (x.isupper()):
				return {'State': i, 'V': x, 'value': "goto " + str(j) }
			else:
				return {'State': i, 'V': x, 'value': "shift " + str(j) }

	def construct_table (self):
		self.dfa_relation_df = pd.DataFrame(self.DFA_relations)
		self.ACTIONGOTO = [] #ACTIONGOTO table {'Si': Si, 'x': x, 'value': 'reduce ^::=S}

		for i in range(len(self.state_set_dict)):
			Si = self.state_set_dict[i]
			# j = self.dfa_relation_df.loc(self.dfa_relation_df['Si'] == i)
			# x =
			for item in Si :
				if self.is_reduce_item(item):
					self.ACTIONGOTO.append(self.ACTIONGOTO_table_function(item,i))
				else:
					next_to_parse = self.next_dot_pos(item)
					# j = self.dfa_relation_df.loc((self.dfa_relation_df['Si']==i)&(self.dfa_relation_df['']==next_to_parse),['Sj'])
					j = self.dfa_relation_df['Sj'][(self.dfa_relation_df['Si']==i) & (self.dfa_relation_df['x']==next_to_parse)]
					j = int(j)
					self.ACTIONGOTO.append(self.ACTIONGOTO_table_function(item,i,j))

		self.ACTIONGOTO_df = pd.DataFrame(self.ACTIONGOTO)
		self.ACTIONGOTO_df.drop_duplicates(inplace=True)
		self.ACTIONGOTO_df['value'][self.ACTIONGOTO_df['value']=="reduce ^::=S"] = "ACC"



	def __init__(self,LR1_grammer_rules):
		self.gram = LR1_grammer_rules
		self.entryOfGram = self.find_terminals_of(self.gram)
		self.first_set = First(grammar_rules=self.gram).first_set

		self.get_DFA()
		self.construct_table()





if __name__ == "__main__":

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
		';' : 'z',
	}
	original_names = list(alias_dict.keys())
	alias_names = list(alias_dict.values())

	MyGram = [
			'^::=S$',
			'S::=mK',
			'K::=lNr',
			'N::=MN',
			'N::=e',
			'M::=iqEz',
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
	
	gram = [
			'^::=S$',
			'S::=aAd',
			'S::=bAc',
			'S::=aec',
			'S::=bed',
			'A::=e'
		]
	LR1_gram = [
		'^::=S$',
		'S::=CC',
		'C::=cC',
		'C::=d',
	]

	LR1 = LR1Table(LR1_grammer_rules=MyGram)

	print("-------State_dict-----------")
	print(LR1.state_set_dict)
	print("-------DFA relation-----------")
	print(LR1.DFA_relations)
	print("-------ACTION GOTO-----------")
	print(LR1.ACTIONGOTO_df)

