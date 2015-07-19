# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist Money count plugin
###############################################################################

# Python Imports
import re

# GTK Imports
import gtk

# EVOGTK imports
from evogtk.gui import GUIClass

# Plugin class
class Plugin(GUIClass):
    """
    LOTROAssist money count plugin class
    """
    metadata={
        'PLUGIN_NAME': 'Money Count',
        'PLUGIN_CODENAME': 'lootbag',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for money counting',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_DOCK': 'status',
    }
        
    def initialize(self):
        """
        Initialization function
        """
        self.regexp=re.compile(r'You( sold \d+ items for | looted | received |\'ve earned |r share was )((?P<gold>\d+) gold coin(s)*( and )*)*((?P<silver>\d+) silver piece(s)*( and )*)*((?P<copper>\d+) copper coin(s)*)*( for quest completion| in the mail)*\.$')
        # TODO: lotroassist: purchasing
        # You purchased 43 Travelling Rations for 68 silver pieces and 80 copper coins.
    def clearMoney(self,widget):
        """
        Clear money
        """
        self.ui.lblCopperCoins=0
        self.ui.lblSilverCoins=0
        self.ui.lblGoldCoins=0

    def newLine(self,line):
        """
        New line analysing function
        """
        # Analyze log line
        resp=self.regexp.search(line)
        if resp:
            # Set values
            carry=0
            copper=resp.group('copper')
            silver=resp.group('silver')
            gold=resp.group('gold')
            if not copper:
                copper=0
            if not silver:
                silver=0
            if not gold:
                gold=0            
            # Calculate copper coins
            val=int(self.ui.lblCopperCoins)+int(copper)
            if val >= 100:
                carry=1
                val=val%100
            self.ui.lblCopperCoins=val
            # Calculate silver coins
            silver=int(silver)+carry
            carry=0
            val=int(self.ui.lblSilverCoins)+silver
            if val >= 1000:
                carry=1
                val=val%1000
            self.ui.lblSilverCoins=val
            # Calculate gold coins
            gold=int(gold)+carry
            self.ui.lblGoldCoins=int(self.ui.lblGoldCoins)+gold
            return True