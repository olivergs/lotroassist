# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist screenshot viewer plugin
###############################################################################

# Python Imports
import os
import re

# EVOGTK Imports
from evogtk.gui import GUIClass
from evogtk.tools import openWithDefaultApp
from evogtk.factories import DialogFactory 
from evogtk.factories import IconViewFactory


class Plugin(GUIClass):
    """
    LOTROAssist screenshot viewer plugin class
    """
    
    metadata={
        'PLUGIN_NAME': 'Screenshots',
        'PLUGIN_CODENAME': 'screenshotviewer',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for screenshot viewing and management',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'main',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        self.dialogs=DialogFactory()
        self.iconview=IconViewFactory(self.widgets.ivScreenshots)
        self.regexp=re.compile(r'Screenshot \[(?P<screenshot>ScreenShot\d{5}\.jpg)\] saved to disk\.$')
        self.filematch=re.compile(r'ScreenShot\d{5}\.jpg$')
        self.refreshScreenshots()
    
    def refreshScreenshots(self):
        """
        Refresh the screenshots viewer
        """
        # Load all files in directory
        dirlist=os.listdir(self.maingui.preferences.general.datadir)
        dirlist.sort()
        for filename in dirlist:
            resp=self.filematch.match(filename)
            if resp:
                if not self.iconview.update('%s/%s' % (self.maingui.preferences.general.datadir,filename),filename,160,120):
                    self.iconview.append('%s/%s' % (self.maingui.preferences.general.datadir,filename),filename,160,120)                
    
    def viewScreenshot(self,widget=None,path=None):
        """
        Show selected screenshot in the image viewer
        """
        selected=self.iconview.selected()
        if selected:
            selected=selected[0]
            # Open Screenshot with default system app
            openWithDefaultApp('%s/%s' % (self.maingui.preferences.general.datadir,selected))
    
    def reloadScreenshots(self,widget=None):
        """
        Reload all screenshots in log directory
        """
        self.iconview.clear()
        self.refreshScreenshots()
    
    def deleteScreenshot(self,widget=None):
        """
        Delete currently selected screenshot
        """
        selected=self.iconview.selected()        
        for icon in selected:
            if self.dialogs.msgDialog('Do you want to delete %s screenshot file?' % icon, 'question'):
                os.remove('%s/%s' % (self.maingui.preferences.general.datadir,icon))
                self.iconview.remove(icon)
    
    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        resp=self.regexp.search(line)
        if resp:
            # Get line information
            screenshot=resp.group('screenshot')
            self.maingui.showNotification('Screenshot taken: %s' % (screenshot),icon='plugins/screenshotviewer/pixmaps/taken.png')
            self.refreshScreenshots()
            return True