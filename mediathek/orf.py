# -*- coding: utf-8 -*-
import re,time
from mediathek import *

class ORFMediathek(Mediathek):
  def __init__(self, simpleXbmcGui):
    self.gui = simpleXbmcGui;
    self.menuTree = (
      TreeNode("0","Startseite","http://tvthek.orf.at/",True),
      TreeNode("1","Sendungen","",False,
        (
          TreeNode("1.0",u"Bundesländer","",False,
            (
              TreeNode("1.0.0",u"Burgenland heute","http://tvthek.orf.at/programs/70021-Burgenland-heute",True),
              TreeNode("1.0.1",u"Kärnten heute","http://tvthek.orf.at/programs/70022-Kaernten-heute",True),
              TreeNode("1.0.2",u"Niederösterreich heute","http://tvthek.orf.at/programs/70017-Niederoesterreich-heute",True),
              TreeNode("1.0.3",u"Oberoesterreich heute","http://tvthek.orf.at/programs/70016-Oberoesterreich-heute",True),
              TreeNode("1.0.4",u"Salzburg heute","http://tvthek.orf.at/programs/70019-Salzburg-heute",True),
              TreeNode("1.0.5",u"Steiermark heute","http://tvthek.orf.at/programs/70020-Steiermark-heute",True),
              TreeNode("1.0.6",u"Tirol heute","http://tvthek.orf.at/programs/70023-Tirol-heute",True),
              TreeNode("1.0.6",u"Vorarlberg heute","http://tvthek.orf.at/programs/70024-Vorarlberg-heute",True),
              TreeNode("1.0.6",u"Wien heute","http://tvthek.orf.at/programs/70018-Wien-heute",True),
            )
          ),
          TreeNode("1.1",u"Dokumentationen","",False,
            (
              TreeNode("1.1.0",u"Erlebnis Österreich","http://tvthek.orf.at/programs/1200-Erlebnis-Oesterreich",True),
              TreeNode("1.1.1",u"Menschen & Mächte","http://tvthek.orf.at/programs/170407-Menschen---Maechte",True),
              TreeNode("1.1.2",u"Universum","http://tvthek.orf.at/programs/35429-Universum",True),
            )
          ),
          TreeNode("1.2",u"Information","",False,
            (
              TreeNode("1.2.0",u"Club 2","http://tvthek.orf.at/programs/1283-Club-2",True),
              TreeNode("1.2.1",u"Heute in Österreich","http://tvthek.orf.at/programs/1257-Heute-in-Oesterreich",True),
              TreeNode("1.2.2",u"Hohes Haus","http://tvthek.orf.at/programs/1264-Hohes-Haus",True),
              TreeNode("1.2.3",u"Im Zentrum","http://tvthek.orf.at/programs/1279-Im-Zentrum",True),
              TreeNode("1.2.4",u"Österreich-Bild","http://tvthek.orf.at/programs/1296-Oesterreich-Bild",True),
              TreeNode("1.2.5",u"Pressestunde","http://tvthek.orf.at/programs/1273-Pressestunde",True),
              TreeNode("1.2.6",u"Runder Tisch","http://tvthek.orf.at/programs/70010-Runder-Tisch",True),
              TreeNode("1.2.7",u"Südtirol heute","http://tvthek.orf.at/programs/1277675-Suedtirol-heute",True),
              TreeNode("1.2.8",u"Wetter","http://tvthek.orf.at/programs/1250-Wetter",True),
              TreeNode("1.2.9",u"Wetter (ÖGS)","http://tvthek.orf.at/programs/1786041-Wetter--OeGS-",True),
              TreeNode("1.2.10",u"Wetter ZiB 20","http://tvthek.orf.at/programs/972117-Wetter-ZIB-20",True),
              TreeNode("1.2.11",u"ZiB 9","http://tvthek.orf.at/programs/71256-ZiB-9",True),
              TreeNode("1.2.12",u"ZiB 11","http://tvthek.orf.at/programs/71276-ZiB-11",True),
              TreeNode("1.2.13",u"ZiB 13","http://tvthek.orf.at/programs/71280-ZiB-13",True),
              TreeNode("1.2.14",u"ZiB 17","http://tvthek.orf.at/programs/71284-ZiB-17",True),
              TreeNode("1.2.15",u"Zeit im Bild","http://tvthek.orf.at/programs/1203-Zeit-im-Bild",True),
              TreeNode("1.2.16",u"Zeit im Bild (ÖGS)","http://tvthek.orf.at/programs/145302-Zeit-im-Bild--OeGS-",True),
              TreeNode("1.2.17",u"ZiB 20","http://tvthek.orf.at/programs/1218-ZiB-20",True),
              TreeNode("1.2.18",u"ZiB 2","http://tvthek.orf.at/programs/1211-ZiB-2",True),
              TreeNode("1.2.19",u"Spät ZiB","http://tvthek.orf.at/programs/79134-Spaet-ZiB",True),
              TreeNode("1.2.20",u"ZiB 24","http://tvthek.orf.at/programs/1225-ZiB-24",True),
              TreeNode("1.2.21",u"ZiB Flash","http://tvthek.orf.at/programs/1232-ZiB-Flash",True),
            )
          ),
          TreeNode("1.3",u"Magazine","",False,
            (
              TreeNode("1.3.0",u"Bewusst gesund - das Magazin","http://tvthek.orf.at/programs/1714463-Bewusst-gesund---das-Magazin",True),
              TreeNode("1.3.0",u"Bürgeranwalt","http://tvthek.orf.at/programs/1339-Buergeranwalt",True),
              TreeNode("1.3.0",u"Bürgerforum","http://tvthek.orf.at/programs/1343-Buergerforum",True),
              TreeNode("1.3.0",u"Konkret","http://tvthek.orf.at/programs/1336-Konkret",True),
              TreeNode("1.3.0",u"Land und Leute","http://tvthek.orf.at/programs/1369-Land-und-Leute",True),
              TreeNode("1.3.0",u"Stöckl am Samstag","http://tvthek.orf.at/programs/1651-Stoeckl-am-Samstag",True),
              TreeNode("1.3.0",u"Thema","http://tvthek.orf.at/programs/1319-Thema",True),
              TreeNode("1.3.0",u"Vera exklusiv","http://tvthek.orf.at/programs/35440-Vera-exklusiv",True),
              TreeNode("1.3.0",u"Weltjournal","http://tvthek.orf.at/programs/1328-Weltjournal",True),
              TreeNode("1.3.0",u"Winterzeit","http://tvthek.orf.at/programs/1003023-Winterzeit",True),
            )
          ),
        )
      )
    );
      
    self.rootLink = "http://tvthek.orf.at"
    
    videoLinkPage = "/programs/.*"
    imageLink = "http://tvthek.orf.at/assets/.*?.jpeg"
    

    self.regex_extractVideoPageLink = re.compile(videoLinkPage+"?\"");
    self.regex_extractImageLink = re.compile(imageLink);
    self.regex_extractTitle = re.compile("<strong>.*<span");
    self.regex_extractVideoLink = re.compile("/programs/.*.asx");
    self.regex_extractVideoObject = re.compile("<a href=\""+videoLinkPage+"\" title=\".*\">\\s*<span class=\"spcr\">\\s*<img src=\""+imageLink+"\" title=\".*\" alt=\".*\" />\\s*<span class=\".*\"></span>\\s*<strong>.*<span class=\"nowrap duration\">.*</span></strong>\\s*<span class=\"desc\">.*</span>\\s*</span>\\s*</a>");
    
    self.replace_html = re.compile("<.*?>");
    
  @classmethod
  def name(self):
    return "ORF";
    
  def isSearchable(self):
    return False;
    
  def buildPageMenu(self, link):
    mainPage = self.loadPage(link);
    
    for linkObject in self.regex_extractVideoObject.findall(mainPage):
      
      videoPageLink = self.regex_extractVideoPageLink.search(linkObject).group().replace("\"","");
      videoPage = self.loadPage(self.rootLink+videoPageLink);
      simpleLink = SimpleLink(self.rootLink+self.regex_extractVideoLink.search(videoPage).group(), 0);
      videoLink = {0:simpleLink};
      
      
      image = self.regex_extractImageLink.search(linkObject).group();
      title = self.regex_extractTitle.search(linkObject).group().decode('UTF8');
      
      title = self.replace_html.sub("", title);
      title = title.replace(" <span","");
      print image
      #self.gui.buildVideoLink(DisplayObject(titles[0],titles[1],pictureLink,"",videoPageLink,False),self);
      self.gui.buildVideoLink(DisplayObject(title,"",image,"",videoLink, True, time.gmtime()),self);