from numpy import e
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
		';' : 'z'
	}


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




class LR1Parser(WordProcess,LR1Table):
	def __init__(self, filename,grammerrules) -> None:
		super().__init__(filename)
		self.state_stack = ['0']
		self.parse_stack = ['$']
		self.input_stack = []
		
		# print(self.input_stack)
		self.token_df['final_table'] = self.token_df['token']
		self.token_df.loc[self.token_df.token_num == 2, ['final_table']] = 'id'
		self.token_df.loc[self.token_df.token_num == 25, ['final_table']] = 'num'
		self.final_table = self.token_df['final_table'].to_list() #将id和num修改为终止符表示
		
		#将Vt和Vn表示为单个alias
		for ch in self.final_table:
			self.input_stack.append(alias_dict[ch])

		self.input_stack.append('$') # 加入终止符$
		# print(self.input_stack)
		self.lr1_table = LR1Table(grammerrules).ACTION
		self.positions = list(self.lr1_table.keys())
		self.positions_x = [i.split("+")[0] for i in self.positions]
		self.positions_y = [i.split("+")[-1] for i in self.positions]

		print(self.parse_stack,end='\t')
		print(self.state_stack,end='\t')
		print(self.input_stack)

		self.parse()

	def look_up_table(self,state,ch):
		
		# print(positions_x)

		actions = list(self.lr1_table.values())
		# print(actions)
		
		indices = [i for i, x in enumerate(self.positions_x) if x == state] #sugar

		for index in indices:
			if (self.positions_y[index] == ch):
				return actions[index]
		
		return -1 #Not found, goes into error handling
		

	def parse(self):
		current_state = self.state_stack[-1]
		current_input_ch = self.input_stack[0]
		
		action = self.look_up_table(current_state,current_input_ch)
		if action == -1:
			print("ERROR, look up table failed.")
			print(current_state,current_input_ch)
			return
		
		while (action != "ACC"):
			action_op = action.split(" ")[0]
			action_cm = action.split(" ")[-1]
			match action_op:
				case 'shift':
					self.parse_stack.append(current_input_ch)
					
					self.state_stack.append(action_cm)
					
					self.input_stack = self.input_stack[1:]

					print(action)
					print(self.state_stack,end='\t')
					print(self.parse_stack,end='\t')
					print(self.input_stack,end='\t')
					

					current_state = self.state_stack[-1]
					current_input_ch = self.input_stack[0]
					action = self.look_up_table(current_state,current_input_ch)
					if(action == -1):
						print("Not Found in table")
						return


				case 'reduce':
					length = len(action_cm.split("::=")[-1])
					for i in range(length): 
						#状态站出栈
						self.state_stack.pop()
						current_state = self.state_stack[-1]
						#栈中符号出栈
						self.parse_stack.pop()
					#压入Vn
					self.parse_stack.append(action_cm.split("::=")[0])
					current_parse_ch = self.parse_stack[-1]
					#查找GOTO表，压入状态栈
					action_1 = self.look_up_table(current_state,current_parse_ch)
					if(action_1 == -1):
						print("Not Found action_1 in table")
						return
					action_num = action_1.split(" ")[-1]
					self.state_stack.append(action_num)

					

					current_state = self.state_stack[-1]
					current_input_ch = self.input_stack[0]
					action = self.look_up_table(current_state,current_input_ch)
					if(action == -1):
						print("Not Found in table")
						return

					print(action)
					print(self.state_stack,end='\t')
					print(self.parse_stack,end='\t')
					print(self.input_stack,end='\t')
					

				case _:
					print("ERROR, action not reduce or shift")
					break
		else:
			print("PARSE FINISHED")


if __name__ == '__main__':
	LR1Parser('LR1_test.c',MyGram)