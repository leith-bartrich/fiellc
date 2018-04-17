#!/usr/local/bin/python
import fiepipe
import fiellclib.registration
import fiepipelib.shells.fiepipe
import fiepipelib.shells.legalentity
import fiepipelib.shells.gitasset
import fiepipelib.localplatform
import fiepipelib.localuser
import pkg_resources
import cmd2
import functools
import fiepipefreecad.commands.system
import fiepipefreecad.commands.asset
import types
import fiepipefreecad.templates.util


def FreeCADFIEPipeShellPlugin(shell:fiepipelib.shells.fiepipe.Shell):
    shell.AddSubmenu(fiepipefreecad.commands.system.FreeCADSystemCommand(
        shell._localUser), "freecad", [])
    #shell.AddCommand("freecad_install_add",\\
                     #fiepipefreecad.commands.system.AddFreeCAD,\
                     #functools.partial(cmd2.path_complete))
    #shell.AddCommand("freecad_install_delete",\
                     #fiepipefreecad.commands.system.DeleteFreeCAD,\
                     #fiepipefreecad.commands.system.freecad_installs_complete)
    

def FreeCADLocalSiteShellPlugin(shell:fiepipelib.shells.legalentity.Shell):
    pass
    
def FreeCADGitAssetShellPlugin(shell:fiepipelib.shells.gitasset.Shell):
    shell.AddSubmenu(fiepipefreecad.commands.asset.PartDesignsCommand(shell), 'freecad_partdesigns', ['fc_pd'])

def FreeCADPartDesignVersionsCommandPlugin(command:fiepipefreecad.commands.asset.PartDesignVersionsCommand):
    templates = fiepipefreecad.templates.util.GetPackageTemplatesDict()
    for k in templates.keys():
        command.AddTemplate(k, templates[k])


def main():

    version = pkg_resources.require("fiellc")[0].version
    print("FIE LLC (fiellc) " + str(version))
    pipeversion = pkg_resources.require("fiepipe")[0].version
    print("fiepipe " + str(pipeversion))

    #register if need be
    if not fiellclib.registration.IsRegistered():
        print("Registering FIE LLC")
        fiellclib.registration.Register()

    #make sure standard volumes are set
    fiellclib.registration.SetupStandardVolumes()

    #start the shell
    platform = fiepipelib.localplatform.GetLocalPlatform()
    user = fiepipelib.localuser.localuser(platform)
    shell = fiepipelib.shells.legalentity.Shell("fie.us",user)
    shell.onecmd("lssh")
    shell.cmdloop()

if __name__ == "__main__":
    main()
