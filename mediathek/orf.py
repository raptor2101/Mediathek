# -*- coding: utf-8 -*-
# -------------LicenseHeader--------------
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
import re,time,urllib,json;
from xml.dom import Node;
from xml.dom import minidom;
from mediathek import *
from bs4 import BeautifulSoup;

class ORFMediathek(Mediathek):
  def __init__(self, simpleXbmcGui):

    self.rootLink = "http://tvthek.orf.at"
    self.gui = simpleXbmcGui;
    self.menuTree = [];
    self.menuTree.append(TreeNode("0","Startseite","http://tvthek.orf.at/",True));



    self.menuTree.append(TreeNode("1","Sendungen","http://tvthek.orf.at/profiles/a-z",True));

    videoLinkPage = "/programs/.*"
    imageLink = "http://tvthek.orf.at/assets/.*?.jpeg"


    self.regex_extractVideoPageLink = re.compile(videoLinkPage+"?\"");
    self.regex_extractImageLink = re.compile(imageLink);
    self.regex_extractTitle = re.compile("<strong>.*<span");
    self.regex_extractVideoLink = re.compile("/programs/.*.asx");
    self.regex_extractVideoObject = re.compile("<a href=\""+videoLinkPage+"\" title=\".*\">\\s*<span class=\"spcr\">\\s*<img src=\""+imageLink+"\" title=\".*\" alt=\".*\" />\\s*<span class=\".*\"></span>\\s*<strong>.*<span class=\"nowrap duration\">.*</span></strong>\\s*<span class=\"desc\">.*</span>\\s*</span>\\s*</a>");

    self.regex_extractSearchObject = re.compile("<li class=\"clearfix\">\\s*<a href=\".*\" title=\".*\" class=\".*\"><img src=\".*\" alt=\".*\" /><span class=\"btn_play\">.*</span></a>\\s*<p>.*</p>\\s*<h4><a href=\".*\" title=\".*\">.*</a></h4>\\s*<p><a href=\".*\" title=\".*\"></a></p>\\s*</li>");

    self.regex_extractProgrammLink = re.compile("/programs/.*?\"");
    self.regex_extractProgrammTitle = re.compile("title=\".*?\"");
    self.regex_extractProgrammPicture = re.compile("/binaries/asset/segments/\\d*/image1");

    self.regex_extractFlashVars = re.compile("ORF.flashXML = '.*?'");
    self.regex_extractHiddenDate = re.compile("\d{4}-\d{2}-\d{2}");
    self.regex_extractXML = re.compile("%3C.*%3E");

    self.replace_html = re.compile("<.*?>");
    self.searchLink = "http://tvthek.orf.at/search?q="




    self.regex_extractProfileSites = re.compile("<a class=\"item_inner clearfix\"\s*?href=\"(http://tvthek.orf.at/profile/.*?/\d+)\".*src=\"(http://api-tvthek.orf.at/uploads/media/profiles/.*?_profiles_list.jpeg)\"(.|\s)*?<h4 class=\"item_title\">(.*?)</h4>");
    self.regex_extractTopicSites = re.compile("<a href=\"(http://tvthek.orf.at/topic/.*?/\d+)\"\s*?title=\"(.*?)\"\s*?class=\"more");
    self.regex_extractVideoPages = re.compile("<a href=\"(http://tvthek.orf.at/.*?/\d+)\"");
    self.regex_extractJson = re.compile("data-jsb=\"({&quot;videoplayer_id&quot;.*})\">");

  @classmethod
  def name(self):
    return "ORF";

  def isSearchable(self):
    return False;

  def createVideoLink(self,title,image,videoPageLink,elementCount):
    videoPage = self.loadPage(self.rootLink+videoPageLink);

    videoLink = self.regex_extractVideoLink.search(videoPage);
    if(videoLink == None):
      return;

    simpleLink = SimpleLink(self.rootLink+videoLink.group(), 0);
    videoLink = {0:simpleLink};
    counter = 0
    playlist = self.loadPage(simpleLink.basePath);
    for line in playlist:
      counter+=1;

    if(counter == 1):
      self.gui.buildVideoLink(DisplayObject(title,"",image,"",videoLink, True, time.gmtime()),self,elementCount);
    else:
      self.gui.buildVideoLink(DisplayObject(title,"",image,"",videoLink, "PlayList", time.gmtime()),self,elementCount);

  def searchVideo(self, searchText):
    link = self.searchLink = "http://tvthek.orf.at/search?q="+searchText;
    mainPage = self.loadPage(link);
    result = self.regex_extractSearchObject.findall(mainPage);
    for searchObject in result:
      videoLink = self.regex_extractProgrammLink.search(searchObject).group().replace("\"","");
      title = self.regex_extractProgrammTitle.search(searchObject).group().replace("title=\"","").replace("\"","");
      title = title.decode("UTF-8");
      pictureLink = self.regex_extractProgrammPicture.search(searchObject).group();

      print videoLink;

      self.createVideoLink(title,pictureLink,videoLink, len(result));

  def extractLinksFromFlashXml(self, flashXml, date, elementCount):
    print flashXml.toprettyxml().encode('UTF-8');
    playlistNode = flashXml.getElementsByTagName("Playlist")[0];
    linkNode=flashXml.getElementsByTagName("AsxUrl")[0];
    link=linkNode.firstChild.data;
    asxLink = SimpleLink(self.rootLink+link,0);
    videoLink = {0:asxLink};
    for videoItem in playlistNode.getElementsByTagName("Items")[0].childNodes:
      if(videoItem.nodeType == Node.ELEMENT_NODE):
        titleNode=videoItem.getElementsByTagName("Title")[0];

        descriptionNode=videoItem.getElementsByTagName("Description")[0];
        title=titleNode.firstChild.data;

        stringArray = link.split("mp4:");

        try:
          description=descriptionNode.firstChild.data;
        except:
          description="";
        self.gui.buildVideoLink(DisplayObject(title,"","",description,videoLink, True, date),self,elementCount);

  def extractVideoLinks(self,videoPageLinks,elementCount):
    for videoPageLink in videoPageLinks:

      videoPage = self.loadPage(videoPageLink.group(1));
      jsonContent = self.regex_extractJson.search(videoPage);
      if(jsonContent == None):
        return;
      jsonContent = jsonContent.group(1);
      jsonContent = BeautifulSoup(jsonContent);
      jsonContent = json.loads(jsonContent.prettify(formatter=None).encode('UTF-8'));
      jsonContent = jsonContent["selected_video"];
      title = jsonContent["title"];
      pictureLink = jsonContent["preview_image_url"];

      videoLinks={};

      for source in jsonContent["sources"]:
        if(source["protocol"] == "http"):
          quality = source["quality"];
          url = source["src"];
          if(quality == "Q1A"):
            videoLinks[0] = SimpleLink(url, -1);
          if(quality == "Q4A"):
            videoLinks[1] = SimpleLink(url, -1);
          if(quality == "Q6A"):
            videoLinks[2] = SimpleLink(url, -1);
          if(quality == "Q8C"):
            videoLinks[3] = SimpleLink(url, -1);
      if("title_separator" in jsonContent):
        titleSeperator = jsonContent["title_separator"];
        titleArray = title.split(titleSeperator);
        try:
          title = titleArray[0];
          subTitle = titleArray[1];
        except IndexError:
          subTitle = "";
        self.gui.buildVideoLink(DisplayObject(title,subTitle,pictureLink,"",videoLinks, True, None),self,0);
      else:
        self.gui.buildVideoLink(DisplayObject(title,None,pictureLink,"",videoLinks, True, None),self,0);

  def buildPageMenu(self, link, initCount):
    mainPage = self.loadPage(link);
    for topic in self.regex_extractTopicSites.finditer(mainPage):
      self.gui.buildVideoLink(DisplayObject(topic.group(2),None,None,"",topic.group(1), False, None),self,0);

    for profile in self.regex_extractProfileSites.finditer(mainPage):
      self.gui.buildVideoLink(DisplayObject(profile.group(4),None,profile.group(2),"",profile.group(1), False, None),self,0);
      
      



    videoPageLinks = self.regex_extractVideoPages.finditer(mainPage);

    self.extractVideoLinks(videoPageLinks,0);

