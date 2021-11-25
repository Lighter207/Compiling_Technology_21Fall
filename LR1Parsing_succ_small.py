# =============================================================================
# Created By  : Huang Chanjuan
# Created Date: Thu November 25 14:27:00 GMT+8 2021
# =============================================================================


from LR1GetTable import LR1Table

LR1_gram = [ #d means dot(.) 该文法来自课本P77 例4-21 算法输出结果符合表4-19 
	'^::=S$',
	'S::=LdS',
	'S::=L',
	'L::=x',
	'L::=y'
]

input_sentence = 'xdydx' #输入来自于课本，x,y,x

class LR1Parser(LR1Table):
	def __init__(self, grammerrules) -> None:
		LR1Table.__init__(self,grammerrules)

		print("-------State_dict-----------")
		print(self.state_set_dict)
	
		print("-------DFA relation-----------")
		print(self.DFA_relations)
		
		self.state_stack = [0]
		self.parse_stack = ['$']
		self.input_stack = list(input_sentence)
		self.input_stack.append('$') # 加入终止符$
		
		self.lr1_table = self.ACTIONGOTO_df

		print("-------ACTION GOTO TABLE-----------")
		print(self.lr1_table)

		print("-------LR1 PARSE START-----------")
		print(self.parse_stack,end='\t')
		print(self.state_stack,end='\t')
		print(self.input_stack,end='\t')

		self.parse()

	def look_up_table(self,state,ch):
		
		try:
			value = self.lr1_table['value'][(self.lr1_table['State']==state) & (self.lr1_table['V']==ch)]
			value = value.to_list()
			value = value[0]

			return value

		except Exception as e:
			print(e)
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
				case 'shift' | 'goto':
					self.parse_stack.append(current_input_ch)
					
					self.state_stack.append(int(action_cm))
					
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
					self.state_stack.append(int(action_num))

					

					current_state = self.state_stack[-1]
					current_input_ch = self.input_stack[0]
					print(action)
					print(self.state_stack,end='\t')
					print(self.parse_stack,end='\t')
					print(self.input_stack,end='\t')
					
					action = self.look_up_table(current_state,current_input_ch)
					if(action == -1):
						print("Not Found in table")
						return

				case _:
					print("ERROR, action not reduce or shift or goto")
					print(action)
					break
		else:
			print("PARSE FINISHED")


if __name__ == '__main__':
	LR1Parser(LR1_gram)
