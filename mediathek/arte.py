# -*- coding: utf-8 -*- 
#-------------LicenseHeader--------------
# plugin.video.Mediathek - Gives access to most video-platforms from German public service broadcasters
# Copyright (C) 2010  Raptor 2101 [raptor2101@gmx.de]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 
import re, traceback
from mediathek import *
from xml.dom import minidom
from xml.dom import Node;

regex_dateString = re.compile("\\d{1,2} ((\\w{3})|(\\d{2})) \\d{4}");
month_replacements = {
    "Jan":"01",
    "Feb":"02",
    "Mar":"03",
    "Apr":"04",
    "May":"05",
    "Jun":"06",
    "Jul":"07",
    "Aug":"08",
    "Sep":"09",
    "Oct":"10",
    "Nov":"11",
    "Dec":"12",
    
  };

class ARTEMediathek(Mediathek):
  @classmethod
  def name(self):
    return "ARTE";
  def isSearchable(self):
    return False;
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui;
    self.rootLink = "http://www.arte.tv";
    self.menuTree = (
      TreeNode("0","Neuste Videos",self.rootLink+"/guide/de",True),
      
      TreeNode("1","Programme","",False, (
        TreeNode("1.0",u"360° - Geo",self.rootLink+"/de/do_delegate/videos/sendungen/360_geo/index-3188704,view,rss.xml",True),
        TreeNode("1.1",u"ARTE Journal",self.rootLink+"/de/do_delegate/videos/artejournal/index-3188708,view,rss.xml",True),
        TreeNode("1.2",u"ARTE Lounge",self.rootLink+"/de/do_delegate/arte_lounge/index-3219086,view,rss.xml",True),
        TreeNode("1.3",u"ARTE Reportage",self.rootLink+"/de/do_delegate/videos/sendungen/arte_reportage/index-3188710,view,rss.xml",True),
        TreeNode("1.4",u"Cut up",self.rootLink+"/de/do_delegate/cut_up/index-3199714,view,rss.xml",True),
        TreeNode("1.5",u"Der Blogger",self.rootLink+"/de/do_delegate/videos/sendungen/blogger/index-3193602,view,rss.xml",True),
        TreeNode("1.6",u"Die Nacht / La nuit",self.rootLink+"/de/do_delegate/die_nacht_la_nuit/index-3188716,view,rss.xml",True),
        TreeNode("1.7",u"Geschichte am Mittwoch",self.rootLink+"/de/do_delegate/geschichte_mittwoch/index-3188722,view,rss.xml",True),
        TreeNode("1.8",u"Giordano trifft",self.rootLink+"/de/do_delegate/giordano_hebdo/index-3199710,view,rss.xml",True),
        TreeNode("1.9",u"Global",self.rootLink+"/de/do_delegate/global_mag/index-3188718,view,rss.xml",True),
        TreeNode("1.10",u"Karambolage",self.rootLink+"/de/do_delegate/videos/sendungen/karambolage/index-3224652,view,rss.xml",True),
        TreeNode("1.11",u"Künstler hautnah",self.rootLink+"/de/do_delegate/l_art_et_la_maniere/index-3188720,view,rss.xml",True),
        TreeNode("1.12",u"Kurzschluss",self.rootLink+"/de/do_delegate/videos/sendungen/kurzschluss/index-3188712,view,rss.xml",True),
        TreeNode("1.13",u"Metropolis",self.rootLink+"/de/do_delegate/videos/sendungen/metropolis/index-3188724,view,rss.xml",True),
        TreeNode("1.14",u"Philosophie",self.rootLink+"/de/do_delegate/videos/sendungen/philosophie/index-3188728,view,rss.xml",True),
        TreeNode("1.15",u"Tracks",self.rootLink+"/de/do_delegate/videos/tracks/index-3188628,view,rss.xml",True),
        TreeNode("1.16",u"X:enius",self.rootLink+"/de/do_delegate/videos/sendungen/xenius/index-3188730,view,rss.xml",True),
        TreeNode("1.17",u"Yourope",self.rootLink+"/de/do_delegate/videos/sendungen/yourope/index-3188732,view,rss.xml",True),
      )),
      TreeNode("2","Themen","",False,(
        TreeNode("2.0",u"Aktuelles",self.rootLink+"/de/do_delegate/videos/alle_videos/aktuelles/index-3188636,view,rss.xml",True),
        TreeNode("2.1",u"Dokumentationen",self.rootLink+"/de/do_delegate/videos/alle_videos/dokus/index-3188646,view,rss.xml",True),
        TreeNode("2.2",u"Entdeckung",self.rootLink+"/de/do_delegate/videos/entdeckung/index-3188644,view,rss.xml",True),
        TreeNode("2.3",u"Europa",self.rootLink+"/de/do_delegate/videos/alle_videos/europa/index-3188648,view,rss.xml",True),
        TreeNode("2.4",u"Geopolitik & Geschichte",self.rootLink+"/de/do_delegate/videos/alle_videos/geopolitik_geschichte/index-3188654,view,rss.xml",True),
        TreeNode("2.5",u"Gesellschaft",self.rootLink+"/de/do_delegate/videos/alle_videos/gesellschaft/index-3188652,view,rss.xml",True),
        TreeNode("2.6",u"Junior",self.rootLink+"/de/do_delegate/videos/alle_videos/junior/index-3188656,view,rss.xml",True),
        TreeNode("2.7",u"Kino & Serien",self.rootLink+"/de/do_delegate/videos/alle_videos/kino_serien/index-3188642,view,rss.xml",True),
        TreeNode("2.8",u"Kunst & Kultur",self.rootLink+"/de/do_delegate/videos/alle_videos/kunst_kultur/index-3188640,view,rss.xml",True),
        TreeNode("2.9",u"Popkultur & Musik",self.rootLink+"/de/do_delegate/videos/alle_videos/popkultur_musik/index-3188638,view,rss.xml",True),
        TreeNode("2.10",u"Umwelt & Wissenschaft",self.rootLink+"/de/do_delegate/videos/alle_videos/umwelt_wissenschaft/index-3188650,view,rss.xml",True),
      )),
    );
      
    self.regex_VideoPageLinks = re.compile("href=[\"'](/guide/de/\d{6}-\d{3}/.+?)[\"']");
    
    self.regex_JSONPageLink = re.compile("http://arte.tv/papi/tvguide/videos/stream/player/D/\d{6}-\d{3}.+?/ALL/ALL.json");
    self.regex_JSON_VideoLink = re.compile("\"HTTP_MP4_.+?\":{.*?\"bitrate\":(\d+),.*?\"url\":\"(http://.*?.mp4)\".*?}");
    self.regex_JSON_ImageLink = re.compile("\"original\":\"(http://www.arte.tv/papi/tvguide/images/.*?.jpg)\"");
    self.regex_JSON_Detail = re.compile("\"VDE\":\"(.*?)\"");
    self.regex_JSON_Titel = re.compile("\"VTI\":\"(.*?)\"");
    
    
    
    
  def buildPageMenu(self, link, initCount):
    self.gui.log("buildPageMenu: "+link);
    htmlPage = self.loadPage(link);
    self.extractVideoLinks(htmlPage, initCount);
  
  
  #def searchVideo(self, searchText):
  #  link = self.searchLink + searchText
  #  self.buildPageMenu(link,0);
    
  def extractVideoLinks(self, htmlPage, initCount):
    links = set();
    for videoPageLink in self.regex_VideoPageLinks.finditer(htmlPage):
      link = videoPageLink.group(1);
      
      if(link not in links):
	links.add(link);
    linkCount = initCount + len(links);
    for link in links:
      videoPage = self.loadPage(self.rootLink+link);
      match = self.regex_JSONPageLink.search(videoPage);
      if(match is not None):
	link = match.group(0);
	jsonPage = self.loadPage(link).decode('utf-8');
	videoLinks = {}
	for match in self.regex_JSON_VideoLink.finditer(jsonPage):
	  bitrate = match.group(1);
	  url = match.group(2);
	  if(bitrate < 800):
	    videoLinks[0] = SimpleLink(url,0);
	  if(bitrate >= 800 and bitrate < 1500):
	    videoLinks[1] = SimpleLink(url,0);
	  if(bitrate >= 1500 and bitrate <= 2200):
	    videoLinks[1] = SimpleLink(url,0);
	  if(bitrate >= 2200):
	    videoLinks[3] = SimpleLink(url,0);
	picture = self.regex_JSON_ImageLink.search(jsonPage).group(1);
	title = self.regex_JSON_Titel.search(jsonPage).group(1);
	detail =  self.regex_JSON_Detail.search(jsonPage).group(1);
	self.gui.buildVideoLink(DisplayObject(title,"",picture,detail,videoLinks,True, None),self,linkCount);
	
   
    
    
      