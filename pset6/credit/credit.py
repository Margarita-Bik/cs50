from cs50 import get_int

card = get_int("Number: ")
c = card
i = 0

while c > 1:
    c = c/10
    i = i + 1

if not i == 13 and not i == 15 and not i == 16:
    print("INVALID")
    exit(1)
    
n = card
s1 = 0
s2 = 0

while True:
    m1 = int(n % 10)
    n = n/10
    s1 = s1 + m1
  
    m2 = int(n % 10)
    n = n / 10
    
    m2 = m2 * 2
    mm1 = int(m2 % 10)
    mm2 = int(m2 / 10)
      
    s2 = s2 + mm1 + mm2
    
    if n < 1:
        break

total = int(s1 + s2)

if not total % 10 == 0:
    print("INVALID")
    exit(0)

num = card

while True:
    num = int(num / 10)
    if num < 99:
        break

if i == 16 and int(num / 10) == 5 and int(num % 10) > 0 and int(num % 10) < 6:
    print("MASTERCARD")
elif i == 15 and int(num / 10) == 3:
    if int(num % 10) == 4 or int(num % 10) == 7:
        print("AMEX")
elif i == 13 or i == 16 and int(num /10) == 4:
    print("VISA")
else:
    print("INVALID")



    
    
    
    

