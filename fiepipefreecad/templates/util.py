import os
import os.path
import pathlib
import fiepipefreecad.data


def GetPackageTemplatesDict():
    moduleDir = os.path.dirname(__file__)
    ret = {}
    dirPath = pathlib.Path(moduleDir)
    for f in os.listdir(dirPath):
        p = pathlib.Path(os.path.join(str(dirPath),f))
        root, ext = os.path.splitext(f)
        if ext.lower() == ".fcstd":
            ret[root] = str(p)
    return ret