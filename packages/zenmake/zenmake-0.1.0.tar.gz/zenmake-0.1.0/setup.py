import os
import sys
import shutil
import fnmatch
import subprocess
from distutils.errors import DistutilsOptionError
from setuptools import setup, find_packages
from setuptools import Command
from setuptools.command.egg_info import egg_info
#from wheel.bdist_wheel import bdist_wheel
from zenmake.zm.version import VERSION

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

DEST_DIR = 'dist'
DIST_DIR = os.path.join(DEST_DIR, 'dist')
PYPI_USER = 'pustotnik'

PRJ_NAME = 'zenmake'
AUTHOR = 'Alexander Magola'
AUTHOR_EMAIL = 'pustotnik@gmail.com'

REPO_URL   = 'https://gitlab.com/pustotnik/zenmake'
SRC_URL    = REPO_URL
ISSUES_URL = 'https://gitlab.com/pustotnik/zenmake/issues'

DESCRIPTION = 'ZenMake - build system based on WAF'
#with open(os.path.join(here, "README.md"), "r") as fh:
#    LONG_DESCRIPTION = fh.read()
LONG_DESCRIPTION = """\
ZenMake - build system for C/C++ projects based on WAF.
It's designed to be as simple as possible to use but be flexible.
"""

CLASSIFIERS = """\
Development Status :: 4 - Beta
License :: OSI Approved :: BSD License
Environment :: Console
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
Operating System :: POSIX :: Linux
Operating System :: MacOS
Operating System :: Microsoft :: Windows
Topic :: Software Development :: Build Tools
""".splitlines()

PYTHON_REQUIRES = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4'
RUNTIME_DEPS = ['PyYAML']
#PKG_DIRS = ['auxiliary', 'waf', 'zm']
PKG_DIRS = ['zenmake']

CMD_OPTS = dict(
    # options for commands

    # setuptools/distuils like to litter in several dirs, not one
    egg_info = dict( egg_base = DEST_DIR ),
    sdist = dict( dist_dir = DIST_DIR),
    bdist = dict( dist_dir = DIST_DIR),
    build = dict( build_base = os.path.join(DEST_DIR, 'build')),
    # for python 2 and 3
    bdist_wheel = dict( universal = 1),
)

class EggInfoCmd(egg_info):

    def finalize_options(self):
        # 'egg_info' doesn't make dir for self.egg_base
        if self.egg_base and not os.path.isdir(self.egg_base):
            os.makedirs(self.egg_base)
        egg_info.finalize_options(self)

class CleanCmd(Command):

    description = "clean up files from 'setuptools' commands and some extras"

    PATTERNS = '*.pyc *.pyo *.egg-info __pycache__ .pytest_cache .coverage'.split()
    TOP_DIRS = 'build dist'.split() + [DEST_DIR]

    # Support the "all" option. Setuptools expects it in some situations.
    user_options = [
        ('all', 'a', "provided for compatibility"),
    ]

    boolean_options = ['all']

    def initialize_options(self):
        self.all = None

    def finalize_options(self):
        pass

    def run(self):
        remove = []
        for root, dirs, files in os.walk(here):
            for pattern in self.PATTERNS:
                for name in fnmatch.filter(dirs, pattern):
                    remove.append(os.path.join(root, name))
                    dirs.remove(name) # don't visit sub directories
                for name in fnmatch.filter(files, pattern):
                    remove.append(os.path.join(root, name))

        for path in self.TOP_DIRS:
            remove.append(os.path.join(here, path))

        for path in remove:
            if os.path.isdir(path):
                shutil.rmtree(path, ignore_errors = True)
            elif os.path.isfile(path):
                os.remove(path)

class PublishCmd(Command):

    description = "upload to pypi using 'twine'"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        try:
            import twine
        except ImportError:
            raise DistutilsOptionError("Module 'twine' not found. You need to install it.")

    def run(self):
        cmd = "%s -m twine upload -u %s %s/*" % (sys.executable, PYPI_USER, DIST_DIR)
        subprocess.call(cmd, shell = True)

cmdclass = {
    'egg_info' : EggInfoCmd,
    'clean': CleanCmd,
    'publish' : PublishCmd,
}

kwargs = dict(
    name = PRJ_NAME,
    version = VERSION,
    license = 'BSD',
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = REPO_URL,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    zip_safe = False, # waf cannot run from .zip without unpacking
    packages = PKG_DIRS,
    include_package_data = True,    # include everything in source control
    #exclude_package_data = {'': ['README.txt']},
    #package_dir = {'': 'src'},
    classifiers = CLASSIFIERS,
    python_requires = PYTHON_REQUIRES,
    install_requires = RUNTIME_DEPS,
    project_urls = {
        'Bug Tracker' : ISSUES_URL,
        'Source Code' : SRC_URL,
        #'Documentation' : ?,
    },
    entry_points = {
        'console_scripts': [
            'zenmake = zenmake.zmrun:main',
        ],
    },
    #py_modules = ['__main__'],
    options = CMD_OPTS,
    cmdclass = cmdclass,
)

DEFAULT_SETUP_CMDS = 'clean sdist bdist_wheel'

def main():

    if len(sys.argv) == 1:
        sys.argv.extend(DEFAULT_SETUP_CMDS.split())

    setup(**kwargs)

if __name__ == '__main__':
    main()