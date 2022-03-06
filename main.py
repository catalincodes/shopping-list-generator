import sys
import re
import habitica


class ShoppingItem:
    def __init__(self, name, price, qty, store):
        self.name = name
        self.price = price
        self.qty = qty
        self.store = store

    def toString(self):
        return "{} - {} - {}({})".format(self.name, self.price, self.store, self.qty)


def GetListFromUser():
    userInput = ""
    shoppingList = []

    while userInput != "stop":
        userInput = input("Name: ")
        if userInput == "stop":
            break
        name = userInput
        userInput = input("Price: ")
        if userInput == 0:
            continue
        price = userInput
        userInput = input("Qty: ")
        if userInput == 0:
            continue
        qty = userInput
        userInput = input("Store: ")
        store = userInput
        newEntry = ShoppingItem(name, price, qty, store)
        shoppingList.append(newEntry)
    return shoppingList


def ReadFromFile(filename):
    shoppingList = []
    f = open(str(filename), "rt")
    try:
        with open(str(filename), "rt") as file:
            for line in f:
                line = line.rstrip("\n")
                firstParse = line.split(" - ")
                secondParse = re.split(r"\(|\)", firstParse[2])
                name = firstParse[0]
                price = firstParse[1]
                qty = secondParse[1]
                store = secondParse[0]
                newEntry = ShoppingItem(name, price, qty, store)
                shoppingList.append(newEntry)
            f.close()
    except IOError:
        print("ERROR OPENING FILE")
    return shoppingList


def IsUserSaving():
    userInput = input("Do you wish to save (yes/no)?")
    if userInput == "yes":
        return True
    return False


def IsUserPostingToHabitica():
    userInput = input("Do you wish to send list to Habitica (yes/no)?")
    if userInput == "yes":
        return True
    return False


def PrintToFile(filename, shoppingList):
    f = open(str(filename), "wt")
    try:
        with open(str(filename), "rt") as file:
            for si in shoppingList:
                f.write(si.toString())
            f.close()
    except IOError:
        print("ERROR OPENING FILE")


def ConvertShoppingListToStringArray(shoppingList):
    resultArray = []
    for item in shoppingList:
        resultArray.append(item.toString())
    return resultArray


shoppingList = []
if len(sys.argv) == 1:
    shoppingList = GetListFromUser()
    if IsUserSaving():
        PrintToFile("grocery.txt", shoppingList)
elif len(sys.argv) == 2:
    filename = sys.argv[1]
    shoppingList = ReadFromFile(filename)


for si in shoppingList:
    print(si.toString())

if IsUserPostingToHabitica():
    shoppingListAsStrings = ConvertShoppingListToStringArray(shoppingList)
    habitica.pushTaskToHabitica("Groceries|Test", shoppingListAsStrings)
