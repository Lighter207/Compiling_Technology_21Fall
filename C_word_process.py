# =============================================================================
# Created By  : Huang Chanjuan
# Created Date: Thu November 25 14:27:00 GMT+8 2021
# =============================================================================

import string
import pandas as pd


class TokenError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)




class WordProcess :
    lines = []
    tokens = [] # eg. element 1 {line_num: 1 , token:main, token_num: 1}
    keywords = ["if","else","while","do","main","int","float","double","return",
                "const","void","continue","break","char","unsigned","enum",
                "long","switch","case","signed","auto","static"]

    def __init__(self,filename) -> None:
        '''Get_file in lines[] first, then get_token to extract the tokens 
            into a token table. error_handle is included.
        '''
        self.f_name = filename
        self.multiline_anno_flag = 0
        self.get_file()
        print(self.lines)
        self.get_token()
        # print(self.tokens)
        self.token_df = pd.DataFrame.from_dict(self.tokens)
        # print(self.token_df)
        

    def get_file(self):
        '''Get file in lines, store all data in lines[]
           without empty spaces and \n '''
        with open(self.f_name,'r') as f:
            for line in f.readlines():
                line = line.replace(" ","") #get rid of all empty spaces
                line = line.strip() #get rid of all new line \n
                self.lines.append(line)


    def get_token(self):
        '''Get token and line number, output (token,token_num)
            if error, output error message and line_num'''
        #init 
        error_num = 0
        local_line_num = 0
        local_token = ""
        local_token_num = 0 
        
        for line in self.lines:
            #init
            local_line_num += 1
            line_element_index = 0
            
            while (line_element_index<len(line)):
                element = line[line_element_index] #element is a string no matter what
                if (self.multiline_anno_flag == 0): #没有开始多行注释，正常匹配
                    match element:
                        case ';':
                            local_token_num = 1
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case 'a'|'b'|'c'|'d'|'e'|'f'|'g'|'h'|'i'|'j'|'k'|'l'|'m'|'n'|'o'|'p'|'q'|'r'|'s'|'t'|'u'|'v'|'w'|'x'|'y'|'z'|'A'|'B'|'C'|'D'|'E'|'F'|'G'|'H'|'I'|'J'|'K'|'L'|'M'|'N'|'O'|'P'|'Q'|'R'|'S'|'T'|'U'|'V'|'W'|'X'|'Y'|'Z'|'_' : #匹配变量名（标识符）和keyword
                            local_token_num = 2
                            local_token += element
                            while(line[line_element_index+1] in (string.ascii_letters + string.digits + '_')):
                                line_element_index += 1 #jump to the next ch
                                local_token += line[line_element_index] #add the next ch into local_token
                            if(local_token.isalpha): #if this word contains only alphabets
                                for i in range(len(self.keywords)):
                                    if local_token == self.keywords[i]:
                                        local_token_num = i+1+local_token_num #if the word turns out to be a keyword
                            
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9' : #TODO float and other things not done yet
                            local_token_num = 25 #integer
                            local_token += element #TOOD: check if we can remove the str()
                            while(line[line_element_index+1] in (string.digits ) ):
                                line_element_index += 1 #jump to the next ch
                                local_token += line[line_element_index] #add the next ch into local_token
                        
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = ""
                            line_element_index += 1 
                        
                        case "\'": #character
                            local_token_num = 26 #TODO temp num
                            if (line_element_index+2 < len(line) ):
                                lookahead = line[line_element_index+1,line_element_index+3] #look ahead 2
                            else :
                                error_num = 1 # '后为空则报错
                                self.error_handle(error_num,local_line_num)

                            if (not lookahead[0].isalpha()): #TODO 字符变量内非字符 还有各种\0 \n之类的
                                error_num = 2
                                self.error_handle(error_num,local_line_num)
                            else :
                                local_token += element
                                local_token += lookahead
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "\"": #string 
                            local_token_num = 27 #TODO temp num
                            while(line[line_element_index+1] != "\""):
                                line_element_index += 1 #jump to the next ch
                                local_token += line[line_element_index] #add the next ch into local_token
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "+":
                            local_token_num = 28
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "-":
                            local_token_num = 29
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "*":
                            local_token_num = 30
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "/": 
                            local_token_num = 31
                            local_token += element
                            if (line[line_element_index+1]== '/'): #单行注释
                                local_token = "" #recover 
                                break #跳过这一行
                            elif (line[line_element_index+1]== '*') : #多行注释 
                                local_token = "" #recover 
                                line_element_index += 1
                                while(line_element_index < len(line)-1):#先检测是否在这行内含有结束符
                                    if(line[line_element_index:line_element_index+2] == "*/"):
                                        self.multiline_anno_flag = 0 #多行注释在本行内结束\
                                        line_element_index += 2
                                        break
                                    else:
                                        line_element_index += 1
                                        self.multiline_anno_flag = 1 #多行注释活跃中
                                
                            else: # just /
                                self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                                local_token = "" #recover 
                                line_element_index += 1 
                        
                        case "=":
                            local_token_num = 32
                            local_token += element
                            if(line[line_element_index+1] == '='): #'=='
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 33
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "<":
                            local_token_num = 34
                            local_token += element
                            if(line[line_element_index+1] == '='): #'<='
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 35
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case ">":
                            local_token_num = 36
                            local_token += element
                            if(line[line_element_index+1] == '='): #'>='
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 37
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case "{":
                            local_token_num = 38
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 
                        
                        case "}":
                            local_token_num = 39
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 
                        
                        
                        case "(":
                            local_token_num = 40
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 

                        case ")":
                            local_token_num = 41
                            local_token += element
                            self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                            local_token = "" #recover 
                            line_element_index += 1 
                        
                        case "!": # !=
                            local_token += element
                            if(line[line_element_index+1] == '='):
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 42
                                self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                                line_element_index += 1 
                            else :
                                self.error_handle(42,local_line_num)
                            local_token = "" #recover 

                        case "&": # &&
                            local_token += element
                            if(line[line_element_index+1] == '&'):
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 43
                                self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                                line_element_index += 1 
                            else: 
                                self.error_handle(43,local_line_num)
                            local_token = "" #recover

                        case "|": # ||
                            local_token += element
                            if(line[line_element_index+1] == '|'):
                                line_element_index += 1
                                local_token += line[line_element_index]
                                local_token_num = 44
                                self.tokens.append({"token":local_token,"token_num":local_token_num,"line_num":local_line_num})
                                line_element_index += 1 
                            else:
                                self.error_handle(44,local_line_num)
                            local_token = "" #recover 
                            
                        case _:
                            print(f"unknown character")
                else: #多行注释开始了，注释内的字符都不能写进tokens
                    match element:
                        case '*':
                            if(line[line_element_index+1] == '/'): #检测到多行注释结束符
                                line_element_index += 2
                                self.multiline_anno_flag = 0 #结束多行注释状态
                        case _:
                            line_element_index += 1


    def error_handle(self,error_num,line_num):
        print(f"Token error found in line {line_num}")
        match error_num:
            case 1:
                message = "Character error! No enclosing ' found!"
            case 2: 
                message = "Character variable not legitimate."
            case 42:
                message = "Single ! found!"
            case 43:
                message = "Single & found!"
            case 44:
                message = "Single | found!"
        raise TokenError(message)



if __name__ == "__main__":
    WP = WordProcess("C_Word_ProcessTest.c")
    print(WP.token_df)