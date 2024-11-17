import json
from CourseList import CourseListModel


def ConvertModelsToJson(models: list[CourseListModel]):
    data = {}
    for model in models:
        data[model.listName] = model.ClassesToJsonList()

    return data

def ConvertJsonToModels(jsonPath: str):
    pass

