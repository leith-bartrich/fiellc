import typing

import pkg_resources

from fieui.FeedbackUI import AbstractFeedbackUI


async def get_houdini_site_paths(fqdn: str, container_id: str, root_id: str, asset_id: str,
                                 feedback_ui: AbstractFeedbackUI) -> typing.List[str]:
    """Plugin call.  Most likely, this will be implemented by legal entities.
    The fqdn, container_i and asset_id are provided so that a legal entity
    can determine the appropriate houdini $SITE path for the given context.
    """
    entrypoints = pkg_resources.iter_entry_points("fiepipe.houdini.houdini_site_paths")
    ret = []
    for entrypoint in entrypoints:
        method = entrypoint.load()
        ret.extend(await method(fqdn, container_id, root_id, asset_id, feedback_ui))
    return ret
