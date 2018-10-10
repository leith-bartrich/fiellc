import typing

from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines


def get_patterns(routines: GitAssetRoutines, patterns: typing.List[str]):
    if routines.has_config("freecad"):
        # native
        patterns.append("*.fcstd")

        # supported 3d
        patterns.append("*.step")
        patterns.append("*.iges")
        patterns.append("*.igs")
        patterns.append("*.obj")
        patterns.append("*.stl")
        patterns.append("*.dxf")
        patterns.append("*.svg")
        patterns.append("*.dae")
        patterns.append("*.ifc")
        patterns.append("*.off")
        patterns.append("*.vrml")
        patterns.append("*.wrl")
        patterns.append("*.csg")
