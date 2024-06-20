import pickle
from dataclasses import dataclass, field
import typing
from typing import List


@dataclass
class Parser:

    def ReadFile(self, filename):
        with open(filename, 'rb') as f:
            log=pickle.load(f)
            return log

    @dataclass
    class Player:
        numPlayer: int
        numInTeam: int
        teamColorName: str = ''
        type: str = ''
        event: List[int] = field(default_factory=list)
        timeGameEvent: List[float] = field(default_factory=list)
        paramEvent: List[str] = field(default_factory=list)
        timeGameCoordinates: List[float] = field(default_factory=list)
        coordinates: List[list] = field(default_factory=list)
        yaw: List[float] = field(default_factory=list)
        RC: List[list] = field(default_factory=list)

    @dataclass
    class Polygon():
        numPolygon: int
        paramEvent: List[str] = field(default_factory=list)
        timeGame: List[int] = field(default_factory=list)
        type: str = field(default_factory=str)
        event: List[int] = field(default_factory=list)

    @dataclass
    class Server:
        timeGame: List[int] = field(default_factory=list)
        event: List[int] = field(default_factory=list)
        paramEvent: typing.Union[dict, None] = None

    server=Server()
    descriptionPolygons: dict =field(default_factory=dict)
    descriptionPlayers: dict =field(default_factory=dict)
    Players: List[Player] = field(default_factory=list)
    Polygons: List[Polygon] = field(default_factory=list)

    def GetDescriptionPlayers(self, log):
        numPlayers=[]
        teamColorName=[]
        numInTeam=[]
        type=[]
        for i in log['gameDescription']['players']:
            numPlayers.append(i.get('numPlayer'))
            teamColorName.append(i.get('teamColorName'))
            numInTeam.append(i.get('numInTeam'))
            type.append(i.get('type'))
        self.descriptionPlayers.update([('numPlayer', numPlayers), ('teamColorName', teamColorName), ('numInTeam', numInTeam), ('type', type)])
        return self.descriptionPlayers

    def GetDescriptionPolygon(self, log):
        numPolygon=[]
        typePolygon=[]
        for i in log['gameDescription']['polygon']:
            numPolygon.append(i.get('numPolygon'))
            typePolygon.append(i.get('type'))
        self.descriptionPolygons.update([('numPolygon', numPolygon), ('type', typePolygon)])
        return self.descriptionPolygons

    def GetServer(self, log):
        timeGame = []
        event = []
        paramEvent = []
        for i in log['serverLog']['baseEventLog']:
            timeGame.append(i.get('timeGame'))
            event.append(i.get('event'))
            paramEvent.append(i.get('paramEvent'))
        self.server.timeGame=timeGame
        self.server.event=event
        self.server.paramEvent=paramEvent
        return self.server

    def GetPlayersEvent(self, log):
        playersEvent=dict()
        timeGame=[]
        numPlayer=[]
        event=[]
        paramEvent=[]
        for i in log['playersLog']['baseEventLog']:
            timeGame.append(i.get('timeGame'))
            numPlayer.append(i.get('numPlayer'))
            event.append(i.get('event'))
            paramEvent.append(i.get('paramEvent'))
        playersEvent.update([('timeGame', timeGame), ('numPlayer', numPlayer), ('event', event), ('paramEvent', paramEvent)])
        return playersEvent

    def GetPlayersData(self, log):
        DataPlayers=dict()
        timeGame=[]
        numPlayer=[]
        x=[]
        y=[]
        z=[]
        yaw=[]
        RC1=[]
        RC2=[]
        RC3=[]
        RC4=[]
        for i in log['playersLog']['dataPlayer']:
            timeGame.append(i.get('timeGame'))
            numPlayer.append(i.get('numPlayer'))
            x.append(i.get('x'))
            y.append(i.get('y'))
            z.append(i.get('z'))
            yaw.append(i.get('yaw'))
            RC1.append(i.get('RC1'))
            RC2.append(i.get('RC2'))
            RC3.append(i.get('RC3'))
            RC4.append(i.get('RC4'))
        DataPlayers.update([('timeGame', timeGame), ('numPlayer', numPlayer), ('x', x), ('y', y), ('z', z), ('yaw', yaw), ('RC1', RC1), ('RC2', RC2), ('RC3', RC3), ('RC4', RC4)])
        return DataPlayers

    def SetPlayers(self, events, dataPlayers):
        self.Players = [self.Player(numPlayer=i,
                                    teamColorName=self.descriptionPlayers['teamColorName'][i],
                                    numInTeam=self.descriptionPlayers['numInTeam'][i],
                                    type=self.descriptionPlayers['type'][i])
                        for i in self.descriptionPlayers['numPlayer']]
        for i in range(len(events['event'])):
            self.Players[events['numPlayer'][i]].timeGameEvent.append(events['timeGame'][i])
            self.Players[events['numPlayer'][i]].event.append(events['event'][i])
            self.Players[events['numPlayer'][i]].paramEvent.append(events['paramEvent'][i])
        for i in range(len(dataPlayers['numPlayer'])):
            self.Players[dataPlayers['numPlayer'][i]].coordinates.append([dataPlayers['x'][i], dataPlayers['y'][i], dataPlayers['z'][i]])
            self.Players[dataPlayers['numPlayer'][i]].RC.append([dataPlayers['RC1'][i], dataPlayers['RC2'][i], dataPlayers['RC3'][i], dataPlayers['RC4'][i]])
            self.Players[dataPlayers['numPlayer'][i]].timeGameCoordinates.append(dataPlayers['timeGame'][i])
            self.Players[dataPlayers['numPlayer'][i]].yaw.append(dataPlayers['yaw'][i])
        return self.Players

    def GetPolygonLog(self, log):
        PolygonEvents=dict()
        timeGame=[]
        numPolygon=[]
        event=[]
        paramEvent=[]
        for i in log['polygonLog']['baseEventLog']:
            timeGame.append(i.get('timeGame'))
            numPolygon.append(i.get('numPolygon'))
            event.append(i.get('event'))
            paramEvent.append(i.get('paramEvent'))
        PolygonEvents.update([('timeGame', timeGame), ('numPolygon', numPolygon), ('event', event), ('paramEvent', paramEvent)])
        return PolygonEvents

    def SetPolygonClass(self, events):
        for i in range(len(self.descriptionPolygons.get('numPolygon'))):
            self.Polygons.append(self.Polygon(numPolygon=self.descriptionPolygons.get('numPolygon')[i],
                                              type=self.descriptionPolygons.get('type')[i]))
        for i in range(len(events.get('event'))):
            self.Polygons[events.get('numPolygon')[i]].timeGame.append(events.get('timeGame')[i])
            self.Polygons[events.get('numPolygon')[i]].event.append(events.get('event')[i])
            self.Polygons[events.get('numPolygon')[i]].paramEvent.append(events.get('paramEvent')[i])
        return self.Polygons
