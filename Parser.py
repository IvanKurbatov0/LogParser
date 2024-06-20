import pickle
from dataclasses import dataclass, field
import typing
from typing import List


def read(filename):
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


descriptionPlayers=dict()

def GetGameDescriptionPlayers(log):
    numPlayers=[]
    teamColorName=[]
    numInTeam=[]
    type=[]
    for i in log['gameDescription']['players']:
        numPlayers.append(i.get('numPlayer'))
        teamColorName.append(i.get('teamColorName'))
        numInTeam.append(i.get('numInTeam'))
        type.append(i.get('type'))
    descriptionPlayers.update([('numPlayer', numPlayers), ('teamColorName', teamColorName), ('numInTeam', numInTeam), ('type', type)])
    return descriptionPlayers


Players=[]
descriptionPolygons=dict()


def GetGameDescriptionPolygon(log):
    numPolygon=[]
    typePolygon=[]
    for i in log['gameDescription']['polygon']:
        numPolygon.append(i.get('numPolygon'))
        typePolygon.append(i.get('type'))
    descriptionPolygons.update([('numPolygon', numPolygon), ('type', typePolygon)])
    return descriptionPolygons


Polygons=[]
ServerEvent = dict()


def GetServerEvent(log):
    timeGame=[]
    event=[]
    paramEvent=[]
    for i in log['serverLog']['baseEventLog']:
        timeGame.append(i.get('timeGame'))
        event.append(i.get('event'))
        paramEvent.append(i.get('paramEvent'))
    ServerEvent.update([('timeGame', timeGame), ('event', event), ('paramEvent', paramEvent)])
    return ServerEvent


server=Server()


def SetServerClass(events):
    #global server
    server = Server(timeGame=events.get('timeGame'), event=events.get('event'), paramEvent=events.get('paramEvent'))


def GetPlayersEvent(log):
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


def GetDataPlayers(log):
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


def SetPlayerClass(Events, Data):
    global Players
    Players = [Player(numPlayer=i,
                      teamColorName=descriptionPlayers['teamColorName'][i],
                      numInTeam=descriptionPlayers['numInTeam'][i],
                      type=descriptionPlayers['type'][i])
               for i in descriptionPlayers['numPlayer']]
    for i in range(len(Events['event'])):
        Players[Events['numPlayer'][i]].timeGameEvent.append(Events['timeGame'][i])
        Players[Events['numPlayer'][i]].event.append(Events['event'][i])
        Players[Events['numPlayer'][i]].paramEvent.append(Events['paramEvent'][i])
    for i in range(len(Data['numPlayer'])):
        Players[Data['numPlayer'][i]].coordinates.append([Data['x'][i], Data['y'][i], Data['z'][i]])
        Players[Data['numPlayer'][i]].RC.append([Data['RC1'][i], Data['RC2'][i], Data['RC3'][i], Data['RC4'][i]])
        Players[Data['numPlayer'][i]].timeGameCoordinates.append(Data['timeGame'][i])
        Players[Data['numPlayer'][i]].yaw.append(Data['yaw'][i])

PolygonEvents = dict()


def GetPolygonLog(log):
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


def SetPolygonClass(Events):
    for i in range(len(descriptionPolygons.get('numPolygon'))):
        Polygons.append(Polygon(numPolygon=descriptionPolygons.get('numPolygon')[i], type=descriptionPolygons.get('type')[i]))
    for i in range(len(Events.get('event'))):
        Polygons[Events.get('numPolygon')[i]].timeGame.append(Events.get('timeGame')[i])
        Polygons[Events.get('numPolygon')[i]].event.append(Events.get('event')[i])
        Polygons[Events.get('numPolygon')[i]].paramEvent.append(Events.get('paramEvent')[i])
