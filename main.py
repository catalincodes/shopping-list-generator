import sys
from core import (
    IsUserPostingToHabitica,
    GetListFromUser,
    IsUserSaving,
    PrintToFile,
    ReadFromFile,
    ConvertShoppingListToStringArray,
)
from habitica import pushTaskToHabitica


def GetShoppingList():
    shoppingList = []
    if len(sys.argv) == 1:
        shoppingList = GetListFromUser()
        if IsUserSaving():
            PrintToFile("grocery.txt", shoppingList)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        shoppingList = ReadFromFile(filename)
    return shoppingList


shoppingList = GetShoppingList()

for si in shoppingList:
    print(si.toString())

if IsUserPostingToHabitica():
    shoppingListAsStrings = ConvertShoppingListToStringArray(shoppingList)
    pushTaskToHabitica("Groceries", shoppingListAsStrings)
