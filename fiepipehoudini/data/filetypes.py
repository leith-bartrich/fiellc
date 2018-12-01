import typing


def get_extensions_pattern(master_extensions: typing.List[str], prepend: str = "") -> typing.List[str]:
    ret = []
    houdini_filetype_postpends = ['', 'lc', 'nc']
    for master_extension in master_extensions:
        stripped_extension = master_extension.lstrip("*").lstrip(".")
        for postpend in houdini_filetype_postpends:
            ret.append(prepend + stripped_extension + postpend)
    return ret


def get_hip_extensions(prepend: str = "") -> typing.List[str]:
    houdini_filetype_patterns = ['*.hip']
    return get_extensions_pattern(houdini_filetype_patterns, prepend)


def get_geo_extensions(prepend: str = "") -> typing.List[str]:
    houdini_filetype_patterns = ['*.bgeo', '*.geo']
    return get_extensions_pattern(houdini_filetype_patterns, prepend)


def get_digasset_extensions(prepend: str = "") -> typing.List[str]:
    houdini_filetype_patterns = ['*.hda']
    return get_extensions_pattern(houdini_filetype_patterns, prepend)


def get_all_extensions(prepend: str = "") -> typing.List[str]:
    ret = []
    ret.extend(get_hip_extensions(prepend))
    ret.extend(get_geo_extensions(prepend))
    ret.extend(get_digasset_extensions(prepend))
    return ret
