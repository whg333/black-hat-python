def sum(num1, num2):
    num1_int = parseInt(num1)
    num2_int = parseInt(num2)
    
    result = num1_int + num2_int
    
    return result

def parseInt(num):
    return int(num)

if(__name__=="__main__"):
    sum = sum("1", "2")
    print sum