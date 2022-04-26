from cs50 import get_string

text = get_string("Text: ")
letters = 0
words = 0
sentences = 0

for  i  in range(len(text)):
    if text[i].isalpha() == True:
        letters = letters + 1
    if text[i] == ' ':
        words = words + 1
    if text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences = sentences + 1
        
words = words + 1
#print(f"{letters}, letters")
#print(f"{words}, words")
#print(f"{sentences}, sentences")

L = float((letters/words)*100)
S = float((sentences/words)*100)
index = float(0.0588*L-0.296*S-15.8)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {round(index)}")