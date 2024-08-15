import random
'''
snake = 1
water = 0
gun = -1

'''
computer = random.choice([1,-1,0])
you = input("Enter your choice : ")
yourdict = {
    "Snake" : 1,
    "Water" : 0,
    "Gun" : -1
}
reversedict = {
    1 : "Snake",
    0 : "Water",
    -1 : "Gun"
}
yourchoice = yourdict[you]
result = computer - yourchoice

print(f"You choose {you}\nComputer choose {reversedict[computer]}")
'''
win = snake - gun = 2
win = gun - water = -1
win = water - snake = -1

loose = gun - snake = -2
loose = water - gun = 1
loose = snake - water = 1

tie = same = 0
'''
if(result == 2 or result == -1):
    print("You win! :)")
elif(result == -2 or result == 1):
    print("You loose :(")
elif(result == 0):
    print("Its a tie :|")

