# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


import os
from Components.config import config
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup
from .__init__ import _
from .Version import PLUGIN
from .Debug import logger, log_levels, setLogLevel


class SetupScreen(Setup):

    def __init__(self, session):
        Setup.__init__(self, session, setup="piconcockpit", plugin="Extensions/PiconCockpit", PluginLanguageDomain=PLUGIN)
        self.setTitle(PLUGIN + " - " + _("Setup"))

    def keySelect(self):
        # the picon directory is chosen in the directory browser, not typed
        if self.getCurrentItem() is config.plugins.piconcockpit.picon_directory:
            self.selectPiconDirectory()
        else:
            Setup.keySelect(self)

    def selectPiconDirectory(self):
        current = config.plugins.piconcockpit.picon_directory.value
        self.session.openWithCallback(
            self.selectPiconDirectoryCallback,
            LocationBox,
            windowTitle=_("Picon directory"),
            text=_("Select the directory the picons are stored in."),
            currDir=current if current and os.path.isdir(current) else "/media",
            editDir=True,
        )

    def selectPiconDirectoryCallback(self, path):
        logger.debug("path: %s", path)
        if path:
            config.plugins.piconcockpit.picon_directory.value = os.path.normpath(path)
            self["config"].invalidateCurrent()

    def _applyLogLevel(self):
        setLogLevel(log_levels[config.plugins.piconcockpit.debug_log_level.value])

    def keySave(self):
        path = os.path.normpath(config.plugins.piconcockpit.picon_directory.value)
        if not os.path.exists(path):
            logger.error("Path does not exist: %s", path)
            self.session.open(MessageBox, _("Path does not exist") + ": " + path, MessageBox.TYPE_ERROR)
            return
        self._applyLogLevel()
        Setup.keySave(self)
