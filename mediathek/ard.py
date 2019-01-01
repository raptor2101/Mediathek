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
import re, time, datetime, json;
from bs4 import BeautifulSoup;
from mediathek import *

class ARDMediathek(Mediathek):
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui;
    self.rootLink = "https://www.ardmediathek.de"
    self.menuTree = (
                      TreeNode("0","Neuste Videos",self.rootLink+"/ard/",True),
                      TreeNode("1","Sendungen von A-Z","",False,(
                        TreeNode("1.0","0-9",self.rootLink+"/tv/sendungen-a-z?buchstabe=0-9",True),
                        TreeNode("1.1","A",self.rootLink+"/tv/sendungen-a-z?buchstabe=A",True),
                        TreeNode("1.2","B",self.rootLink+"/tv/sendungen-a-z?buchstabe=B",True),
                        TreeNode("1.3","C",self.rootLink+"/tv/sendungen-a-z?buchstabe=C",True),
                        TreeNode("1.4","D",self.rootLink+"/tv/sendungen-a-z?buchstabe=D",True),
                        TreeNode("1.5","E",self.rootLink+"/tv/sendungen-a-z?buchstabe=E",True),
                        TreeNode("1.6","F",self.rootLink+"/tv/sendungen-a-z?buchstabe=F",True),
                        TreeNode("1.7","G",self.rootLink+"/tv/sendungen-a-z?buchstabe=G",True),
                        TreeNode("1.8","H",self.rootLink+"/tv/sendungen-a-z?buchstabe=H",True),
                        TreeNode("1.9","I",self.rootLink+"/tv/sendungen-a-z?buchstabe=I",True),
                        TreeNode("1.10","J",self.rootLink+"/tv/sendungen-a-z?buchstabe=J",True),
                        TreeNode("1.11","K",self.rootLink+"/tv/sendungen-a-z?buchstabe=K",True),
                        TreeNode("1.12","L",self.rootLink+"/tv/sendungen-a-z?buchstabe=L",True),
                        TreeNode("1.13","M",self.rootLink+"/tv/sendungen-a-z?buchstabe=M",True),
                        TreeNode("1.14","N",self.rootLink+"/tv/sendungen-a-z?buchstabe=N",True),
                        TreeNode("1.15","O",self.rootLink+"/tv/sendungen-a-z?buchstabe=O",True),
                        TreeNode("1.16","P",self.rootLink+"/tv/sendungen-a-z?buchstabe=P",True),
                        TreeNode("1.17","Q",self.rootLink+"/tv/sendungen-a-z?buchstabe=Q",True),
                        TreeNode("1.18","R",self.rootLink+"/tv/sendungen-a-z?buchstabe=R",True),
                        TreeNode("1.19","S",self.rootLink+"/tv/sendungen-a-z?buchstabe=S",True),
                        TreeNode("1.20","T",self.rootLink+"/tv/sendungen-a-z?buchstabe=T",True),
                        TreeNode("1.21","U",self.rootLink+"/tv/sendungen-a-z?buchstabe=U",True),
                        TreeNode("1.22","V",self.rootLink+"/tv/sendungen-a-z?buchstabe=V",True),
                        TreeNode("1.23","W",self.rootLink+"/tv/sendungen-a-z?buchstabe=W",True),
                        TreeNode("1.24","X",self.rootLink+"/tv/sendungen-a-z?buchstabe=X",True),
                        TreeNode("1.25","Y",self.rootLink+"/tv/sendungen-a-z?buchstabe=Y",True),
                        TreeNode("1.26","Z",self.rootLink+"/tv/sendungen-a-z?buchstabe=Z",True),
                        )),
                      TreeNode("2","Ausgewählte Dokus".decode("utf-8"),self.rootLink+"/tv/Ausgew%C3%A4hlte-Dokus/mehr?documentId=33649086",True),
                      TreeNode("3","Ausgewählte Filme".decode("utf-8"),self.rootLink+"/tv/Ausgew%C3%A4hlte-Filme/mehr?documentId=33649088",True),
                      TreeNode("4","Alle Reportagen und Dokus",self.rootLink+"/tv/dokus",True),
                      TreeNode("5","Alle Filme",self.rootLink+"/tv/filme",True),
                      TreeNode("6","Nachrichten",self.rootLink+"/tv/nachrichten",True),
                      TreeNode("7","Themen",self.rootLink+"/tv/Themen/mehr?documentId=21301810",True),
                      TreeNode("8","Rubriken","",False,(
                        TreeNode("8.0","Kinder",self.rootLink+"/tv/Kinder/Tipps?documentId=21282542",True),
                        TreeNode("8.1","Unterhaltung & Comedy",self.rootLink+"/tv/unterhaltung",True),
                        TreeNode("8.2","Kultur",self.rootLink+"/tv/kultur",True),
                        TreeNode("8.3","Wissen",self.rootLink+"/tv/wissen",True),
                        TreeNode("8.4","Politik",self.rootLink+"/tv/politik",True),
                        TreeNode("8.5","Ratgeber",self.rootLink+"/tv/ratgeber",True),
                        TreeNode("8.6","Sport",self.rootLink+"/tv/sport",True),
                        TreeNode("8.7","Reise",self.rootLink+"/tv/reise",True),
                        )),
                      )
    self.configLink = self.rootLink+"/play/media/%s?devicetype=pc&feature=flash"
    self.regex_VideoPageLink = re.compile("<a href=\".*Video\?.*?documentId=(\d+).*?\" class=\"textLink\">\s+?<p class=\"dachzeile\">(.*?)<\/p>\s+?<h4 class=\"headline\">(.*?)<\/h4>\s+?<p class=\"subtitle\">(?:(\d+.\d+.\d+) \| )?(\d*) Min.")
    self.regex_CategoryPageLink = re.compile("<a href=\"(.*(?:Sendung|Thema)\?.*?documentId=\d+.*?)\" class=\"textLink\">(?:.|\n)+?<h4 class=\"headline\">(.*?)<\/h4>")
    self.pageSelectString = "&mcontent%s=page.%s"
    self.regex_DetermineSelectedPage = re.compile("&mcontents{0,1}=page.(\d+)");

    self.regex_videoLinks = re.compile("\"_quality\":(\d).*?\"_stream\":\[?\"(.*?)\"");
    self.regex_pictureLink = re.compile("_previewImage\":\"(.*?)\"");


    self.regex_Date = re.compile("\\d{2}\\.\\d{2}\\.\\d{2}");


    self.replace_html = re.compile("<.*?>");
    
    self.playerLink = self.rootLink+"/ard/player/%s"
    self.regex_ExtractJson = re.compile("__APOLLO_STATE__ = ({.*});");
    self.tumbnail_size = "600";

  @classmethod
  def name(self):
    return "ARD";
  def isSearchable(self):
    return False;
  def extractJsonFromPage(self,link):
    pageContent = self.loadPage(link).decode('UTF-8');
    content = self.regex_ExtractJson.search(pageContent).group(1);
    pageContent = BeautifulSoup(content,"html.parser");
    jsonContent= pageContent.prettify(formatter=None);
    return json.loads(jsonContent);

  def buildPageMenu(self, link, initCount, subLink = False):
    self.gui.log("Build Page Menu: %s SubLink: %d"%(link,subLink));
    jsonContent = self.extractJsonFromPage(link);
    for key in jsonContent:
      if(key.startswith("Teaser:")):
        self.doSomeShit(jsonContent[key],jsonContent);
    return 0;

  def doSomeShit(self, teaserContent, jsonContent):
    title = teaserContent["shortTitle"];
    subTitle = None;
    picture = self.getPictureLink(teaserContent["images"],jsonContent);
    videoLinks = self.getVideoLinks(teaserContent["links"],jsonContent);
    date = None;
    duration = None;
    nodeCount = 0;
    self.gui.buildVideoLink(DisplayObject(title, subTitle,picture,"",videoLinks,"JsonLink",date,duration),self,nodeCount);

  def getVideoLinks(self, linkSource, jsonContent):
    #WTF geht es noch sinnloser?
    key = linkSource["id"]
    key = jsonContent[key]["target"]["id"];
    return self.playerLink%jsonContent[key]["id"];

  def getPictureLink(self, pictureSource, jsonContent):
    if(pictureSource is not None):
      key=pictureSource["id"];
      pictureConfig = jsonContent[key];
      for key in pictureConfig:
        if(key.startswith("aspect") and pictureConfig[key] is not None):
          key = pictureConfig[key]["id"];
          return jsonContent[key]["src"].replace("{width}",self.tumbnail_size);
    return None;

  def playVideoFromJsonLink(self,link):
    #WTF OHHHHHHHHH JAAAAAA - es geht noch sinnloser...
    jsonContent = self.extractJsonFromPage(link);

    videoLinks = {}
    for key in jsonContent:
      if("_mediaStreamArray." in key):
        streamConfig = jsonContent[key];
        if(streamConfig["_quality"] == "auto"):
          quality = 3;
        else:
          quality = int(streamConfig["_quality"]);
        link = streamConfig["_stream"]["json"][0];
        if(not link.startswith("http")):
          link = "https:"+link;
        self.gui.log("VideoLink: "+link);
        videoLinks[quality] = SimpleLink(link,-1);

    self.gui.play(videoLinks);
