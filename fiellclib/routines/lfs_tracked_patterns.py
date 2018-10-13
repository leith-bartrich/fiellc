import typing

from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines


def get_patterns(routines: GitAssetRoutines, patterns: typing.List[str]):

    if routines.container.GetFQDN() == "fie.us":

        #ithoughts
        patterns.append("*.itmz")

        #krita
        patterns.append("*.kra")

        #sketchbook
        patterns.append("*.skba")

        #houdini
        patterns.append("*.hip")
        patterns.append("*.hiplc")
        patterns.append("*.hipnc")
        patterns.append("*.bgeo")
        patterns.append("*.geo")
        patterns.append("*.poly")
        patterns.append("*.bpoly")
        patterns.append("*.d")
        patterns.append("*.rib")
        patterns.append("*.pc")
        patterns.append("*.pic")
        patterns.append("*.pic.Z")
        patterns.append("*.rat")





