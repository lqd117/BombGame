from operat import Operat
import select
import socket


class GameServer(Operat):
    def __init__(self, HOST: str, USER: str, PWD: str, DB: str, port=20000):
        super(GameServer, self).__init__(HOST, USER, PWD, DB)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener.bind(("127.0.0.1", port))
        self.read_list = [self.listener]
        self.write_list = []
        self.id_ip_port = {}  # 记录每个id可以接受广播的ip_por
        self.players = [[] for _ in range(401)]  # 存放每个房间的ip_port
        self.playersId = [[] for _ in range(401)]  # 存放每个房间玩家id、名字和位置
        self.playersPos = [[1 for i in range(0, 9)] for _ in range(401)]  # 每个房间每个位置是否空余
        self.playersLive = []  # 存放所有在线玩家的id和名字
        self.map = ['1' for _ in range(401)]  # 存放每个房间的题目信息
        self.personColor = {}  # 存放玩家的颜色
        self.roomOwner = [0 for _ in range(401)]  # 存放每个房间的房主位置
        self._clearAllRoom()

    # 接受可以广播的ip_port
    def listen(self, addr, id):
        self.players[0].append(addr)
        self.id_ip_port[int(id)] = addr

    # 登录
    def logIn(self, addr, user, pwd):
        id = self._getId(user, pwd)
        if id is None:
            self._createNewId(user, pwd)
            id = self._getId(user, pwd)
        self._changePerson(id, 'live', 1)
        self._changeRoom(0, 'num', 1)
        name = self._display(id)[1]
        self.playersLive.append((id, name))
        self.personColor[id] = 'red'
        string = ''
        for i in range(1, 401):
            if len(self.playersId[i]) == 0:
                continue
            string += str(i) + ':' + str(len(self.playersId[i])) + ',' + self.map[i]
            string += '#'
        string = string[0:len(string) - 1]
        self.listener.sendto("{id};{name};{string}".format(id=id, name=name, string=string).encode(), addr)

    # 退出游戏
    def quitGame(self, addr, id, name):
        del self.players[0][self.players[0].index(self.id_ip_port[int(id)])]
        del self.playersLive[self.playersLive.index((int(id), name))]
        self.id_ip_port.pop(int(id), 0)
        self._changePerson(int(id), 'live', 0)
        self._changeRoom(0, 'num', -1)

    # 退出房间
    def quitRoom(self, addr, rid, id, name, pos):
        del self.players[int(rid)][self.players[int(rid)].index(self.id_ip_port[int(id)])]
        del self.playersId[int(rid)][self.playersId[int(rid)].index([int(id), name, int(pos)])]
        for item in self.id_ip_port:
            if int(item) == int(id):
                continue
            self.listener.sendto('quitRoom;{rid}'.format(rid=int(rid)).encode(), self.id_ip_port[item])
        self.players[0].append(self.id_ip_port[int(id)])
        self.playersPos[int(rid)][int(pos)] = 1
        self._changeRoom(int(rid), 'num', -1)
        self._changePerson(int(id), 'rid', 0)
        self._changeRoom(0, 'num', 1)
        newOwnerId, newOwnerPos, newOwnerName = 0, 0, ""
        for i in range(1, 9):
            if self.playersPos[int(rid)][i] == 0:
                newOwnerPos = i
                break
        for item in self.playersId[int(rid)]:
            if item[2] == newOwnerPos:
                newOwnerId, newOwnerName = item[0], item[1]
                break
        self._changeInt('room', int(rid), 'owner', newOwnerId)
        self.roomOwner[int(rid)] = newOwnerPos
        print("the room {rid} owner is {pos}".format(rid=int(rid),pos=newOwnerPos))
        for item in self.players[int(rid)]:
            self.listener.sendto('quitRoomPos;{pos1};{pos}'.format(id=id,pos1=pos, pos=newOwnerPos).encode(), item)

    # 开始游戏
    def startGame(self, addr, rid):
        self._changeInt('room', int(rid), 'play', 1)
        for item in self.players[int(rid)]:
            self.listener.sendto('startGame'.encode(), item)


    # 创建房间
    def createRoom(self, addr, id, name):
        rid = self._findCreateRid()
        self.playersId[rid].append([int(id), name, 1])
        del self.players[0][self.players[0].index(self.id_ip_port[int(id)])]
        self.players[rid].append(self.id_ip_port[int(id)])
        self.playersPos[rid][1] = 0
        self.roomOwner[rid] = 1
        self._changeInt('person', int(id), 'rid', rid)
        self._changeInt('room', rid, 'owner', int(id))
        self._changeRoom(rid, 'num', 1)
        self.listener.sendto("{rid};1;{map}".format(rid=rid, map=self.map[rid]).encode(), addr)
        for item in self.id_ip_port:
            if int(item) == int(id):
                continue
            self.listener.sendto('createNewRoom;{rid};{map}'.format(rid=rid, map=self.map[rid]).encode(),
                                 self.id_ip_port[int(item)])
        self.personColor[int(id)] = 'red'

    # 加入房间
    def addRoom(self, addr, rid, id, name):
        del self.players[0][self.players[0].index(self.id_ip_port[int(id)])]
        pos = 0
        for i in range(1, 9):
            if self.playersPos[int(rid)][i] == 1:
                pos = i
                self.playersPos[int(rid)][i] = 0
                break
        self._changeRoom(int(rid), 'num', 1)
        self._changeInt('person', int(id), 'rid', rid)
        self.playersId[int(rid)].append([int(id), name, pos])
        self.players[int(rid)].append(self.id_ip_port[int(id)])
        string = ""
        for item in self.playersId[int(rid)]:
            string = string + str(item[2]) + ":" + str(item[1]) + "," + self.personColor[item[0]]
            if item != self.playersId[int(rid)][-1]:
                string = string + '#'
        self.listener.sendto("{pos};{map};{string};{owner}".format(pos=pos, map=self.map[int(rid)], string=string,
                                                                   owner=self.roomOwner[int(rid)]).encode(), addr)
        for item in self.id_ip_port:
            if int(item) == int(id):
                continue
            self.listener.sendto('addRoom;{rid}'.format(rid=int(rid)).encode(), self.id_ip_port[item])

        for item in self.players[int(rid)]:
            if item != self.id_ip_port[int(id)]:
                self.listener.sendto("addPerson;{pos};{name};{color}".format(pos=pos, name=name, color='red').encode(),
                                     item)

    # 游戏数据传输
    def gaming(self, addr, rid, pos,flag):
        print(rid,pos,flag)
        for item in self.players[int(rid)]:
            print(item)
            self.listener.sendto("gaming;{pos};{flag}".format(pos=pos,flag=flag).encode(), item)

    # 广播聊天信息
    def sendText(self, addr, name, string, id):
        for item in self.players[int(id)]:
            self.listener.sendto('text;{name};{string}'.format(name=name, string=string).encode(), item)

    # 广播房间中人物颜色信息
    def sendColor(self,addr, id, rid, pos, color):
        self.roomPersonColor[int(id)] = color
        for item in self.players[int(rid)]:
            self.listener.sendto('color;{pos};{color}'.format(pos=pos, colorId=color).encode(), item)

    # 广播房间地图信息
    def sendMap(self,addr, rid, mapData):
        self.map[int(rid)] = mapData
        for item in self.id_ip_port:
            self.listener.sendto('map;{rid};{map}'.format(rid=rid, map=mapData).encode(), self.id_ip_port[item])

    # 广播踢人信息
    def sendKick(self,addr, rid, pos):
        for item in self.players[int(rid)]:
            self.listener.sendto('kick;{pos}'.format(pos=pos).encode(), item)

    # 广播死亡信息
    def sendDead(self,addr,rid,pos):
        for item in self.players[int(rid)]:
            self.listener.sendto('dead;{pos}'.format(pos=pos).encode(), item)

    # 广播开始游戏消息
    def sendStartGame(self,addr,rid,pos):
        for item in self.players[int(rid)]:
            self.listener.sendto('sendStartGame;{pos}'.format(pos=pos).encode(), item)

    # 询问所有已创建房间信息
    def askAllCreatedRoom(self, addr):
        data = self._askAllCreatedRoom()
        array = []
        for x in data:
            for y in x:
                array.append(str(y))
        string = ';'.join(array) if len(array) > 0 else 'NO'
        self.listener.sendto(string.encode(), addr)

    # 询问所有在线人物名字
    def askAllLive(self, addr):
        data = ';'.join([item[1] for item in self.playersLive])
        self.listener.sendto(data.encode(), addr)

    def run(self):
        print('waiting')
        try:
            while True:
                readable, writable, exceptional = (
                    select.select(self.read_list, self.write_list, [])
                )
                for f in readable:
                    if f is self.listener:
                        msg, addr = f.recvfrom(1024)
                        msg = msg.decode('utf-8')
                        msg = msg.split(';')
                        print(msg, addr, *msg[1:])
                        getattr(self, msg[0])(addr, *msg[1:])
                        print(self.id_ip_port, self.players[0])

        except KeyboardInterrupt as e:
            print("222222222")
            pass


def main():
    c = GameServer("39.107.241.25", "SA", "lqdLQD!!", "BombGame")
    c.run()
    pass


if __name__ == '__main__':
    main()
