import typing
import pkg_resources
from fieui.FeedbackUI import AbstractFeedbackUI

def get_houdini_job_paths(fqdn:str, container_id:str, root_id:str, asset_id:str, feedback_ui:AbstractFeedbackUI) -> typing.List[str]:
    entrypoints = pkg_resources.iter_entry_points("fiepipe.houdini.houdini_job_paths")
    ret = []
    for entrypoint in entrypoints:
        method = entrypoint.load()
        ret.extend( method(fqdn,container_id,root_id,asset_id,feedback_ui) )
    return ret

def get_houdini_site_paths(fqdn:str, container_id:str, root_id:str, asset_id:str, feedback_ui:AbstractFeedbackUI) -> typing.List[str]:
    entrypoints = pkg_resources.iter_entry_points("fiepipe.houdini.houdini_site_paths")
    ret = []
    for entrypoint in entrypoints:
        method = entrypoint.load()
        ret.extend( method(fqdn,container_id,root_id,asset_id,feedback_ui) )
    return ret
