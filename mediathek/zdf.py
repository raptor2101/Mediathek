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
    
    self.menuTree = (
      TreeNode("0","Startseite","https://zdf-cdn.live.cellular.de/mediathekV2/start-page",True),
      TreeNode("1","Ketegorieren","https://zdf-cdn.live.cellular.de/mediathekV2/categories",True),
      TreeNode("2","Sendungen von A-Z","https://zdf-cdn.live.cellular.de/mediathekV2/brands-alphabetical",True),
      TreeNode("3","Sendung verpasst?","https://zdf-cdn.live.cellular.de/mediathekV2/broadcast-missed/%s",True)
      );
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
    callhash = self.gui.storeJsonFile(jsonObject);
    
    counter=0;
    
    if("stage" in jsonObject):
      for stageObject in jsonObject["stage"]:
        if(stageObject["type"]=="video"):
          self.buildVideoLink(stageObject,counter);
    
    if("cluster" in jsonObject):
      for clusterObject in jsonObject["cluster"]:
        if clusterObject["type"].startswith("teaser"):
          path = "cluster.%d.teaser"%(counter)
          self.gui.buildJsonLink(self,clusterObject["name"],path,callhash,counter)
        counter=counter+1;
      
  def buildJsonMenu(self, path,callhash, initCount):
    jsonObject=self.gui.loadJsonFile(callhash);
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
    if("formitaeten" in videoObject):
      links = self.extractLinks(jsonObject);
      self.gui.buildVideoLink(DisplayObject(title,subTitle,imageLink,description,links,True),self,counter);
    else:
      link = videoObject["url"];
      self.gui.buildVideoLink(DisplayObject(title,subTitle,imageLink,description,link,"JsonLink"),self,counter);
    
  def playVideoFromJsonLink(self,link):
    jsonObject = json.loads(self.loadPage(link));
    links = self.extractLinks(jsonObject);
    self.gui.play(links);
  def extractLinks(self,jsonObject):
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
    return links;
    
      
    

    
    
