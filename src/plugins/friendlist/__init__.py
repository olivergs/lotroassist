# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist friend list plugin
###############################################################################

# Python Imports
import re

# EVOGTK Imports
from evogtk.gui import GUIClass
from evogtk.factories import TreeViewFactory

class Plugin(GUIClass):
    """
    LOTROAssist friend list plugin class
    """
    
    metadata={
        'PLUGIN_NAME': 'Friends',
        'PLUGIN_CODENAME': 'friendlist',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for friend list tracking',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'lists',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        self.friendlist=TreeViewFactory('list',
                                   ['str','bool'],
                                   ['Name','Status'],
                                   treeview=self.widgets.tvFriendList)
        self.regexpstatus=re.compile(r'Your friend, (?P<player>.*), has (come|gone) (?P<status>.*)\.$')
        self.regexpmanage=re.compile(r'(?P<player>.*) has been (?P<action>(added to|removed from)) your friends list\.$')
    
    def newLine(self,line):
        """
        New line analysing function
        """
        return (self.friendStatus(line) or self.friendManage(line))
    
    def friendManage(self,line):
        """
        Friend management check
        """
        # Analyze log line
        resp=self.regexpmanage.search(line)
        if resp:
            player=resp.group('player')
            action=resp.group('action')
            # Send management notification
            self.maingui.showNotification('%s have been %s Friends' % (player,action),icon='plugins/friendlist/pixmaps/friendmanage.png')
            return True
    
    def friendStatus(self,line):
        """
        Friend status check
        """
        # Analyze log line
        resp=self.regexpstatus.search(line)
        if resp:
            status=resp.group('status')
            player=resp.group('player')
            # Modify player if already added
            if not self.friendlist.update(player,[player,status=='online'],0):
                # Add the new player to tree view
                self.friendlist.append([player,status=='online'])
            # Send friend notification
            self.maingui.showNotification('%s is %s' % (player,status),icon='plugins/friendlist/pixmaps/%s.png' % status)
            return True