# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import sys
import os
import atexit
if sys.hexversion < 0x2070000:
    raise ImportError('Python >= 2.7 is required')

#pylint: disable=wrong-import-position
from waflib import Context
from zm import ZENMAKE_DIR, WAF_DIR
from zm.constants import WSCRIPT_NAME
Context.WSCRIPT_FILE = WSCRIPT_NAME

joinpath = os.path.join

def atExit():
    """
    Callback function for atexit
    """

    # remove 'wscript' file if it exists
    from zm import shared
    if not shared.buildConfHandler:
        return
    wscriptfile = shared.buildConfHandler.confPaths.wscriptfile
    if os.path.isfile(wscriptfile):
        os.remove(wscriptfile)

atexit.register(atExit)

def prepareDirs(bconfPaths):
    """
    Prepare some paths for correct work
    """
    from zm import utils

    buildroot     = bconfPaths.buildroot
    realbuildroot = bconfPaths.realbuildroot
    if not os.path.exists(realbuildroot):
        os.makedirs(realbuildroot)
    if buildroot != realbuildroot and not os.path.exists(buildroot):
        utils.mksymlink(realbuildroot, buildroot)

    from zm import assist
    assist.writeWScriptFile(bconfPaths.wscriptfile)

def handleCLI(buildConfHandler, args, buildOnEmpty):
    """
    Handle CLI and return command object and waf cmd line
    """
    from zm import cli

    defaults = {
        '*' : dict( buildtype = buildConfHandler.defaultBuildType )
    }

    cmd, wafCmdLine = cli.parseAll(args, defaults, buildOnEmpty)
    cli.selected = cmd
    return cmd, wafCmdLine

def isDevVersion():
    """
    Detect that this is development version
    """
    gitDir = joinpath(ZENMAKE_DIR, os.path.pardir, '.git')
    #TODO: check that it is 'master' branch
    return os.path.exists(gitDir)

def run():
    """
    Prepare and run ZenMake and Waf with ZenMake stuffs
    """

    # When set to a non-empty value, the process will not search for a build
    # configuration in upper folders.
    os.environ['NOCLIMB'] = '1'

    # use of Options.lockfile is not enough
    os.environ['WAFLOCK'] = '.lock-wafbuild'
    from waflib import Options
    Options.lockfile = '.lock-wafbuild'

    # process buildconf and CLI
    from zm import log, assist, shared
    from zm.buildconf import loader as bconfLoader
    from zm.buildconf.handler import BuildConfHandler

    buildconf = bconfLoader.load(check = False, dirpath = os.getcwd())
    if assist.isBuildConfChanged(buildconf) or isDevVersion():
        bconfLoader.validate(buildconf)
    bconfHandler = BuildConfHandler(buildconf)
    shared.buildConfHandler = bconfHandler
    bconfPaths = bconfHandler.confPaths
    isBuildConfFake = assist.isBuildConfFake(buildconf)

    cmd, wafCmdLine = handleCLI(bconfHandler, sys.argv, not isBuildConfFake)

    if isBuildConfFake:
        log.error('Config buildconf.py not found. Check buildconf.py '
                  'exists in the project directory.')
        return 1

    # Special case for 'distclean'
    if cmd.name == 'distclean':
        assist.distclean(bconfPaths)
        return 0

    if cmd.args.distclean:
        assist.distclean(bconfPaths)

    prepareDirs(bconfPaths)

    # Load waf add-ons to support of custom waf features
    import zm.waf
    zm.waf.loadAllAddOns()

    # start waf ecosystem
    from waflib import Scripting
    del sys.argv[1:]
    sys.argv.extend(wafCmdLine)
    from zm.waf import wrappers
    wrappers.setupAll(cmd, bconfHandler)

    cwd = bconfPaths.wscriptdir
    Scripting.waf_entry_point(cwd, Context.WAFVERSION, WAF_DIR)

    return 0
