import typing

from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines


def get_patterns(routines: GitAssetRoutines, patterns: typing.List[str]):

    if routines.has_config("coat3d"):

        #native
        patterns.append("*.3b")

        #supported 3d
        patterns.append("*.fbx")
        patterns.append("*.obj")
        patterns.append("*.lwo")
        patterns.append("*.stl")
        patterns.append("*.ply")
        patterns.append("*.dae")
        patterns.append("*.wrl")

        #supported 2d
        patterns.append("*.tga")
        patterns.append("*.tif")
        patterns.append("*.tiff")
        patterns.append("*.png")
        patterns.append("*.exr")
        patterns.append("*.bmp")
        patterns.append("*.dds")
        patterns.append("*.jpg")
        patterns.append("*.hdr")





