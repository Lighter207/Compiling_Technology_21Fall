from LRGetFirstSet import First
import pandas as pd

class LR1Table:
	''' Grammar rules must be augmented beforehand by the user 
		with '^::=.S$'. Where ^ denotes S', S is the first Vn.
	'''
	def check_validility(self,i):
		if i[0][-1]=='.':
			return False
		return True

	def pre_process_states(self,states):
		'''
		One of the implementation error:
		Since our grammar is in the form 'A::=Bb' where b is the follow of the grammar.

		The program could not distinguish the follow element from the other elements, hence, we need this function to
		avoid that.

		'''
		l=[]
		for i in states:
			if self.check_validility(i):
				l.append(''.join(i).replace(' ',''))

		if len(l)!=0:
			return(l)
			

	def is_nonterminal(self,symbol):
		return symbol.isupper()
	
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
		Item = ''.join(item).replace(' ','')
		listItem = list(Item)
		try:
			index=listItem.index('.')
			#index1=listItem.index('=')
			if N == listItem[index+1]:
				return True
			if ' '== listItem[index+1]:
				return False
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
		J=[]
		is_Vn = 0
		for i in I:
			if self.check(i,symbol): #True if . can still be shifted else False
				new = self.shift_pos(i)
				J.append(new)
		
		if(symbol.isupper()):
			is_Vn = 1

		if len(J) == 0:
			return([],is_Vn)

		return(J,is_Vn)

	def all_grammar_symbols(self,item):
		'''
		Input: All sets of Grammar(our main input)
		Output: Grammar Symbols
		'''
		l=[]
		for i in item:
			for k in i:
				if k.isalpha():
					l.append(k)
		
		return set(l)


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
		Item = item.replace(' ','')
		listItem = list(Item)
		try:
			index = listItem.index('.')
			return listItem[index+1]
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
		Item = item.replace(' ','')
		listItem = list(Item)
		try:
			index = listItem.index('.')
			return listItem[index+2:]
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
						for b in self.first_set[beta_and_follow[0]]:
							new_item = next_ch_to_parse + '::=.' + productions + b
							if new_item not in I:
								I.append(new_item)
								add=1
			return(I)
			

	def __init__(self,LR1_grammer_rules):
		self.gram = LR1_grammer_rules
		starting = '^::=.S$'

		self.entryOfGram = self.find_terminals_of(self.gram)
		self.first_set = First(grammar_rules=self.gram).first_set

		I = [self.find_closure([starting])] #I0状态集

		all_symbols_set = self.all_grammar_symbols(self.gram)

		self.allItems = {}
		self.ItemsAll = []

		new_item = True
		while new_item:
			new_item = False
			count = 1
			for item in I: #item是状态集合I中的一个表达式，如S::=.CC$
				# count += 1
				for symbol in all_symbols_set: 
					if len(self.parse_shift(item,symbol)) != 0: #item可以解析symbol并shift一步
						shifted, mark_goto = self.parse_shift(item,symbol) #比如解析C得到['S::=C.C$', 'C::=.cC$', 'C::=.d$'], 1
						new_state_set = self.find_closure(shifted)#找到shift后的子集

						if new_state_set not in I: #避免重复状态集合
							index = 'I' + str(count)
							count += 1
							if index not in self.allItems.keys(): #存入总字典
								self.allItems[index] = [symbol]
								
							I_new = new_state_set
							Z = self.pre_process_states(I_new)
							if (Z):
								if I_new not in self.ItemsAll:
									self.ItemsAll.append(I_new) #存入总列表
							new_item=True		
			new_item=False

		#完成了I0的所有自己的四个状态子集


		self.ItemsAll.insert(0,self.find_closure([starting]))
		count = 0
		self.ACTION = {}
		
		# print('*********************')
		# for item in self.ItemsAll:
		# 	count+=1
		# 	for num in item:
		# 		x=list(num[0]).index('.')+2
		# 		y=len(num[0])
		# 		if x<y:
		# 			elem=list(num[0]).index('.')+1
		# 			gotoElem=list(num[0])[elem]
		# 			IJ= self.GOTO(num,gotoElem)
		# 			#print(IJ)
		# 			if IJ in self.ItemsAll:
		# 				#print('aa')
		# 				#print(num)
		# 				index = self.ItemsAll.index(IJ)
		# 				last = list(num[0])[len(num[0])-1]
		# 				self.ACTION[str(count-1)+'+'+gotoElem]="shift "+str(index)
		# 		else:
		# 			listy=list(num[0]).index('.')
		# 			el=num[0][listy+1]
		# 			self.ACTION[str(count-1)+'+'+el]="reduce "+num[0][:listy]

		# 		#print(num[0])
			
		# values = list(self.ACTION.values())

		#设置ACC
		# for value in values:
		# 	if value == 'reduce ^::=S' :
		# 		index = values.index(value)
		# key = list(self.ACTION)[index]
		# self.ACTION[key] = "ACC"



		# print("ACTION and GOTO Table")
		# print(self.ACTION)
		# print('*************************')

		print('**** All States Are ****')
		for i in self.ItemsAll:
			print('State ',self.ItemsAll.index(i))
			print(i)
			print('*********************')



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

	LR1 = LR1Table(LR1_grammer_rules=LR1_gram)
	# print("-"*20)
	# # print(LR1.allItems)
	# print(LR1.ItemsAll)
	

