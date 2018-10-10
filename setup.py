import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "fiellc",
    version = "0.1.0.dev1",
    author= "Bradley Friedman",
    author_email = "brad@fie.us",
    description = ("A plugin and command for FIE LLC using fiepipe"),
    keywords = "pipeline,workflow,fiepipe",
    url = "http://www.fie.us",
    py_modules=["fiellc"],
    packages = ["fiellclib"],
    install_requires=["fiepipe"],
    entry_points={
        'fiepipe.plugin.shell.fiepipe.v1' : 'fiellc = fiellc:FIEPipeShellPlugin',
        #'fiepipe.plugin.shell.gitasset.v1' : 'fiellc = fiellc:GitAssetShellPlugin',
        #'fiepipe.plugin.shell.all_single_file_representations_command.v1' : 'fiellc = fiellc:AllSingleFileRepresentationsCommand',
        #'fiepipe.plugin.shell.freecad_part_design_versions_command.v1' : 'fiellc = fiellc:FreeCADPartDesignVerionsCommand',
        #'fiepipe.plugin.shell.coat_workfile_versions_command.v1' : 'fiellc = fiellc:CoatWorkfileVersionsCommand',
        'fiepipe.pluign.templates.file' : 'fiellc = fiellc:FileTemplates',
        'console_scripts': [
            'fiellc = fiellc:main',
        ],
        'fiepipe.plugin.gitstorage.lfs.patterns': [
            'coat3d = fiepipe3dcoat.routines.lfs_tracked_patterns:get_patterns',
            'freecad = fiepipefreecad.routines.lfs_tracked_patterns:get_patterns',
        ],

    },
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        ],
    include_package_data = True,
)

