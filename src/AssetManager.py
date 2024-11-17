import PathUtility
import os

def GetFinishedIcon():
    return os.path.join(GetAssetDirName(), "finished.png")

def GetAssetDirName():
    return os.path.join(PathUtility.GetPrjDir(), "assets")
