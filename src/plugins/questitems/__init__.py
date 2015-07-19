# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist quest items plugin
###############################################################################

# Python Imports
import re

# GTK Imports
import gtk

# EVOGTK Imports
from evogtk.gui import GUIClass
from evogtk.factories import TreeViewFactory

class Plugin(GUIClass):
    """
    LOTROAssist quest items plugin class
    """

    metadata={
        'PLUGIN_NAME': 'Quest Items',
        'PLUGIN_CODENAME': 'questitems',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for quest item count',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'main',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        self.questlist=TreeViewFactory('list',
                                   ['bool','str','int','int','progress'],
                                   ['Finished','Quest','Done','Pending','Progress'],
                                   treeview=self.widgets.tvQuestItems)
        self.regexp=re.compile(r'(?P<name>.*)\s\((?P<done>\d+)\/(?P<pending>\d+)\)$')
    
    def copyQuestItems(self,widget):
        """
        Copy quest items to clipboard
        """
        clipboard=gtk.Clipboard()
        # Get stored data
        data=self.questlist.getData()
        # Copy data to clipboard
        textdata=''
        for row in data:
            textdata+='%s (%s/%s)\n' % tuple(row[1:-1])
        if textdata:
            clipboard.set_text('Quest Items\n' + textdata)
    
    def removeQuestItem(self,widget):
        """
        Remove selected quest item
        """
        self.questlist.remove()
    
    def clearQuestItems(self,widget):
        """
        Clears quest item list
        """
        self.questlist.clear()
    
    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        resp=self.regexp.search(line)
        if resp:
            # Get line information
            questname=resp.group('name')
            questdone=int(resp.group('done'))
            questpending=int(resp.group('pending'))
            questfinished=(questdone==questpending)
            questprogress=questdone*100/questpending
            # If autoremove is active, remove quest
            if questfinished and self.widgets.tlbcAutoRemoveQuestItem.get_active():
                self.questlist.remove(questname,1)
            else:
                # Modify quest if already added
                if not self.questlist.update(questname,[questfinished,questname,questdone,questpending,questprogress],1):
                    # Add the new quest to tree view
                    self.questlist.append([questfinished,questname,questdone,questpending,questprogress])
            return True