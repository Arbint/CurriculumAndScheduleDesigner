import json
import os
from degreeplaner.CourseList import CourseListModel

def ConvertModelsToJson(models: list[CourseListModel]):
    data = {}
    for model in models:
        data[model.listName] = model.CoursesToJsonList()

    return data

def LoadJsonDictFromPath(jsonPath)->dict:
    with open(jsonPath, 'r') as jsonFile:
        data = json.load(jsonFile)
        return data

def SaveModelsToJson(models: list[CourseListModel], savePath):
    data = ConvertModelsToJson(models)
    SaveToJson(data, savePath)

def SaveToJson(jsonDict, savePath):
    with open(savePath, "w") as jsonFile:
        json.dump(jsonDict, jsonFile, indent=4)