import os
import os.path
import typing

import fiepipelib.fqdn
from fiepipelib.gitstorage.routines.gitasset import GitAssetRoutines
from fiepipelib.localplatform.routines.localplatform import get_local_platform_routines
from fiepipelib.localuser.routines.localuser import LocalUserRoutines
from fieui.FeedbackUI import AbstractFeedbackUI


def houdini_site_paths(fqdn: str, contaier_id: str, root_id: str,
                       asset_id: str, feedback_ui: AbstractFeedbackUI) -> typing.List[str]:
    # only work for fie.us or subdomains
    if not fiepipelib.fqdn.is_dommain_or_subdomain(fqdn, "fie.us"):
        return []

    # go!
    ret = []
    # TODO: pull from github here

    #at fie, we have a company wide hsite toolset in the user's Documents folder, for now.

    #an alternative, might be to have a checkout of such a toolset in each asset.  Which would keep
    #the toolset's checkout versioned.  Especially if it were an asset itself.
    #we could also switch to different toolsets based on asset configuration here too.

    plat = get_local_platform_routines()
    user = LocalUserRoutines(plat)

    company_tools = os.path.join(user.get_home_dir(), "Documents", fqdn, "houdini_tools")
    ret.append(company_tools)

    return ret


def houdini_job_paths(fqdn: str, contaier_id: str, root_id: str,
                      asset_id: str, feedback_ui: AbstractFeedbackUI) -> typing.List[str]:
    # only work for fie.us or subdomains
    if not fiepipelib.fqdn.is_dommain_or_subdomain(fqdn, "fie.us"):
        return []

    # go!
    ret = []

    #at fie we set the job to the asset's working directory.
    #though we could also pull from the asset configuration here too.

    plat = get_local_platform_routines()
    user = LocalUserRoutines(plat)

    asset_routines = GitAssetRoutines(contaier_id, root_id, asset_id, feedback_ui)
    asset_routines.load()

    asset_working_path = asset_routines.abs_path

    ret.append(asset_working_path)

    return ret
