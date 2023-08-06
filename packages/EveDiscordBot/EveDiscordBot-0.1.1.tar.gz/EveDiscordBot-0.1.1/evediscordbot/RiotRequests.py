from riotwatcher import RiotWatcher


""" Riotwatcher's parameter is your riot API key"""
watcher = RiotWatcher('')

class RiotAPI:

    def __new__(cls,summonername,region):
        return super(RiotAPI,cls).__new__(cls)

    def __init__(self,summonername, region):
        self.region = region
        self.summonername = summonername
        self.me = self.getsummonerid()
        self.mastery = self.getmastery()
        self.ranking = self.getranking()








    def getsummonerid(self):
        return (watcher.summoner.by_name(self.region,self.summonername))['id']

    def getmastery(self):
        """gets champion mastery with EVELYNN SPECIFICALLY"""
        mastery = watcher.champion_mastery.by_summoner_by_champion(self.region,self.me,28)
        return mastery['championPoints']


    def getranking(self):
        """gets Solo queue ranking """
        ranking = watcher.league.positions_by_summoner(self.region,self.me)
        return (ranking[0]['tier'] + " " + ranking[0]['rank'])



""""test cases"""

"""RiotAPI('hi im eve','na1')

RiotAPI('confuss','na1')

RiotAPI('rarie','na1')"""