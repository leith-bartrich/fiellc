#!/usr/local/bin/python
import fiepipe
import fiellclib.registration
import fiepipelib.shells.fiepipe
import fiepipelib.shells.legalentity
import fiepipelib.localplatform
import fiepipelib.localuser
import pkg_resources

def plugintest(self, args):
    """Test plugin command.
    """
    print("Test!")

def fiepipeShellPlugin(shell):
    assert isinstance(shell, fiepipelib.shells.fiepipe.Shell)
    shell.__class__.do_plugintest = plugintest
    shell.__class__.complete_plugintest = shell.__class__.path_complete


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
    shell.cmdloop()

if __name__ == "__main__":
    main()
