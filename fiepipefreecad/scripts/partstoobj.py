import FreeCAD
import os
import os.path
import Part
import math
import Mesh
import MeshPart


def filterBodies(objects):
    ret = []
    for o in objects:
        if o.TypeId == "PartDesign::Body":
            ret.append(o)
    return ret

def filterParts(objects):
    ret = []
    for o in objects:
        if o.TypeId == "App::Part":
            ret.append(o)
    return ret


def filterVisible(objects):
    ret = []
    for o in objects:
        if o.ViewObject.Visibility == True:
            ret.append(o)	
    return ret

def partToExportableList(part, subParts=False):
    ret = []
    for o in part.Group:
        if o.TypeId == "App::Part":
            if subParts:
                ret.extend(partToExportableList(o))
        elif o.TypeId == "PartDesign::Body":
            ret.append(o)
    return ret

if __name__ == "__main__":

    allObjects = App.ActiveDocument.Objects
    
    
    toExport = filterParts(allObjects)
    filePath = App.ActiveDocument.FileName
    dirPath = os.path.dirname(filePath)
    exportPath = os.path.join(dirPath,App.ActiveDocument.Name + ".representations","obj_dir")
    if not os.path.exists(exportPath):
        os.makedirs(exportPath)
    App.Console.PrintMessage(exportPath + "\n")
    
    scalar = App.Matrix()
    scalar.scale(0.1,0.1,0.1)
    rotator = App.Matrix()
    
    rotator.rotateX(math.radians(-90.0))
    
    for o in toExport:
        App.Console.PrintMessage("Exporing: " + o.Name  + "\n")
        bodies = partToExportableList(o,subParts=False)
        m = Mesh.Mesh()
        for b in bodies:
            App.Console.PrintMessage(b.TypeId)
            m.addMesh(MeshPart.meshFromShape(Shape=b.Shape,Fineness=2,SecondOrder=0,Optimize=1,AllowQuad=1))
        f = App.ActiveDocument.addObject("Mesh::Feature", o.Name + "_Mesh")
        m.transform(scalar)
        m.transform(rotator)
        f.Mesh = m
        Mesh.export([f], os.path.join(exportPath, App.ActiveDocument.Name + "_" + o.Name + ".obj"))
        
    exit()
    