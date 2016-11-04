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
import re,math,traceback,time
from mediathek import *
import json
    
class ZDFMediathek(Mediathek):
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui;
    if(self.gui.preferedStreamTyp == 0):
      self.baseType = "http_na_na";
    elif (self.gui.preferedStreamTyp == 1):  
      self.baseType = "rtmp_smil_http"
    elif (self.gui.preferedStreamTyp == 2):
      self.baseType ="mms_asx_http";
    else:
      self.baseType ="rtsp_mov_http";
    
    self.menuTree = (
      TreeNode("0","Startseite","https://zdf-cdn.live.cellular.de/mediathekV2/start-page",True),
      TreeNode("0","Startseite","https://zdf-cdn.live.cellular.de/mediathekV2/start-page",True),
      );
    regex_imageLink = "/ZDFmediathek/contentblob/\\d+/timg\\d+x\\d+blob/\\d+";
    #ZDFmediathek/beitrag/live/
    self.regex_videoPageLink = "/ZDFmediathek/beitrag/((video)|(live))/\\d+?/.*flash=off";
    self.regex_topicPageLink = "/ZDFmediathek/((kanaluebersicht/aktuellste/\\d+.*)|(hauptnavigation/nachrichten/ganze-sendungen.*))flash=off";
    self._regex_extractTopicObject = re.compile("<li.*\\s*<div class=\"image\">\\s*<a href=\""+self.regex_topicPageLink+"\">\\s*<img src=\""+regex_imageLink+"\" title=\".*\" alt=\".*\"/>\\s*</a>\\s*</div>\\s*<div class=\"text\">\\s*<p( class=\".*\"){0,1}>\\s*<a href=\""+self.regex_topicPageLink+"\"( class=\"orangeUpper\"){0,1}>.*</a>\\s*</p>\\s*<p>\\s*<b>\\s*<a href=\""+self.regex_topicPageLink+"\">\\s*.*</a>");
    self._regex_extractPageNavigation = re.compile("<a href=\""+self.regex_topicPageLink+"\" .*>.*?</a>");
    
    
    self._regex_extractPictureLink = re.compile(regex_imageLink);
    self._regex_extractPicSize = re.compile("\\d{2,4}x\\d{2,4}");
    
    self._regex_extractTopicPageLink = re.compile(self.regex_topicPageLink);    
    self._regex_extractTopicTitle = re.compile("<a href=\"/ZDFmediathek/.*flash=off\".*>[^<].*</a>");
    
    self._regex_extractVideoPageLink = re.compile(self.regex_videoPageLink);
    self._regex_extractVideoID = re.compile("/\\d+/");
    self._regex_extractVideoLink = re.compile("");
    self.replace_html = re.compile("<.*?>");
    
    self.rootLink = "http://www.zdf.de";
    self.searchSite = "http://www.zdf.de/ZDFmediathek/suche?flash=off"
    self.xmlService = "http://www.zdf.de/ZDFmediathek/xmlservice/web/beitragsDetails?id=%s&ak=web";
  @classmethod
  def name(self):
    return "ZDF";
    
  def isSearchable(self):
    return False;
  
  def searchVideo(self, searchText):
    return;
    
  def buildPageMenu(self, link, initCount):
    self.gui.log("buildPageMenu: "+link);
    jsonObject = json.loads(self.loadPage(link));
    self.gui.storeJsonFile(jsonObject);
    
    counter=0;
    for clusterObject in jsonObject["cluster"]:
      if clusterObject["type"]=="teaser":
        path = "cluster.%d.teaser"%(counter)
        self.gui.buildJsonLink(self,clusterObject["name"],path,initCount)
      counter=counter+1;
      
  def buildJsonMenu(self, path, initCount):
    jsonObject=self.gui.loadJsonFile();
    jsonObject=self.walkJson(path,jsonObject);
   
    categoriePages=[];
    videoObjects=[];
    counter=0;
    
    for entry in jsonObject:
      if entry["type"] == "brand":
        categoriePages.append(entry);
      if entry["type"] == "video" and len(videoObjects) < 50:
        videoObjects.append(entry);  
    
    counter=initCount+len(videoObjects)+len(categoriePages);
    self.gui.log("CategoriePages: %d"%len(categoriePages));
    self.gui.log("VideoPages: %d"%len(videoObjects));  
    for categoriePage in categoriePages:
      title=categoriePage["titel"];
      subTitle=categoriePage["beschreibung"];
      imageLink="";
      for width,imageObject in categoriePage["teaserBild"].iteritems():
        if int(width)<=840:
          imageLink=imageObject["url"];
      url = categoriePage["url"];
      self.gui.buildVideoLink(DisplayObject(title,subTitle,imageLink,"",url,False),self,counter);
    
    
    
    for videoObject in videoObjects:
      self.buildVideoLink(videoObject,counter);
      
      
  def buildVideoLink(self,videoObject,counter):
    title=videoObject["headline"];
    subTitle=videoObject["titel"];
    description=videoObject["beschreibung"];
    imageLink="";
    for width,imageObject in videoObject["teaserBild"].iteritems():
      if int(width)<=840:
        imageLink=imageObject["url"];
    link = videoObject["url"];
    self.gui.buildVideoLink(DisplayObject(title,subTitle,imageLink,description,link,"JsonLink"),self,counter);
    
  def playVideoFromJsonLink(self,link):
    jsonObject = json.loads(self.loadPage(link));
    links={};
    for formitaete in jsonObject["document"]["formitaeten"]:
      url = formitaete["url"];
      quality = formitaete["quality"];
      hd = formitaete["hd"];
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
    self.gui.play(links);
    
      
    

    
    
