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
import re,time,json
from mediathek import *
from xml.dom import minidom;


regex_dateString = re.compile("\\d{2} ((\\w{3})|(\\d{2})) \\d{4}");
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

class DreiSatMediathek(Mediathek):
  @classmethod
  def name(self):
    return "3Sat";
  def isSearchable(self):
    return True;
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui;
    if(self.gui.preferedStreamTyp == 0):
      self.baseType = "video/x-ms-asf";
    elif (self.gui.preferedStreamTyp == 1):  
      self.baseType = "video/x-ms-asf"
    elif (self.gui.preferedStreamTyp == 2):
      self.baseType ="video/x-ms-asf";
    else:
      self.baseType ="video/quicktime";
    self.webEmType = "video/webm";
    self.menuTree = (
      TreeNode("0","Hauptseite","http://www.3sat.de/mediathek/",True),
      TreeNode("1","Hauptseite","http://www.3sat.de/mediathek/",True),
      TreeNode("2","Hauptseite","http://www.3sat.de/mediathek/",True)
      );

    self.rootLink = "http://www.3sat.de"
    self.searchLink = 'http://www.3sat.de/mediathek/mediathek';

    self.regex_objectLink = re.compile("obj=(\\d+)");

    self.xmlService_Link = "http://www.3sat.de/mediathek/xmlservice.php/v3/web/beitragsDetails?id=%s"
    self.jsonService_Link = "http://tmd.3sat.de/tmd/2/ngplayer_2_3/vod/ptmd/3sat/%s"

  def buildPageMenu(self, link, initCount):
    self.gui.log("buildPageMenu: "+link);

    mainPage = self.loadPage(link);
    matches = list(self.regex_objectLink.finditer(mainPage));
    counter = len(matches)+initCount
    for match in matches:
      self.buildVideoLink(match.group(1), counter);

  def buildVideoLink(self, objectId, counter):
    xmlPage = self.loadPage(self.xmlService_Link%objectId);
    xmlPage = minidom.parseString(xmlPage);
    videoNode = xmlPage.getElementsByTagName("video")[0];
    informationNode = xmlPage.getElementsByTagName("information")[0];
    detailsNode = xmlPage.getElementsByTagName("details")[0];
    title = self.readText(informationNode,"title");
    basename = self.readText(detailsNode,"basename");

    self.gui.buildVideoLink(DisplayObject(title,"","","",self.jsonService_Link%basename,"JsonLink",None,None),self,counter);

  def playVideoFromJsonLink(self,link):
    page = self.loadPage(link);
    jsonObject = json.loads(page);
    links = self.extractLinks(jsonObject["priorityList"]);
    self.gui.play(links);

  def extractLinks(self,jsonList):
    links={};
    for jsonListObject in jsonList:
      for formitaete in jsonListObject["formitaeten"]:
        for jsonObject in formitaete["qualities"]:
          quality = jsonObject["quality"];
          hd = jsonObject["hd"];
          url = jsonObject["audio"]["tracks"][0]["uri"];
          if("manifest.f4m" in url):
            continue;
          self.gui.log("quality:%s hd:%s url:%s"%(quality,hd,url));
          if hd == True:
            links[4] = SimpleLink(url, -1); 
          else:
            if quality == "low":
              links[0] = SimpleLink(url, -1);
            if quality == "med":
              links[1] = SimpleLink(url, -1);
            if quality == "high":
              links[2] = SimpleLink(url, -1);
            if quality == "veryhigh":
              links[3] = SimpleLink(url, -1);
            if quality == "auto":
              links[3] = SimpleLink(url, -1);
    return links;

  def searchVideo(self, searchText):
    values ={'mode':'search',
             'query':searchText,
             'red': '',
             'query_time': '',
             'query_sort': '',
             'query_order':''
             }
    mainPage = self.loadPage(self.searchLink,values);
    results = self.regex_searchResult.findall(mainPage);
    for result in results:
      objectLink = self.regex_searchResultLink.search(result).group();
      infoLink = self.rootLink+objectLink
      infoPage = self.loadPage(infoLink);
      title = self.regex_searchTitle.search(infoPage).group();
      detail = self.regex_searchDetail.search(infoPage).group();
      image = self.regex_searchImage.search(infoPage).group();
      title = self.replace_html.sub("", title);
      detail = self.replace_html.sub("", detail);
      try:
        dateString = self.regex_searchDate.search(infoPage).group();
        pubDate = time.strptime(dateString,"%d.%m.%Y");
      except:
        pubDate = time.gmtime();
      videoLink = self.rootLink+objectLink+"&mode=play";
      videoPage = self.loadPage(videoLink);
      video = self.regex_searchLink.search(videoPage).group();
      video = video.replace("fstreaming","wstreaming").replace(".smil",".asx");
      links = {}
      links[2] = SimpleLink(video,0)
      self.gui.buildVideoLink(DisplayObject(title,"",self.rootLink + image,detail,links,True, pubDate),self,len(results));
  def readText(self,node,textNode):
    try:
      node = node.getElementsByTagName(textNode)[0].firstChild;
      return unicode(node.data);
    except:
      return "";
  def loadConfigXml(self, link):
    self.gui.log("load:"+link)
    xmlPage = self.loadPage(link);
    return minidom.parseString(xmlPage);  
  def extractVideoObjects(self, rssFeed, initCount):
    nodes = rssFeed.getElementsByTagName("item");
    nodeCount = initCount + len(nodes)
    for itemNode in nodes:
      try:
        self.extractVideoInformation(itemNode,nodeCount);
      except:
        pass

  def parseDate(self,dateString):
    dateString = regex_dateString.search(dateString).group();
    for month in month_replacements.keys():
      dateString = dateString.replace(month,month_replacements[month]);
    return time.strptime(dateString,"%d %m %Y");

  def extractVideoInformation(self, itemNode, nodeCount):
    title = self.readText(itemNode,"title");
    self.gui.log(title)
    dateString = self.readText(itemNode,"pubDate");
    pubDate = self.parseDate(dateString);
    descriptionNode = itemNode.getElementsByTagName("description")[0].firstChild.data;
    description = unicode(descriptionNode);
    picture = "";
    pictureNodes = itemNode.getElementsByTagName("media:thumbnail");
    if(len(pictureNodes) > 0):
      picture = pictureNodes[0].getAttribute("url");
    links = {};
    for contentNode in itemNode.getElementsByTagName("media:content"):
      height = int(contentNode.getAttribute("height"));
      url = contentNode.getAttribute("url");
      size = int(contentNode.getAttribute("fileSize"));
      if(height < 300):
        links[0] = SimpleLink(url, size);
      elif (height < 480):
        links[1] = SimpleLink(url, size);
      else:
        links[2] = SimpleLink(url, size);
    if links:
      self.gui.buildVideoLink(DisplayObject(title,"",picture,description,links,True, pubDate),self,nodeCount);
