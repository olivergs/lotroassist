# -*- coding: utf-8 -*-
###############################################################################
# (C) 2010 Oliver Gutiérrez <ogutsua@gmail.com>
# Map Markers plugin ruslotro.com marker download module
###############################################################################

# Python imports
import os
import httplib
import re

# GTK imports
import gobject

maps=(
    'angmar','annuminas','archet','breeland','breetown','carasgaladhon','durins_way','enedwaith','ered_luin','eregion',
    'ettenmoors','evendim','flaming_deeps','forochel','foundations_of_stone','lone_lands','lothlorien','mirkwood',
    'misty_mountains','moria','north_downs','nothern_barrow_downs','nud_melek','old_forest','redhorn_lodes',
    'rivendell','southern_barrow_downs','the_grand_stair','the_great_delving','the_shire','the_silvertine_lodes',
    'the_walls_of_moria','the_water_works','thorins_gate','trollshaws','zelem_melek','zirakzigil'
)

remarker=re.compile(r'\[(-*?\d+\.\d*,-*\d+\.\d*,\".*\",\d+,\".*\")\]')
remarkerdata=re.compile(r'(?P<lat>-*?\d+\.\d*),(?P<lon>-*\d+\.\d*),(?P<name>\".*\"),\d+,(?P<type>\".*\")')

def downloadMarkers(map):
    """
    Downloads markers directly from ruslotro.com
    """
    # TODO: lotroassist.plugins.mapmark.mapdata.markerload: Use non blocking method for downloading markers
    conn=httplib.HTTPConnection('dynmap.ruslotro.com')
    conn.request('GET','/data/%s.js' % map)
    resp=conn.getresponse().read()
    markersdata=remarker.findall(resp)
    markers=[]
    for marker in markersdata:
        res=remarkerdata.search(marker)
        if res:
            lat=float(res.group('lat'))
            lon=float(res.group('lon'))
            name=res.group('name').replace('"','').replace('&','and').replace(';','').replace('<','[').replace('>',']')
            type=res.group('type').replace('"','').replace('&','and').replace(';','').replace('<','[').replace('>',']')
        markers.append([lat,lon,name,type])
    return markers

def readMarkers(map):
    """
    Read markers from local file
    """
    mapfile='plugins/mapmark/mapdata/markers/%s.dat' % map
    if os.path.isfile(mapfile):
        fd=open(mapfile,'r')
        line=fd.readline()
        markerlist=[]
        while line:
            line=fd.readline().strip()
            if line:
                lat,lon,name,type=line.split(';')
                markerlist.append([float(lat),float(lon),name,type])
        # Close file
        fd.close()
        return markerlist
    else:
        return None

def saveMarkers(*args,**kwargs):
    """
    Saves markers to files for offline use
    """
    for map in maps:
        yield (map,maps.index(map),len(maps)-1)      
        markers=downloadMarkers(map)
        if markers:
            # Open file
            fd=open('plugins/mapmark/mapdata/markers/%s.dat' % map,'wb')
            for marker in markers:
                # Save marker to file
                fd.write('%s;%s;%s;%s\n' % (marker[0],marker[1],marker[2],marker[3]))
            # Close file
            fd.close()
            
def loadMarkers(map,online):
    """
    Load markers from previously saved files
    """
    if online:
        return downloadMarkers(map)
    else:
        return readMarkers(map)