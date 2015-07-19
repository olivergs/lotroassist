# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist world broadcast plugin
###############################################################################

# Python Imports
import re

# GTK Imports
import gtk

# EVOGTK Imports
from evogtk.gui import GUIClass

class Plugin(GUIClass):
    """
    LOTROAssist world broadcast plugin class
    """
    
    metadata={
        'PLUGIN_NAME': 'World Broadcasts',
        'PLUGIN_CODENAME': 'worldbroadcasts',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for world broadcasts notifications',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
    }

    def initialize(self):
        """
        Initialization function
        """
        # World broadcast Regular Expression
        self.regexp=re.compile(r'World broadcast: (?P<msg>.*)$')
    
    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        resp=self.regexp.search(line)
        if resp:
            # Set values
            msg=resp.group('msg')
            self.maingui.showNotification(msg,icon='plugins/worldbroadcasts/pixmaps/broadcast.png')
            return True