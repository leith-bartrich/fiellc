import typing

from fiepipeloosefiles.routines.assetaspect import LooseFilesAspectConfigurationRoutines

def get_patterns(routines: LooseFilesAspectConfigurationRoutines, patterns: typing.List[str]):

        # native
        patterns.append(".fcstd")

        # supported 3d
        patterns.append(".step")
        patterns.append(".iges")
        patterns.append(".igs")
        patterns.append(".obj")
        patterns.append(".stl")
        patterns.append(".dxf")
        patterns.append(".svg")
        patterns.append(".dae")
        patterns.append(".ifc")
        patterns.append(".off")
        patterns.append(".vrml")
        patterns.append(".wrl")
        patterns.append(".csg")
