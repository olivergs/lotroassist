# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# LOTROAssist map mark plugin
###############################################################################

# Python Imports
import re
import math

# GTK Imports
import gobject,gtk,cairo

# EVOGTK Imports
from evogtk.gui import GUIClass
from evogtk.tools import setupComboBox,openWithDefaultApp
from evogtk.factories import TreeViewFactory,DialogFactory
from evogtk.widgets import CairoScroller
from evogtk.gui import threadtasks

# Plugin Imports
import mapdata
from mapdata.markerload import loadMarkers,saveMarkers

class Plugin(GUIClass):
    """
    # LOTROAssist map mark plugin class
    """
    metadata={
        'PLUGIN_NAME': 'Map',
        'PLUGIN_CODENAME': 'mapmark',
        'PLUGIN_VERSION': '0.1',
        'PLUGIN_DESC': 'Lord Of The Rings Online Assistant plugin for map marking',
        'PLUGIN_COPYRIGHT': '(C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>',
        'PLUGIN_WEBSITE': 'http://www.evosistemas.com',
        'PLUGIN_GUI': 'mapmark.ui',
        'PLUGIN_CALLBACKS': 'mapmark',
        'PLUGIN_DOCK': 'main',
    }
    
    def initialize(self):
        """
        Initialization function
        """
        # Dialog factory
        self.dialogs=DialogFactory(self.widgets.vboxMain)
        # Custom markers treeview
        self.custommarkers=TreeViewFactory('list',
                                   ['str','str','str'],
                                   ['Name','Latitude','Longitude'],
                                   treeview=self.widgets.tvCustomMarkers)
        # Original image width and height
        self.width=1900
        self.height=1200
        # Current position
        self.currentpos=(0,0,0)
        # Current location image
        self.curlocimg=cairo.ImageSurface.create_from_png('plugins/mapmark/pixmaps/currentloc.png')
        # Regular expression for location command management
        self.regexploc=re.compile(r'You are at: r(?P<zone>.*) lx(?P<xpos>\d+) ly(?P<ypos>\d+) ox(?P<oxpos>\d+\.*\d+) oy(?P<oypos>\d+\.*\d+) oz(?P<ozpos>\d+\.*\d+) h(?P<facing>\d+\.*\d+)')
        # Task list
        self.tasks=[]
        # Initialize Cairo Scroller drawing and size
        self.widgets.cascrMapViewer.canvas.set_draw_callback(self.drawMap)
        self.widgets.cascrMapViewer.set_zoom_parameters(origwidth=self.width,origheight=self.height)
        # Add mouse movement event for map tooltips and show coordinates
        self.widgets.cascrMapViewer.canvas.add_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK)
        self.widgets.cascrMapViewer.canvas.connect('motion-notify-event',self.showMarkerName)
        self.widgets.cascrMapViewer.canvas.connect('button-press-event',self.mapClick)
        # Cursors for map linking
        self.pointer=gtk.gdk.Cursor(gtk.gdk.HAND2)
        # Generate zones combobox
        self.zonescombo=setupComboBox(mapdata.zones,self.widgets.tlbcMapViewerZone,active='Middle Earth',changed_callback=self.setZone)
        # Check map data
        self.checkMapData()
        # Load initial zone
        self.setZone()
    
    def newLine(self,line):
        """
        New line analysing function
        """
        global currentpos
        resp=self.regexploc.search(line)
        if resp:
            x=int(resp.group('xpos'))
            y=int(resp.group('ypos'))
            facing=float(resp.group('facing'))
            longitude=((1467-x)/10.0)*-1
            latitude=((1243-y)/10.0)*-1
            self.maingui.showNotification('Actual Location: %sS %sW' % (latitude,longitude),icon='plugins/mapmark/pixmaps/location.png')
            currentpos=(latitude,longitude,facing)
            self.redrawMap()                  
            return True
    
    def checkMapData(self):
        """
        Checks if all map data is valid
        """
        for zoneid in mapdata.maplinks:
            if not mapdata.zones.has_key(zoneid):
                self.dialogs.msgDialog('Invalid zone "%s" in maplinks ' % zoneid,'warning')
            for maplinkid in mapdata.maplinks[zoneid]:
                if not mapdata.zones.has_key(mapdata.maplinks[zoneid][maplinkid]):
                    self.dialogs.msgDialog('Invalid map link in "%s" ("%s")' % (zoneid,maplinkid),'warning')
        for zoneid in mapdata.zones:
            if mapdata.zones[zoneid][6] and not mapdata.zones.has_key(mapdata.zones[zoneid][6]):
                self.dialogs.msgDialog('Invalid parent zone "%s" for zone "%s"' % (mapdata.zones[zoneid][6],zoneid),'warning')
        
    def updateMarkers(self,widget=None):
        """
        Download and save markers from internet
        """
        # Create task
        self.task=threadtasks.ThreadTask(threadtasks.TYPE_GENERATOR,saveMarkers,self.updateMarkersProgress,self.updateMarkersEnd)
        # Show progress bar
        self.widgets.cascrMapViewer.hide()
        self.widgets.lblMapViewerCoords.hide()
        self.widgets.algMapViewerProgress.show()
        # Run task
        self.task.start()
        # Deactivate download button
        self.widgets.tlbMapViewer.set_sensitive(False)
        
    def updateMarkersProgress(self,name,actual,total):
        """
        Sets progress on updating markers download
        """
        self.widgets.prgMapViewer.set_text('Downloading zone %s' % name)
        self.widgets.prgMapViewer.set_fraction(float(actual)/total)
        return False

    def updateMarkersEnd(self):
        """
        Hide progress bar
        """
        self.widgets.algMapViewerProgress.hide()
        self.widgets.cascrMapViewer.show()
        self.widgets.lblMapViewerCoords.show()
        self.widgets.tlbMapViewer.set_sensitive(True)
        del(self.task)

    def setZone(self,widget=None,zoneid=None):
        """
        Draws map for a specified zone
        """
        if not zoneid:
            zoneid=self.zonescombo.get_active_text()
        else:
            # Set combo to the selected zone
            index=0
            mapzones=mapdata.zones.keys()
            mapzones.sort()
            for zonename in mapzones:
                if zonename==zoneid:
                    self.zonescombo.set_active(index)
                    return
                index+=1
    
        if mapdata.zones.has_key(zoneid):
            self.zone=mapdata.zones[zoneid]
            self.mapimg=cairo.ImageSurface.create_from_png('plugins/mapmark/pixmaps/maps/%s' % self.zone[1])
            self.locations={}
            # Generate map locations
            if self.zone[0]:
                xdist=abs(self.zone[5]-self.zone[3])
                ydist=abs(self.zone[2]-self.zone[4])
                markers=loadMarkers(self.zone[0],self.ui.tlbtMapViewerOnlineMarkers)
                if markers:
                    for mark in markers:
                        # Check if mark is in zone area
                        if self.zone[3] <= mark[1] <=  self.zone[5] and self.zone[2] >= mark[0] >= self.zone[4]:
                            # Calculate position from it's latitude/longitude
                            x=self.width*abs(mark[1]-self.zone[3])/xdist
                            y=self.height*abs(mark[0]-self.zone[2])/ydist
                            markertype=mark[3]
                            textcolor,drawcolor=self.getMarkerType(markertype)[0]
                            # Add location to location information dictionary
                            self.locations[(x,y)]=(mark[2],markertype,drawcolor,textcolor,mark[0],mark[1])
                        else:
                            msg='Map mark "%s" (%s %s) is not located in "%s" limits (%s,%s)-(%s,%s)' % (mark[2],mark[0],mark[1],zoneid,self.zone[2],self.zone[3],self.zone[4],self.zone[5])
                            self.dialogs.msgDialog(msg,'warning')
                else:
                    msg='No markers loaded. Check if you\'ve downloaded mark information for offline use or if you are online, check internet connection'  
                    self.dialogs.msgDialog(msg,'warning')
        else:
            raise Exception('Invalid zone selected')
        self.zoomOptimal()
    
    def worldToMapCoords(self,lat,lon):
        """
        Convert from world coordinate system to current map coordinates
        """
        if self.zone[0]:
            xdist=abs(self.zone[5]-self.zone[3])
            ydist=abs(self.zone[2]-self.zone[4])
            # Check if mark is in zone area
            if self.zone[3] <= lon <=  self.zone[5] and self.zone[2] >= lat >= self.zone[4]:
                # Calculate position from it's latitude/longitude
                return (self.width*abs(lon-self.zone[3])/xdist,self.height*abs(lat-self.zone[2])/ydist)
            else:
                return None
    
    def drawMap(self,ctx):
        """
        Draw the canvas
        """
        if self.zone:
            # Draw map image
            ctx.set_source_surface(self.mapimg,0,0)
            ctx.paint()
            # Draw markers
            for location in self.locations:
                x=location[0]
                y=location[1]
                markertype=self.locations[location][1]
                color=self.locations[location][2]
                if self.getMarkerType(markertype)[1]:
                    markername=self.locations[location][0].lower()
                    search=self.ui.entMapViewerSearch.lower()
                    # Draw marker
                    zoom=self.widgets.cascrMapViewer.getZoomScale()
                    self.widgets.cascrMapViewer.canvas.draw_arc(ctx,x,y,4/zoom,borderwidth=1/zoom,color=color)
                    # If marker is eligible for current search draw a circle around it
                    if search and markername[:len(search)]==search:
                        self.widgets.cascrMapViewer.canvas.draw_arc(ctx,x,y,8/zoom,bordercolor=(0,1,1),borderwidth=3/zoom,fill=False)
            # Draw current pos
            coords=self.worldToMapCoords(self.currentpos[0],self.currentpos[1])
            if coords:
                # Current position drawing
                ctx.translate(coords[0],coords[1])
                ctx.rotate(math.radians(self.currentpos[2]))
                self.widgets.cascrMapViewer.canvas.draw_png(ctx,-16,-16,self.curlocimg)
    
    def redrawMap(self,widget=None):
        """
        Redraw cairo canvas
        """
        self.widgets.cascrMapViewer.redrawCanvas()
    
    def getMarkerType(self,markertype):
        """
        Gets the type information for a marker
        """
        if mapdata.markertypes.has_key(markertype):
            if markertype=='Mob':
                enabled=self.ui.tlbtMapViewerMob
            elif markertype=='POI':
                enabled=self.ui.tlbtMapViewerPOI
            elif markertype=='NPC':
                enabled=self.ui.tlbtMapViewerNPC
            elif markertype=='Item':
                enabled=self.ui.tlbtMapViewerItem
            elif markertype=='Milestone':
                enabled=self.ui.tlbtMapViewerMilestone
            elif markertype=='Stablemaster':
                enabled=self.ui.tlbtMapViewerStablemaster
            return (mapdata.markertypes[markertype],enabled)
        return (['white',(1,1,1)],self.ui.tlbtMapViewerOther)
    
    def showMarkerName(self,widget,event):
        """
        Shows tooltip if the mouse is over a marker
        """
        cursor=None
        markerlist=[]
        self.ui.stbMapViewer=''
        zoom=self.widgets.cascrMapViewer.getZoomScale()
        # Update mouse coordinates
        if self.zone[0]:
            lat=self.zone[2]-(event.y*abs(self.zone[4]-self.zone[2])/(self.height*zoom))
            lon=self.zone[3]+(event.x*abs(self.zone[5]-self.zone[3])/(self.width*zoom))
            self.ui.lblMapViewerCoords='%.1f%s %.1f%s' % (abs(lat),lat>0 and 'N' or 'S',abs(lon),lon>0 and 'E' or 'W')
            # Check if we are in a marker and show marker data
            for location in self.locations:
                if location[0]*zoom-3 <= event.x <= location[0]*zoom+3 and location[1]*zoom-3 <= event.y <= location[1]*zoom+3:
                    markername=self.locations[location][0]
                    markertype=self.locations[location][1]
                    markercolor=self.locations[location][3]
                    markerlat='%s%s' % (abs(self.locations[location][4]),(self.locations[location][4]>0 and 'N' or 'S'))
                    markerlon='%s%s' % (abs(self.locations[location][5]),(self.locations[location][5]>0 and 'E' or 'W'))
                    markerlist.append('<b>[<span fgcolor="%s">%s</span>]</b> - <b>%s</b> (%s %s)' % (markercolor,markertype,markername,markerlat,markerlon))
                if markerlist:
                    markertip=''
                    for marker in markerlist:
                        markertip+=marker + '\n'
                    markertip=markertip[:-1]
                    self.widgets.cascrMapViewer.set_has_tooltip(True)
                    self.widgets.cascrMapViewer.set_tooltip_markup(markertip)
                else:
                    self.widgets.cascrMapViewer.set_has_tooltip(False)
        else:
            self.ui.lblMapViewerCoords=''
        # Check if we are in a map link
        if not markerlist and mapdata.maplinks.has_key(self.zonescombo.get_active_text()):
            for maplink in mapdata.maplinks[self.zonescombo.get_active_text()]:
                if maplink[0]*zoom <= event.x <= maplink[2]*zoom and maplink[1]*zoom <= event.y <= maplink[3]*zoom:
                    cursor=self.pointer
                    self.ui.stbMapViewer='Go to %s map' % mapdata.maplinks[self.zonescombo.get_active_text()][maplink]
                    break    
        # Change cursor if we are in a map link area
        self.widgets.cascrMapViewer.canvas.window.set_cursor(cursor)
    
    def mapClick(self,widget,event):
        """
        Handles mouse clicks on map
        """
        if event.button==1:
            absx=event.x
            absy=event.y
            zoom=self.widgets.cascrMapViewer.getZoomScale()
            # Check if we are in a map marker
            for location in self.locations:            
                if location[0]*zoom-4 <= absx <= location[0]*zoom+4 and location[1]*zoom-4 <= absy <= location[1]*zoom+4:
                    # Show popup with link information on click
                    markername=self.locations[location][0]
                    markertype=self.locations[location][1]
                    markerlat='%s%s' % (abs(self.locations[location][4]),(self.locations[location][4]>0 and 'N' or 'S'))
                    markerlon='%s%s' % (abs(self.locations[location][5]),(self.locations[location][5]>0 and 'E' or 'W'))
                    self.ui.lblMarkerInfoName=markername
                    self.ui.lblMarkerInfoType=markertype
                    self.ui.lblMarkerInfoLatitude=markerlat
                    self.ui.lblMarkerInfoLongitude=markerlon
                    self.widgets.diaMarkerInfo.set_title(markername)
                    self.widgets.diaMarkerInfo.show()
                    return 
            # Check if we are in a map link
            if mapdata.maplinks.has_key(self.zonescombo.get_active_text()):
                for maplink in mapdata.maplinks[self.zonescombo.get_active_text()]:
                    if maplink[0]*zoom <= absx <= maplink[2]*zoom and maplink[1]*zoom <= absy <= maplink[3]*zoom:
                        zoneid=mapdata.maplinks[self.zonescombo.get_active_text()][maplink]
                        self.setZone(zoneid=zoneid)
                        return
        elif event.button==3:
            # If right click we go to parent map
            zoneid=mapdata.zones[self.zonescombo.get_active_text()][6]
            if zoneid:
                self.setZone(zoneid=zoneid)
        self.widgets.cascrMapViewer.canvas.window.set_cursor(None)
        
    def zoomOptimal(self,widget=None):
        """
        Zoom to optimal viewing of map
        """
        self.widgets.cascrMapViewer.zoomOptimal(widget)
    
    def zoomOriginal(self,widget):
        """
        Zoom to optimal viewing of map
        """
        self.widgets.cascrMapViewer.zoomOriginal(widget)
    
    def zoomIn(self,widget=None):
        """
        Zoom to optimal viewing of map
        """
        self.widgets.cascrMapViewer.zoomIn(widget)
    
    def zoomOut(self,widget=None):
        """
        Zoom to optimal viewing of map
        """
        self.widgets.cascrMapViewer.zoomOut(widget)
