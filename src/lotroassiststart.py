#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist start script
###############################################################################

from LOTROAssist import LOTROAssistClass
gui=LOTROAssistClass(guifiles=['lotroassist.ui'],mainapp=True,debug=True)
gui.run()