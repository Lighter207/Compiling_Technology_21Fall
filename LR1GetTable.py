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
			if N ==listItem[index+1]:
				return True
			if ' '== listItem[index+1]:
				return False
		except:
			return False

	def GOTO(self,I,N):
		'''
		Input: (Item,GrammarSymbol)
		Output: Closure of Item after shift grammar GrammarSymbol is performed

		Example: 
		Input: ['S::=.CC$'],C
		Output: [['S::=C.C$'], ['C::=.cC$'], ['C::=.d$']]

		'''
		J=[]
		for i in I:
			if self.check(i,N):
				new = self.shift_pos(i)
				J.append(new)

		if len(J) == 0:
			return([])

		return(self.find_closure([J]))

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


	def find_productions(self,B):
		'''
		Input: A non-terminal B
		Output: All Productions of B
		Example
		Input : 'S'
		Output: ['CC']
		'''
		if B=='$':
			return 1
		if B not in self.entryOfGram.keys():
			return 1
		return self.entryOfGram[B]

	def find_terminals_of(self,gram):
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

	def follow_of(self,item):
		'''
		input: An item
		output: The next non-terminal to be opened up

		Example
		input:'A::.AB'
		output: 'B'

		'''
		Item = item.replace(' ','')
		listItem = list(Item)
		try:
			index = listItem.index('.')
			return listItem[index+2]
		except IndexError:
			return '$'

	def find_closure(self,I):
		'''
		Input: Grammar I
		Output : Closure of Grammar

		Input: '^::=.S$''
		Output : [['^::=.S$'], ['S::=.aAd$'], ['S::=.bAc$'], ['S::=.aec$'], ['S::=.bed$']]

		where last element is the follow element.
		Example:
		In ['^::=.S$'] , $ is the follow of '^::=.S'


		'''
		add=1
		while (add!=0):
			add=0
			for item in I:
				element = item[0]
				giveElement = self.next_dot_pos(element)
				findPr = self.find_productions(giveElement)
				if findPr == 1:
					pass
				else:				
					for productions in findPr:
						first_set = First(grammar_rules=self.gram).first_set
						for b in first_set[self.follow_of(element)]:
							elem = [giveElement+'::=.'+productions+''+b]
							if elem not in I:
								I.append(elem)
								add=1
			return(I)
			break

	def __init__(self,LR1_grammer_rules):
		self.gram = LR1_grammer_rules
		starting='^::=.S$'

		self.entryOfGram = self.find_terminals_of(self.gram)
		I = [self.find_closure([[starting]])]
		#find_closure(GOTO(I[0],'d'))

		X = self.all_grammar_symbols(self.gram)

		self.allItems = {}
		self.ItemsAll = []
		new_item = True
		while new_item:
			new_item=False
			i=1
			for item in I:
				i+=1
				for g in X:
					if len(self.GOTO(item,g))!=0:
						goto = self.GOTO(item,g)
						flat_list = [[item] for sublist in goto for item in sublist]
						if flat_list not in I:
							index='I'+str(i)
							if index not in self.allItems.keys():
								self.allItems[index]=[g]
							else:
								self.allItems[index].append(g)	
							I.append(flat_list)
							Z=self.pre_process_states(flat_list)
							if (Z):
								if flat_list not in self.ItemsAll:
									self.ItemsAll.append(flat_list)
							
							new_item=True		
			new_item=False

		self.ItemsAll.insert(0,self.find_closure([[starting]]))
		i=0
		
		self.ACTION = {}
		

		print('*********************')
		for item in self.ItemsAll:
			i+=1
			for num in item:
				x=list(num[0]).index('.')+2
				y=len(num[0])
				if x<y:
					elem=list(num[0]).index('.')+1
					gotoElem=list(num[0])[elem]
					IJ= self.GOTO(num,gotoElem)
					#print(IJ)
					if IJ in self.ItemsAll:
						#print('aa')
						#print(num)
						index = self.ItemsAll.index(IJ)
						last = list(num[0])[len(num[0])-1]
						self.ACTION[str(i-1)+'+'+gotoElem]="shift "+str(index)
				else:
					listy=list(num[0]).index('.')
					el=num[0][listy+1]
					self.ACTION[str(i-1)+'+'+el]="reduce "+num[0][:listy]

				#print(num[0])
			

		print("ACTION and GOTO Table")
		print(self.ACTION)
		print('*************************')

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
	}
	original_names = list(alias_dict.keys())
	alias_names = list(alias_dict.values())

	'''Test:
		'^::=S$',
		'S::=aAd',
		'S::=bAc',
		'S::=aec',
		'S::=bed',
		'A::=e'
	'''
	'''MyGram:
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
			'G::=T' 
	'''
	gram = [
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
			'G::=T' 
		]

	LR1 = LR1Table(LR1_grammer_rules=gram)
	print("-"*20)
	# print(LR1.allItems)
	print(LR1.ItemsAll)
	

