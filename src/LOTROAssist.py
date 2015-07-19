#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# Main LOTROAssist module
###############################################################################

from evogtk.gui import GUIClass

# Python Imports
import os
import time

# GTK Imports
import glib
import gobject
import gtk

# EVOGTK Import
import evogtk
from evogtk import tools
from evogtk.factories.dialogs import DialogFactory
# from evogtk.gui import threadtasks
from evogtk.gui.plugins import PluginLoader
from evogtk.widgets import TrayIcon,FloatingWindow

class LOTROAssistClass(GUIClass):
    """
    LOTROAssist main class
    """
    # Application metadata
    metadata={
        'APP_NAME': 'LOTROAssist',
        'APP_CODENAME': 'lotroassist',
        'APP_VERSION': '0.1',
        'APP_DESC': 'Lord Of The Rings Online Assistant Application',
        'APP_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'APP_WEBSITE': 'http://www.evosistemas.com',
        'APP_PREFERENCES': {
            'general': {
                'closetotray': ('bool',['chkCloseToTray'],True),
                'alwaysshowtrayicon': ('bool',['chkAlwaysShowTrayIcon'],True),
                'shownotifications': ('bool',['chkShowNotifications'],True),
                'datadir': ('str',['fcbDataDir'],'./'),
                'monitorlogs': ('bool',['tactMonitorLogs'],False),
                'showinfobar': ('bool',['tactShowInfoBar'],False),           
                'showconsole': ('bool',['tactShowConsole'],False),
                'infobarposx': ('int',[],0),
                'infobarposy': ('int',[],0),
            },
            'log': {
                'forcesimplelog': ('bool',['chkForceSimpleLog'],False),
                'delay': ('int',['spnLogDelay'],20),
                'normalcolor': ('str',['cbNormalColor'],'#000000'),
                'internalcolor': ('str',['cbInternalColor'],'#00FF00'),
                'logopencolor': ('str',['cbLogOpenColor'],'#0000FF'),
                'plugincolor': ('str',['cbPluginColor'],'#FF0000'),
            },
        }
    }

    def initialize(self):
        """
        GUI initialization method
        """
        self.currentlog={
            'filename': None,
            'age': 0,
            'manual': False,
        }
        # Create info bar
        self.setupInfoBar()
        # Tray icon setup
        self.trayicon=TrayIcon('pixmaps/lotroassist.png',self.metadata['APP_NAME'],menu=self.widgets.mnuTrayIcon,action=self.trayIconActivate)
        # Load Application preferences
        self.preferences.load()
        # Move info window
        self.widgets.winInfoBar.move(self.preferences.general.infobarposx,self.preferences.general.infobarposy)
        # Log window setup
        self.setupLogWindow()
        self.setupTextStyles()
        self.widgets.scrConsole.add(self.widgets.txtLog)
        # Show log message for app initialization
        self.logMessage('Initialising LOTROAssist','internal')
        # Set preferences
        self.logMessage('Loading preferences','internal')
        self.setPreferences()
        # Dialog module initialization
        self.dialogs=DialogFactory(self.widgets.winMain)
        # Load Application plugins
        self.logMessage('Initialising Plugin system','internal')
        self.plugins=PluginLoader()
        self.loadPlugins()
        # Add main loop callback
        gobject.timeout_add(self.preferences.log.delay,self.mainLoop,priority=gobject.PRIORITY_LOW)
        # Test
        def validatetext(val):
            if val != 'HOLA':
                return "<b>Error</b> de texto"
            return None
        def validateint(val):
            if int(val) != 10:
                return "<b>Error</b> de entero"
            return None
        def validatebool(val):
            if not bool(val):
                return "<b>Error</b> de booleano"
            return None
        def validatefloat(val):
            if float(val) != 10.10:
                return "<b>Error</b> de float"
            return None
        def validatedate(val):
            from datetime import datetime
            if datetime(2010,10,21)>val:
                return "<b>Error</b> de fecha"
            return None
        self.widgets.dbentTest.add_validators(validatetext,validatebool)
        self.widgets.dbcmbTest.add_validators(validatetext,validatebool)
        self.widgets.dbspnTest.add_validators(validateint,validatefloat)
        self.widgets.dbchkTest.add_validators(validatebool)
        self.widgets.dbreentTest.add_validators(validatetext)
        self.widgets.dbdtpTest.add_validators(validatedate)
        self.widgets.dbcalTest.add_validators(validatedate)

        print 'Entry',self.ui.dbentTest
        print 'ComboBox',self.ui.dbcmbTest
        print 'SpinButton',self.ui.dbspnTest
        print 'CheckButton',self.ui.dbchkTest
        print 'RegExpEntry',self.ui.dbreentTest
        print 'DatePicker',self.ui.dbdtpTest
        print 'Calendar',self.ui.dbcalTest
        
    def setupInfoBar(self):
        """
        Setups the information bar
        """
        infobar=FloatingWindow(title='LOTROAssist info bar',color='#999',rounded=True,alwaysontop=True,dragable=True,maximize=evogtk.MAXIMIZE_HORIZONTAL)
        hbxinfobar=gtk.HBox(spacing=5)
        infobar.add(hbxinfobar)
        # Add info bar to widget access
        self.widgets.add_widget(infobar,'winInfoBar')
        self.widgets.add_widget(hbxinfobar,'hbxInfoBar')

    def setupLogWindow(self):
        """
        Setup the log window
        """
        # Check if we use GTK Sourceview for log widget
        if evogtk.EVOGTK_HAS_GTKSOURCEVIEW and not self.preferences.log.forcesimplelog:
            # Use GTK Sourceview
            import gtksourceview2
            buffer=gtksourceview2.Buffer()
            view=gtksourceview2.View(buffer)
            view.set_show_line_numbers(True)
            view.set_show_line_marks(True)
        else:
            # Use GTK TextView
            buffer=gtk.TextBuffer()
            view=gtk.TextView(buffer)
        # Show log view and set basic parameters
        self.widgets.add_widget(view,'txtLog')
        view.set_editable(False)
        view.set_cursor_visible(False)
        view.show()
    
    def setupTextStyles(self):
        """
        Setup text styles used by application
        """
        buffer=self.widgets.txtLog.get_buffer()
        tools.newTextTag({'name': 'normal','foreground': self.preferences.log.normalcolor},buffer)
        tools.newTextTag({'name': 'internal','foreground': self.preferences.log.internalcolor, 'weight': 700},buffer)
        tools.newTextTag({'name': 'logopen','foreground': self.preferences.log.logopencolor, 'weight': 700},buffer)
        tools.newTextTag({'name': 'plugin','foreground': self.preferences.log.plugincolor, 'weight': 700},buffer)
    
    def openLogFile(self,widget):
        """
        Manually select the logfile to load
        """
        # Open file selection dialog
        logfile=self.dialogs.fileSelDialog('open','Log File Selection',False,self.preferences.general.datadir)
        # Check if has selected a log file
        if logfile[0]:
            logfile=logfile[0][0]
            self.currentlog={
                'filename': logfile,
                'age': 0,
                'fd': open(logfile,'r'),
                'manual': True,
            }
            # Show desktop notification
            self.showNotification('Opening selected log: %s' % logfile,True)
            self.logMessage('Opened Log File: %s' % logfile,'logopen')
            self.ui.tlbtMonitorLogs=False
            # Do a burst read of log
            self.burstRead()

    
    def quitApplication(self,widget,event=None):
        """
        Application quit callback
        """
        if self.preferences.general.closetotray and widget == self.widgets.winMain:
            self.trayIconActivate()
        else:
            if self.dialogs.msgDialog('¿Do you want to exit LOTRO Assist?', 'question'):
                self.savePreferences()
                self.unloadPlugins()
                self.quit()
        return True
    
    def showPreferences(self,widget=None):
        """
        Show preferences dialog
        """
        self.widgets.winPreferences.show()
        
    def showAbout(self,widget=None):
        """
        Show about dialog
        """
        self.dialogs.aboutDialog(self.metadata)
    
    def trayIconActivate(self,widget=None):
        """
        Toggles main window visible status
        """
        if self.widgets.winMain.get_property('visible'):
            self.widgets.winMain.hide()
            self.trayicon.show()
        else:
            self.widgets.winMain.show()
            self.trayicon.set_visible(self.preferences.general.alwaysshowtrayicon)
    
    def savePreferences(self,widget=None,other=None):
        """
        Save application preferences
        """
        self.widgets.winPreferences.hide()
        self.preferences.general.infobarposx,self.preferences.general.infobarposy=self.widgets.winInfoBar.get_position()
        self.preferences.save()
        self.setPreferences()
        return True

    def setPreferences(self):
        """
        Set preferences
        """
        # Tray Icon preferences
        self.trayicon.set_visible(self.preferences.general.alwaysshowtrayicon)

    def mainLoop(self):
        """
        Starts main log process loop
        """
        # Check if a new log has been created
        if self.ui.tlbtMonitorLogs:
            self.checkLogFiles()
        if self.currentlog.has_key('fd'):
            # Check new lines in current log
            line=self.currentlog['fd'].readline().strip()    
            if line:
                # Call new line callback
                self.newLogLine(line)
        # Return true for loop repeat
        return True
    
    def toggleConsole(self,widget,event=None):
        """
        Toggle log monitoring
        """
        if widget==self.widgets.winConsole:
            self.preferences.general.showconsole=False
        else:
            self.preferences.general.showconsole=widget.get_active()
        if self.preferences.general.showconsole:
            self.widgets.winConsole.show()
        else:
            self.widgets.winConsole.hide()
        return True

    def toggleInfoBar(self,widget,event=None):
        """
        Toggle log monitoring
        """
        if widget==self.widgets.winInfoBar:
            self.preferences.general.showinfobar=False
        else:
            self.preferences.general.showinfobar=widget.get_active()
        if self.preferences.general.showinfobar:
            self.widgets.winInfoBar.show_all()
        else:
            self.widgets.winInfoBar.hide()
        return True

    def toggleMonitorLogs(self,widget):
        """
        Toggle log monitoring
        """ 
        self.preferences.general.monitorlogs=widget.get_active()
        self.currentlog['manual']=not self.preferences.general.monitorlogs
    
    def checkLogFiles(self):
        """
        Check if new log files has been created and replaces current by the new one
        """
        logage=self.currentlog['age']
        logfile=self.currentlog['filename']
        # Get last log filename
        files=os.listdir(self.preferences.general.datadir)
        for file in files:
            filename=file.split('.')
            if len(filename)==2 and filename[1]=='txt':
                fileage=os.stat('%s/%s' % (self.preferences.general.datadir,file))[8]
                if logage<=fileage:
                    logfile='%s/%s' % (self.preferences.general.datadir,file)
                    logage=fileage
        # Check if current log is the newest one
        if logfile != self.currentlog['filename']:
            # Close older log and open the new one
            if self.currentlog.has_key('fd'):
                self.currentlog['fd'].close()
            self.currentlog={
                'filename': logfile,
                'age': logage,
                'fd': open(logfile,'r'),
                'manual': False,
            }
            # Show desktop notification
            self.showNotification('Opened Log File: %s' % logfile,True)
            self.logMessage('Opened Log File: %s' % logfile,'logopen')
            # Do a burst read of log
            self.burstRead()

    def burstRead(self):
        """
        Burst read of a log file
        """
        notif=self.preferences.general.shownotifications
        self.preferences.general.shownotifications=False
        self.logMessage('Doing burst read of lofgile %s' % self.currentlog['filename'],'internal')
        lines=self.currentlog['fd'].readlines()
        for line in lines:
            tools.processPendingEvents()
            self.newLogLine(line.strip(),burst=True)
        self.preferences.general.shownotifications=notif
        self.logMessage('Burst read of lofgile %s finished for a total of %s lines' % (self.currentlog['filename'],len(lines)),'internal')

    
    def showNotification(self,msg,statusbar=False,icon=None):
        """
        Show notification
        """
        if statusbar:
            self.ui.stbMain=msg
        if self.preferences.general.shownotifications:
            self.trayicon.blink()
            self.notifsys.queue_msg(msg=msg,color='#444444',icon=icon)
    
    def logMessage(self,msg,tag='normal'):
        """
        Log Message function
        """
        # TODO: lotroassist: limit log buffer to X lines/bytes
        logbuffer=self.widgets.txtLog.get_buffer()
        iter=logbuffer.get_end_iter()
        logbuffer.insert_with_tags_by_name(iter,msg + '\n', tag)
        iter=logbuffer.get_end_iter()
        self.widgets.txtLog.scroll_to_iter(iter,0)
    
    def newLogLine(self,line,burst=False):
        """
        New line callback
        """
        # Pass the line to plugins
        for plugin in self.plugins.loaded_plugins():
            result=self.plugins.get_plugin_instance(plugin).newLine(line)
            if result and evogtk.EVOGTK_HAS_GTKSOURCEVIEW:
                # TODO: lotroassist: Line marking with custom icons in log
                pass
        # Add line to main log window
        if not burst:
            self.logMessage(line)
        
    def loadPlugins(self):
        """
        Load plugins
        """
        self.logMessage('Loading plugins','internal')
        pluginlist=self.plugins.plugin_list()
        self.logMessage('Found %s plugins' % len(pluginlist),'plugin')
        for plugin in pluginlist:
            self.plugins.load_plugin(plugin,env={'maingui':self})
            # Add plugin to interface if needed
            pluginclass=self.plugins.get_plugin_instance(plugin)
            if pluginclass.metadata.has_key('PLUGIN_DOCK'):
                pluginclass.widgets.vbxMain.unparent()
                pluginlabel=gtk.Label(pluginclass.metadata['PLUGIN_NAME'])
                if pluginclass.metadata['PLUGIN_DOCK']=='main':
                    self.widgets.ntbMain.append_page(pluginclass.widgets.vbxMain,pluginlabel)
                elif pluginclass.metadata['PLUGIN_DOCK']=='lists':
                    self.widgets.ntbLists.append_page(pluginclass.widgets.vbxMain,pluginlabel)
                elif pluginclass.metadata['PLUGIN_DOCK']=='console':
                    self.widgets.ntbConsole.append_page(pluginclass.widgets.vbxMain,pluginlabel)
                elif pluginclass.metadata['PLUGIN_DOCK']=='status':
                    self.widgets.hbxInfoBar.pack_end(pluginclass.widgets.vbxMain,False,False)
                else:
                    raise Exception('Plugin %s have no position for GUI docking' % plugin)
            self.logMessage('\tPlugin %s v%s initialized' % (pluginclass.metadata['PLUGIN_NAME'],pluginclass.metadata['PLUGIN_VERSION']),'plugin')
    
    def unloadPlugins(self):
        """
        Unload Plugins
        """
        for plugin in self.plugins.loaded_plugins():
            self.plugins.unload_plugin(plugin)
