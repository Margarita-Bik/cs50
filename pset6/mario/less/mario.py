from cs50 import get_int

def main():
    n = get_height()
    for i in range(n):
        for j in range(n):
            if j < n - i -1 :
                print(" ", end="")
            else:
                print("#", end="")
        print()
  
         
    

def get_height():
    while True:
        n = get_int("Height: ")
        if n > 0 and n < 9 :
            break
    return n
            
main()
            


