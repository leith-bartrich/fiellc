#!/usr/local/bin/python
# general and fiepipe
import sys
import typing
import pkg_resources

# fiellc
import fiellclib.registration
# 3dcoat
import fiepipe3dcoat.shell.manager
# import fiepipe3dcoat.shell.representations
# import fiepipe3dcoat.shell.workfile
import fiepipe3dcoat.templates.util
# import fiepipefreecad.commands.asset
# freecad
import fiepipefreecad.commands.manager
import fiepipefreecad.templates.util
import fiepipehoudini.shell.assetaspect
import fiepipehoudini.shell.installs
import fiepipedesktoplib.gitstorage.shells.gitasset
import fiepipedesktoplib.legalentity.registry.shell.legal_entity
import fiepipelib.localplatform.routines.localplatform
import fiepipelib.localuser.routines.localuser
import fiepipedesktoplib.shells.fiepipe
import fiepipeunreal4.shell.assetaspect
# unreal4
import fiepipeunreal4.shell.installs
from fiellclib.mr_project.shell.root_structure import MRProjectConfigShell
from fiepipedesktoplib.gitstorage.shells.gitroot import Shell as GitRootShell
from fiepipeloosefiles.shell.assetaspect import LooseFilesAspectConfigCommand
from fiepiperpgmakermv.shell.aspectconfig import RPGMakerMVAspectConfigurationCommand
from fiepiperpgmakermv.shell.installs import RPGMakerMVInstallsCommand


# The plugins we use are set up here.
# And the main loop of the entity's custom command is defined here.

# Typically, python registers the plugin entry points system wide (globally).  Therefore the plugin entry points will
# be run no matter if this script is the one running fiepipe, or if the main fiepipe command is used, or
# if another entitiy's custom command is run.

# In some cases, you are comfortable running your plugins always (globally).
# In some cases, you should be checking which entity the request is for, before running plugin logic (limited by entity).
# In some cases, you might use other criteria to determine if your plugin logic should run. (limited by X)

# For example: the 'freecad' and '3dcoat' commands that link into the fiepipe Shell always run (globally), because they're
# about applications that are installed to the system.  They don't care which entity they're for.

# However, it's a judgement call as to if they should be adding their commands to assets for all entities, or just this (fiellc) one.
# It's probably a matter of a questioning whether a plugin is 'well known' or not as to if it should push itself globally on
# this system or not.

# when in doubt, assume an entity will opt-in to a plugin explicitly in its own plugin code.

# plugins for fiepipe shell
def FIEPipeShellPlugin(shell: fiepipedesktoplib.shells.fiepipe.Shell):
    # freecad command
    shell.add_submenu(fiepipefreecad.commands.manager.FreeCADSystemCommand(), "freecad", [])
    # 3dcoat command
    shell.add_submenu(fiepipe3dcoat.shell.manager.CoatSystemCommand(), "3dcoat", [])
    # unreal4 command
    shell.add_submenu(fiepipeunreal4.shell.installs.Unreal4InstallsCommand(), "unreal4", [])
    # houdini command
    shell.add_submenu(fiepipehoudini.shell.installs.HoudiniInstallsCommand(), "houdini", [])
    # rpgmakermv command
    shell.add_submenu(RPGMakerMVInstallsCommand(), "rpg_maker_mv", [])


# plugins for asset shell
def GitAssetShellPlugin(shell: fiepipedesktoplib.gitstorage.shells.gitasset.Shell):
    # freecad pard designs command
    # shell.AddSubmenu(fiepipefreecad.commands.asset.PartDesignsCommand(shell), 'freecad_partdesigns', ['fc_pd'])
    # 3DCoat work files command
    # shell.AddSubmenu(fiepipe3dcoat.shell.workfile.WorkFilesCommand(shell), "3dcoat_workfiles", ['coat_wf'])
    # unreal aspect command
    shell.add_submenu(fiepipeunreal4.shell.assetaspect.Unreal4AssetAspectCommand(shell), "unreal4", [])
    shell.add_submenu(fiepipehoudini.shell.assetaspect.HoudiniAssetAspectCommand(shell), "houdini", [])
    shell.add_submenu(LooseFilesAspectConfigCommand(shell), "loose_files", [])
    shell.add_submenu(RPGMakerMVAspectConfigurationCommand(shell), "rpg_maker_mv", [])


def GitRootShellPlugin(shell: GitRootShell):
    shell.add_submenu(MRProjectConfigShell(shell), "mr_project", [])


# plugins for all representations commands
# def AllSingleFileRepresentationsCommand(command: AbstractSingleFileRepresentationsCommand):
#     if shell._entity.get_fqdn == "fie.us":
#         # 3DCoat command
#         command.add_submenu(fiepipe3dcoat.shell.representations.CoatRepresentationsCommand(command), "3dcoat", [])


# plugins for freecad part design versions command
# def FreeCADPartDesignVerionsCommand(command: fiepipefreecad.commands.asset.PartDesignVersionsCommand):
#     if shell._entity.get_fqdn == "fie.us":
#         # templates for freecad pard designs
#         templates = fiepipefreecad.templates.util.GetPackageTemplatesDict()
#         for k in templates.keys():
#             command.AddTemplate(k, templates[k])


# plugins for 3DCoat work file verions command
# def CoatWorkfileVersionsCommand(command: fiepipe3dcoat.shell.workfile.WorkFileVerionsCommand):
#     if shell._entity.get_fqdn == "fie.us":
#         # templates for 3DCoat work files
#         templates = fiepipe3dcoat.templates.util.GetPackageTemplatesDict()
#         for k in templates.keys():
#             command.AddTemplate(k, templates[k])


# plugins for file templates
def FileTemplates(templateType: str, fqdn: str, templates: typing.Dict[str, str]):
    if shell._entity.get_fqdn == "fie.us":
        # templates for 3dcoat work files
        if templateType == "3b":
            templates.update(fiepipe3dcoat.templates.util.GetPackageTemplatesDict())
        if templateType == "fcstd":
            templates.update(fiepipefreecad.templates.util.GetPackageTemplatesDict())


# commmand main loop
def main():
    if "--testing" in sys.argv:
        testing = True
    else:
        testing = False

    # print start info
    name = "fiellc"
    if testing:
        name = "fiellc testing"

    fqdn = "fie.us"
    if testing:
        fqdn = "testing.fie.us"

    version = pkg_resources.require("fiellc")[0].version
    print("FIE LLC (" + name + ") " + str(version))
    pipeversion = pkg_resources.require("fiepipe")[0].version
    print("fiepipe " + str(pipeversion))

    # register entity if need be
    # note: in this mode, we're distributing the registration by pip becaues the registration is embedded in the python package.
    # that means we can update the registration with new authority, etc. by releasing a new version of the package and requiring
    # that users keep up to date via pip/pypi/github/git.
    if not fiellclib.registration.is_registered(fqdn=fqdn):
        print("Registering FIE LLC")
        fiellclib.registration.register(fqdn=fqdn)

    # make sure entity standard volumes are set
    # note: Since the storage volumes are global to the system, this step is potentially contentious.
    # we at FIE LLC are ensuring cerrtain standards for our systems.  But we could be stepping on others
    # here.  We make the decision that this pacakge will only ever run on OUR systems.  In which
    # case we're fine making this call.

    # In truth though, the implementaiton only sets up a "docs" volume in an extremely common way.  So we're
    # not stepping on toes with this one.
    fiellclib.registration.setup_standard_volumes()

    # start the shell.
    # note:  We're just jumping straight into the local site here.  But we don't have to.
    # while we could process other parameters here and jump deeper into the system, we'd
    # rather have nice tab-completion help with that within the fiepipe system.
    platform = fiepipelib.localplatform.routines.localplatform.get_local_platform_routines()
    user = fiepipelib.localuser.routines.localuser.LocalUserRoutines(platform)
    shell = fiepipedesktoplib.legalentity.registry.shell.legal_entity.LegalEntityShell(fqdn, user)
    # run until exited.
    shell.cmdloop()
    # exited.
    print("Exiting " + fqdn + " fiepipe system.")
    exit()


# run main loop if this script is run
if __name__ == "__main__":
    main()
