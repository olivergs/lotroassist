# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist experience plugin
###############################################################################

# Python Imports
import re

# GTK Imports
import gobject
import gtk

# EVOGTK Imports
from evogtk.gui import GUIClass

class Plugin(GUIClass):
    """
    LOTROAssist experience plugin class
    """
    
    metadata={
        'PLUGIN_NAME': 'XP Counter',
        'PLUGIN_CODENAME': 'xpcount',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for XP counting',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'status',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        self.regexp=re.compile(r'You\'ve earned (?P<gain>\d+) XP for a total of (?P<total>\d*(,)*\d*) XP\.$')
        self.refellowlevup=re.compile(r'Your fellow, (?P<player>.*), is now level (?P<level>\d+)\.$')
        self.reselflevup=re.compile(r'Your level has changed to (?P<level>\d+)\.$')
    
    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        return (self.gotxp(line) or self.fellowlevup(line) or self.selflevup(line))
        
    def gotxp(self,line):
        resp=self.regexp.search(line)
        if resp:
            # Get line information
            # gain=resp.group('gain')
            total=resp.group('total')
            self.ui.lblTotalXP=total
            return True
    
    def fellowlevup(self,line):
        resp=self.refellowlevup.search(line)
        if resp:
            # Get line information
            player=resp.group('player')
            level=resp.group('level')
            # Show notification
            self.maingui.showNotification('%s is now level %s' % (player,level),icon='plugins/xpcount/pixmaps/levelup.png')
            return True
        
    def selflevup(self,line):
        resp=self.reselflevup.search(line)
        if resp:
            # Get line information
            level=resp.group('level')
            # Show notification
            self.maingui.showNotification('Reached level %s' % (level),icon='plugins/xpcount/pixmaps/levelup.png')
            return True

