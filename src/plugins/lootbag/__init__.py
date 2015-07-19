# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist loot bag plugin
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
    LOTROAssist loot bag plugin class
    """
    metadata={
        'PLUGIN_NAME': 'Loot Bag',
        'PLUGIN_CODENAME': 'lootbag',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for loot counting',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'lists',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        self.lootbag=TreeViewFactory('list',
                                   ['int','str'],
                                   ['Items','Item Name',],
                                   treeview=self.widgets.tvLootBag)
        self.itemregexp=re.compile(r'You have acquired .*\[(?P<items>\d*\s)*(?P<name>.*)\]\.$')
        self.itemremregexp=re.compile(r'Item Removed: \[(?P<items>\d*\s)*(?P<name>.*)\].$')
        # TODO: lotroassist: purchased and sold items
        
    
    def copyItems(self,widget):
        """
        Copy loot bag items to clipboard
        """
        clipboard=gtk.Clipboard()
        # Get stored data
        data=self.lootbag.getData()
        # Copy data to clipboard
        textdata=''
        for row in data:
            textdata+='%s x %s\n' % tuple(row)
        if textdata:
            clipboard.set_text('Loot Bag\n' + textdata)
    
    def removeItem(self,widget):
        """
        Remove selected item
        """
        self.lootbag.remove()
    
    def clearItems(self,widget):
        """
        Clears item list
        """
        self.lootbag.clear()
    
    def newLine(self,line):
        """
        New line analysing function
        """
        return (self.gotItem(line) or self.lostItem(line))
    
    def gotItem(self,line):
        """
        Check if line is a item line and process it
        """
        # Analyze log line
        resp=self.itemregexp.search(line)
        if resp:
            # Get line information
            items=resp.group('items')
            itemname=resp.group('name')
            if not items:
                items=1
            else:
                items=int(items)
            # Check if we have adquired the item before
            item=self.lootbag.getRow(itemname,1)
            if item:
                self.lootbag.update(itemname,[item[0]+items],1)
            else:
                # Add the new quest to tree view
                self.lootbag.append([items,itemname])
            return True
    
    def lostItem(self,line):
        """
        Check if line is a item removing line and process it
        """
        # Analyze log line
        resp=self.itemremregexp.search(line)
        if resp:
            # Get line information
            items=resp.group('items')
            itemname=resp.group('name')
            if not items:
                items=1
            else:
                items=int(items)
            # Check if we have adquired the item before
            item=self.lootbag.getRow(itemname,1)
            if item and item[0]>0:
                self.lootbag.update(itemname,[item[0]-items],1)
            return True
