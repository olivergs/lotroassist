# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist Combat stats plugin
###############################################################################

# Python Imports
import re

# GTK Imports
import gtk

# EVOGTK imports
from evogtk.gui import GUIClass
from evogtk.factories import TreeViewFactory

# Plugin class
class Plugin(GUIClass):
    """
    LOTROAssist Combat stats plugin class
    """
    metadata={
        'PLUGIN_NAME': 'Combat stats',
        'PLUGIN_CODENAME': 'combatstats',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for combat stats',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'main',
    }
        
    def initialize(self):
        """
        Initialization function
        """
        self.damagedeal=TreeViewFactory('list',
                                   ['str','int','int','int','int'],
                                   ['Attack Skill','Hits','Average','Max','Total'],
                                   treeview=self.widgets.tvDamageDeal)
        self.dealregexp=re.compile(r'You wound the (?P<mob>.*) (with (?P<attack>.*))* for (?P<damage>\d*) points of (?P<type>.*)\.$')
        # You wound the Snarling Overseer with Retaliation for 370 points of Common damage.
        # You wound the Snarling Overseer for 305 points of Common damage.

    def clearStats(self,widget):
        """
        Clear combat stats
        """
        pass

    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        return self.damageDeal(line)
    
    def damageDeal(self,line):
        """
        Check if line is a damage dealing line
        """
        # Analyze log line
        resp=self.dealregexp.search(line)
        if resp:
            # Get line information
            # 'Attack','Used','Max damage','Total damage'
            mob=resp.group('mob')
            attack=resp.group('attack')
            damage=int(resp.group('damage'))
            type=resp.group('type')
            if not attack:
                attack='Unknown Attack'
            # Check if we have set this attack
            row=self.damagedeal.getRow(attack,0)
            if row:
                self.damagedeal.update(attack,[attack,row[1]+1,(row[2]+damage)/2,row[3]>damage and row[3] or damage,row[4]+damage],0)
            else:
                # Add the new quest to tree view
                self.damagedeal.append([attack,1,damage,damage,damage])
            return True