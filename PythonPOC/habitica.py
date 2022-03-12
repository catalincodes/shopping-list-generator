import os
import requests
from dotenv import load_dotenv


def prepareArrayForCheckList(stringArray):
    resultingArray = []
    for item in stringArray:
        resultingArray.append({"text": item})
    return resultingArray


def createTaskData(title, checklistItems):
    taskData = {}
    taskData["text"] = title
    taskData["type"] = "todo"
    checklist = prepareArrayForCheckList(checklistItems)
    taskData["checklist"] = checklist
    taskData["priority"] = 2
    return taskData


def generateHeaders():
    load_dotenv()
    USER_ID = os.getenv("HABITICA_USER_ID")
    USER_API_KEY = os.getenv("HABITICA_USER_API_KEY")
    headers = {}
    headers["x-api-user"] = "{}".format(USER_ID)
    headers["x-api-key"] = "{}".format(USER_API_KEY)
    headers["x-client"] = "{}-GroceryListToHabitica".format(USER_ID)
    return headers


def addTaskToHabitica(headers, taskData):
    url = "{}/api/v3/tasks/user".format(os.getenv("HABITICA_URL"))
    print(taskData)
    x = requests.post(url, json=taskData, headers=headers)
    if x.status_code == 201:
        print("Successfully added task")
    elif x.status_code == 400:
        print("Error!")
        print(x.text)
    else:
        print("Unhandled Response")
        print(x.text)


def pushTaskToHabitica(title, checklistItems):
    taskData = createTaskData(title, checklistItems)
    httpHeaders = generateHeaders()
    addTaskToHabitica(httpHeaders, taskData)
