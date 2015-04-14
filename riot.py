__author__ = 'Chris'
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from socket import timeout
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Riot:
    api_key = "28b92f8a-f01b-4e6e-825f-5feed275ad7a"

    def __init__(self, api_key):
        self.api_key = api_key

    def getSummonerByName(self, name):
        response = self.request("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" + name + "?api_key=" + self.api_key)
        json = response.read().decode('utf-8', errors='ignore')
        summoner = json.loads(json)
        return summoner

    def getMatchHistory(self, summonerId):
        response = self.request("https://na.api.pvp.net/api/lol/na/v2.2/matchhistory/" + summonerId + "?api_key=" + self.api_key)
        json = response.read().decode('utf-8', errors='ignore')
        match = json.loads(json)
        return match

    def request(self, url):
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

        match = re.search("content-type:\s*([\w/]+);", str(headers), re.IGNORECASE)
        try:
            return match.group(1)
        except:
            return None


    def run(self):
        summoner = self.getSummonerByName("chrispychips5")
        summonerId = summoner["id"]
        matchHistory = self.getMatchHistory(summonerId)
        for match in matchHistory:


