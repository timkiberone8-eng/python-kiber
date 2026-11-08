a = int (input("a"))
b = int (input("b"))
n = int (input("n"))

pauses = n // a 
# // игнор дробных чисел
if n % a == 0:
    pauses = pauses - 1

total = n + pauses * b

print(total)