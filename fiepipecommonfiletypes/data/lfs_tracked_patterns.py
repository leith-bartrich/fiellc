import typing


def extensions_to_lfs_patterns(extensions: typing.List[str]) -> typing.List[str]:
    ret = []
    for ext in extensions:
        ret.append("*." + ext.lstrip('.'))

    return ret


def get_common_extensions(extensions: typing.List[str]):
    get_common_archive_extensions(extensions)
    get_image_extensions(extensions)
    get_common_archive_extensions(extensions)
    get_audio_extensions(extensions)
    get_video_extensions(extensions)
    get_publishing_extensions(extensions)
    get_msoffice_extensions(extensions)
    get_3d_extensions(extensions)
    get_executable_extensions(extensions)
    get_font_extensions(extensions)
    get_fie_extensions(extensions)


def get_image_extensions(extensions: typing.List[str]):
    # common image formats
    extensions.append(".jpg")
    extensions.append(".jpeg")
    extensions.append(".gif")
    extensions.append(".bmp")
    extensions.append(".png")
    extensions.append(".psd")
    extensions.append(".tga")
    extensions.append(".tif")
    extensions.append(".tiff")
    extensions.append(".exr")
    extensions.append(".cin")
    extensions.append(".dpx")
    extensions.append(".dds")
    extensions.append(".hdr")


def get_common_archive_extensions(extensions: typing.List[str]):
    # common archive formats
    extensions.append(".zip")
    extensions.append(".tar")
    extensions.append(".gz")
    extensions.append(".7z")
    extensions.append(".iso")
    extensions.append(".dmg")


def get_audio_extensions(extensions: typing.List[str]):
    # common audio formats
    extensions.append(".mp3")
    extensions.append(".m4a")
    extensions.append(".wav")
    extensions.append(".aif")
    extensions.append(".aiff")
    extensions.append(".wma")
    extensions.append(".ac3")
    extensions.append(".ogg")


def get_video_extensions(extensions: typing.List[str]):
    # common video formats
    extensions.append(".mpg")
    extensions.append(".avi")
    extensions.append(".flv")
    extensions.append(".mov")
    extensions.append(".m4v")
    extensions.append(".mp4")
    extensions.append(".wmv")
    extensions.append(".mxf")


def get_publishing_extensions(extensions: typing.List[str]):
    # common doc/publish formats
    extensions.append(".pdf")
    extensions.append(".eps")
    extensions.append(".ai")
    # patterns.append(".svg")


def get_msoffice_extensions(extensions: typing.List[str]):
    # common MS working files
    extensions.append(".doc")
    extensions.append(".dot")
    extensions.append(".wbk")
    extensions.append(".docx")
    extensions.append(".docm")
    extensions.append(".dotx")
    extensions.append(".dotm")
    extensions.append(".docb")

    extensions.append(".xls")
    extensions.append(".xlt")
    extensions.append(".xlm")
    extensions.append(".xlsx")
    extensions.append(".xlsm")
    extensions.append(".xltx")
    extensions.append(".xltm")
    extensions.append(".xlsb")
    extensions.append(".xla")
    extensions.append(".xlam")
    extensions.append(".xll")
    extensions.append(".xlw")

    extensions.append(".ppt")
    extensions.append(".pot")
    extensions.append(".pps")
    extensions.append(".pptx")
    extensions.append(".pptm")
    extensions.append(".potx")
    extensions.append(".potm")
    extensions.append(".ppam")
    extensions.append(".ppsx")
    extensions.append(".ppsm")
    extensions.append(".sldx")
    extensions.append(".sldm")

    extensions.append(".pub")
    extensions.append(".xps")


def get_3d_extensions(extensions: typing.List[str]):
    # common 3d mesh files
    extensions.append(".obj")
    extensions.append(".fbx")
    extensions.append(".lwo")
    extensions.append(".stl")
    extensions.append(".ply")
    extensions.append(".dae")
    extensions.append(".wrl")


def get_executable_extensions(extensions: typing.List[str]):
    # common executable files
    extensions.append(".exe")
    extensions.append(".com")
    extensions.append(".bin")
    extensions.append(".app")
    extensions.append(".apk")
    extensions.append(".jar")
    extensions.append(".dll")
    extensions.append(".so")
    extensions.append(".lib")
    extensions.append(".cab")
    extensions.append(".sys")


def get_font_extensions(extensions: typing.List[str]):
    # common font files
    extensions.append(".ttf")
    extensions.append(".otf")
    extensions.append(".fnt")


def get_fie_extensions(extensions: typing.List[str]):
    # ithoughts
    extensions.append(".itmz")

    # krita
    extensions.append(".kra")

    # sketchbook
    extensions.append(".skba")
