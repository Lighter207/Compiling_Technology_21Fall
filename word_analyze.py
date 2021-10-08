import my_tokenize

with open("test.py",'rb') as f:
    tokens = my_tokenize.tokenize(f.readline)
    for toknum , tokval ,_,_,_ in tokens:
        print(toknum,tokval)