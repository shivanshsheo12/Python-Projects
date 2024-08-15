import random
n = random.randint(1,100)

a = -1
guess = 0
while(a != n):
    a = int(input("Guess the number : "))
    if(a>n):
        print("Lower number please")
        guess += 1
    elif(a<n):
        print("Higher number Please")
        guess += 1
    
print(f"You have guessed the number {n} in {guess} attempt")