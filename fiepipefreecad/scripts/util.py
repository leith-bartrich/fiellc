import os
import os.path
import pathlib


def GetScriptPath(filename:str):
    moduleDir = os.path.dirname(__file__)
    ret = os.path.join(moduleDir,filename)
    return ret