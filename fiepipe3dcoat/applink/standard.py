import fiepipe3dcoat.coat
import typing
import pathlib
import os
import os.path
import tempfile
import uuid
import math

class Mode (object):

    MODE_PerPixelPaint = "[ppp]"
    MODE_MircoVertexPaint = "[mv]"
    MODE_PTEXPaint = "[ptex]"
    MODE_UVMapping = "[uv]" #will ask about replacing or appending.  provides opportunity for uv set name on import.
    MODE_DropRefernce = "[ref]"
    MODE_DropRetopo = "[retopo]"
    MODE_DropAsVoxel = "[vox]"
    MODE_DropAsCombinedVoxel = "[voxcombine]"
    MODE_DropAsAlpha = "[alpha]"
    MODE_DropAsMergingPrimitive = "[prim]"
    MODE_DropAsCurveProfile = "[curv]"
    MODE_AutoRetopology = "[autopo]"
    MODE_3B = "[3B]"
    
    _mode = None
    
    def __init__(self, mode:str):
        self._mode = mode

class Texture(object):
    
    _materialName = None
    _uvName = None
    _usage = None
    _path = None
    
    def __init__(self, materialName, uvName, usage, path):
        self._materialName = materialName
        self._uvName = uvName
        self._usage = usage
        self._path = path
        

class Mesh(object):
    _path = None
    
    def __init__(self, path:str):
        self._path = path
    
    def __str__(self):
        return self._path


def StartRoundTrip(models:typing.List[Mesh],outModel:Mesh,mode:Mode,additionalOptions:typing.List[str]):
    """Starts a roundtrip to/from 3dcoat.
    """
    modelPaths = []
    for m in models:
        modelPaths.append(m._path)
    firstLine = ';'.join(modelPaths)
    if len(modelPaths) == 0:
        firstLine = ";"
    exdir = fiepipe3dcoat.coat.GetAppLinkExchangeDir()
    temppath = os.path.join(exdir, str(uuid.uuid4()))
    f = open(temppath, mode='w')
    f.write(firstLine + "\n")
    f.write(outModel._path + "\n")
    f.write(mode._mode + "\n")
    f.flush()
    f.close()
    p = pathlib.Path(temppath)
    targetPath = os.path.join(exdir,"import.txt")
    if ImportExists():
        os.unlink(targetPath)
    p.rename(targetPath)

def ImportExists():    
    exdir = fiepipe3dcoat.coat.GetAppLinkExchangeDir()
    p = pathlib.Path(os.path.join(exdir,"import.txt"))
    return p.exists()
    
def ExportExists():
    exdir = fiepipe3dcoat.coat.GetAppLinkExchangeDir()
    p = pathlib.Path(os.path.join(exdir,"export.txt"))
    return p.exists()

def MeshFromParameters(path:str):
    ret = Mesh(path)
    return ret


def EndRountrip() -> typing.Tuple[Mesh,typing.List[Texture]]:
    exdir = fiepipe3dcoat.coat.GetAppLinkExchangeDir()
    p = pathlib.Path(os.path.join(exdir,"export.txt"))
    f = p.open()
    m = Mesh(f.readline())
    f.close()
    t = pathlib.Path(os.path.join(exdir,"textures.txt"))
    f = t.open()
    textureLines = f.readlines()
    f.close()
    textures = []
    for i in range(0,math.floor(len(textureLines)/4)):
        t = Texture()
        t._materialName = textureLines[i*4]
        t._uvName = textureLines[(i*4) + 1]
        t._usage = textureLines[(i*4) + 1]
        t._path = textureLines[(i*4) + 1]
        textures.append(t)
    t.unlink()
    p.unlink()
    return (m, textures)
    
        
    
    