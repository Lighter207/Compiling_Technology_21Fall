# import pandas as pd
import numpy as np
from C_word_process import WordProcess

#先手动消除左递归得到报告中的文法
class LL1Recur(WordProcess):
    def __init__(self, filename) -> None:
        super().__init__(filename)
        # print(self.token_df)

        self.token_df['final_table'] = self.token_df['token']
        self.token_df.loc[self.token_df.token_num == 2, ['final_table']] = 'id'
        self.token_df.loc[self.token_df.token_num == 25, ['final_table']] = 'num'

        self.final_table = self.token_df['final_table'].to_list()
        self.token_num = self.token_df['token_num'].to_list()

        for i in self.final_table:
            print(i,end=' ')
        print("\n语法分析开始:")

        self.pointer = 0
        # print(type(self.lookahead_token_num)) 

        #start LL analysis
        self.program()
    
    def program(self):
        print("program-->block")
        self.block()

    def block(self):
        print("block --> {stmts}")
        self.match("{")
        self.stmts()
        self.match("}")


    def stmts(self):
        
        if (self.token_num[self.pointer] == 39): 
            print("stmts --> null")
            return #TODO
        print("stmts --> stmt stmts")
        self.stmt()
        self.stmts()
            

    def stmt(self):
        
        match self.token_num[self.pointer]:
            case 2:
                print("stmt --> id = expr;")
                self.match("id")
                self.match("=")
                self.expr()
                self.match(";")

            case 3:
                
                self.match("if")
                self.match("(")
                self.bool()
                self.match(")")
                self.stmt()
                if (self.final_table[self.pointer] == 'else'):
                    print("stmt --> if (bool) stmt else stmt")
                    self.match("else")
                    self.stmt()
                else : 
                    print("stmt --> if (bool) stmt")


            case 5:
                print("stmt --> while (bool) stmt")
                self.match("while")
                self.match("(")
                self.bool()
                self.match(")")
                self.stmt()
            case 6:
                print("stmt --> do stmt while (bool)")
                self.match("do")
                self.stmt()
                self.match("while")
                self.match("(")
                self.bool()
                self.match(")")
            case 15:
                print("stmt --> break")
                self.match("break")
            case 38: #"{"
                print("stmt --> block")
                self.block()
            case _: 
                print("ERROR")
    


    def bool(self):
        self.expr()
        match self.token_num[self.pointer]:
            case 34: #"<"
                print("bool --> expr < expr")
                self.match("<")
                self.expr()
            case 35: #"<"
                print("bool --> expr <= expr")
                self.match("<=")
                self.expr()
            case 36: #">"
                print("bool --> expr > expr")
                self.match(">")
                self.expr()
            case 37: #">="
                print("bool --> expr >= expr")
                self.match(">=")
                self.expr()
            case _ : 
                print("bool --> expr")
                #TODO
                


    def expr(self):
        print("expr --> term expr1")
        self.term()
        self.expr1()

    def expr1(self):
        match self.token_num[self.pointer]:
            case 28: #"+"
                print("expr1 --> + term expr1")
                self.match("+")
                self.term()
                self.expr1()
            case 29: #"-"
                print("expr1 --> - term expr1")
                self.match("-")
                self.term()
                self.expr1()
            case _:
                print("expr1 --> null")
                #TODO
   
    def term(self):
        print("term --> factor term1")
        self.factor()
        self.term1()
    
    def term1(self):
        match self.token_num[self.pointer]:
            case 30: #"*"
                print("term1 --> * factor term1")
                self.match("*")
                self.factor()
                self.term1()
            case 31: #"/"
                print("term1 --> / factor term1")
                self.match("/")
                self.factor()
                self.term1()
            case _:
                print("term1 --> null")

    def factor(self):
        match self.token_num[self.pointer]:
            case 40:
                print("factor --> (expr)")
                self.match("(")
                self.expr()
                self.match(")")
            case 2:
                print("factor --> id")
                self.match("id")
            case 25:
                print("factor --> num")
                self.match("num")
            case _:
                print("ERROR factor")

    # def error_handle(self, error_num, line_num):
    #     return super().error_handle(error_num, line_num)
    def match(self,ch):
        if self.final_table[self.pointer] == ch:
            pass
        else :
            print("ERROR")
            return
        
        self.pointer += 1;

if __name__ == "__main__":
    LL1Recur("lltest.c")