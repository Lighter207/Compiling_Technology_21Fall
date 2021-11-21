import string
def generate_match_or() :
    #string.digits和string.ascii_letters都是string类型
    print("|".join("\'"+i+"\'" for i in list(string.digits)))



