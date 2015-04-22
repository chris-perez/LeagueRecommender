__author__ = 'Chris'
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from socket import timeout
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import time
import json

Base = declarative_base()

class Riot:
    api_key = "28b92f8a-f01b-4e6e-825f-5feed275ad7a"

    def __init__(self, api_key="28b92f8a-f01b-4e6e-825f-5feed275ad7a"):
        self.api_key = api_key

    def getSummonerByName(self, name):
        response = self.request("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + name + "?api_key=" + self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        summoner = json.loads(json_as_str)
        return summoner

    def getSummonerById(self, summonerId):
        response = self.request("https://na.api.pvp.net/api/lol/na/v1.4/summoner/" + summonerId + "?api_key=" + self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        summoner = json.loads(json_as_str)
        return summoner

    def getMatch(self, matchId):
        response = self.request("https://na.api.pvp.net//api/lol/na/v2.2/match/" + str(matchId) + "?api_key=" + self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        match = json.loads(json_as_str)
        return match

    def getMatchHistory(self, summonerId):
        response = self.request("https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/" + str(summonerId) + "/recent?api_key=" + self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        match = json.loads(json_as_str)
        return match

    def getRankedMatchHistory(self, summonerId):
        response = self.request("https://na.api.pvp.net/api/lol/na/v2.2/matchhistory/" + str(summonerId) + "?api_key=" + self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        match = json.loads(json_as_str)
        return match

    def getChampionInfo(self):
        response = self.request("https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?champData=info,stats,tags&api_key="+self.api_key)
        json_as_str = response.read().decode('utf-8', errors='ignore')
        champs = json.loads(json_as_str)
        return champs

    def request(self, url):
        time.sleep(1.2)
        req = Request(url, None, {'User-agent': 'Firefox/3.05'})
        try:
            return urlopen(req)
        except (HTTPError, URLError) as error:
            print('ERROR:  Could not retrieve', url, 'because', error)
            return -1
        except timeout:
            print('ERROR:  Socket timed out - URL: %s', url)
            return -1

    # Get the doctype from the headers
    def doctype(self, headers):

        match = headers.search("content-type:\s*([\w/]+);", str(headers), re.IGNORECASE)
        try:
            return match.group(1)
        except:
            return None