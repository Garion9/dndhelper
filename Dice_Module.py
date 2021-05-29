import random as r

def roll_dice(count, faces):
    result = 0
    while count:
        roll = r.randint(1, faces)
        #print("roll: ", roll)
        result += roll
        count -= 1
    return result

def roll_d4(count=1):
    return roll_dice(count, 4)

def roll_d6(count=1):
    return roll_dice(count, 6)

def roll_d8(count=1):
    return roll_dice(count, 8)

def roll_d10(count=1):
    return roll_dice(count, 10)

def roll_d12(count=1):
    return roll_dice(count, 12)

def roll_d20(count=1):
    return roll_dice(count, 20)

def roll_d100(count=1):
    return roll_dice(count, 100)
