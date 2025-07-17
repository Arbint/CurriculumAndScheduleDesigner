import os

def GetPrjDir():
    srcDir = os.path.dirname(__file__)
    prjDir = os.path.dirname(os.path.dirname(srcDir))
    return prjDir
