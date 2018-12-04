import socket
import threading


class GameClient():
    def __init__(self):
        self.ip_port = ''  # 服务端ip和port
        self.listenerSend = ''
        self.listenerRecv = ''
        self.rid, self.pos, self.map = 0, 0, 0
        self.id = ''
        self.name = ''
        self.room = ''  # 存放大厅中的房间信息 rid:num,map
        self.string = ''  # 存放大厅中的聊天信息
        self.choose = 0  # 当前界面是哪个类，0：大厅，1：房间，2：游戏
        self.nowRoomPerson = []  # 存放当前房间位置是否有人,名字和所选颜色(flag,name,color)
        self.owner = ''  # 存放房主位置

    def init(self, user, pwd):
        self.ip_port = ("127.0.0.1", 20000)  # 服务端ip和port
        self.listenerSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listenerRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rid, self.pos, self.map = 0, 0, 0
        self.listenerSend.sendto("logIn;{user};{pwd}".format(user=user, pwd=pwd).encode(), self.ip_port)
        data = self.listenerSend.recv(1024).decode('utf-8').split(';')
        self.id = int(data[0])
        self.name = data[1]
        self.room = [[0, 0] for _ in range(401)]  # 存放大厅中的房间信息 rid:num,map
        temp = data[2].split('#')
        if temp[0] != '':
            for item in temp:
                temp1 = item.split(':')
                temp2 = temp1[1].split(',')
                self.room[int(temp1[0])] = [int(temp2[0]), temp2[1]]
        self.listenerRecv.sendto('listen;{id}'.format(id=self.id).encode(), self.ip_port)
        self.string = ''  # 存放大厅中的聊天信息
        self.choose = 0  # 当前界面是哪个类，0：大厅，1：房间，2：游戏
        self.nowRoomPerson = []  # 存放当前房间位置是否有人,名字和所选颜色(flag,name,color)
        self.owner = -1  # 存放房主位置

    # 接受并处理广播的信息，这里包括游戏中的信息,函数外开启线程

    def run(self, hall, roomFrame):
        while True:
            data = self.listenerRecv.recv(1024).decode('utf-8').split(';')
            print(data)
            if data[0] == 'text':
                string = '{name}: {string}'.format(name=data[1], string=data[2])
                newstring, temp = '', ''
                i, cnt = 0, 0
                while i < len(string):
                    if cnt >= (33 if self.choose == 0 else 70):
                        newstring += temp + '\n'
                        temp = ''
                        cnt = 0
                    if '\u4e00' <= string[i] <= '\u9fff':
                        cnt += 2
                    else:
                        cnt += 1
                    temp += string[i]
                    i = i + 1
                newstring += temp + '\n'
                self.string = self.string + newstring
                if self.choose == 0:
                    hall.runText(self.string)
                elif self.choose == 1:
                    roomFrame.freshEntryText(self.string)
            if data[0] == 'createNewRoom':
                print(data)
                print('-----------------')
                self.room[int(data[1])] = [1, data[2]]
                if self.choose == 0:
                    hall.allRoom(self.room)
            if data[0] == 'addRoom':
                self.room[int(data[1])][0] += 1
                if self.choose == 0:
                    hall.allRoom(self.room)
            if data[0] == 'addPerson':
                self.nowRoomPerson[int(data[1])] = [1, data[2], data[3]]
                print(self.pos,self.owner)
                if self.pos == self.owner:
                    roomFrame.freshNewPerson(1,int(data[1]), data[2], data[3])
                else:
                    roomFrame.freshNewPerson(0,int(data[1]), data[2], data[3])
            if data[0] == 'quitRoom':
                self.room[int(data[1])][0] -= 1
                print(self.room[int(data[1])])
                if self.choose == 0:
                    hall.allRoom(self.room)
            if data[0] == 'quitRoomPos':
                print(data, self.rid)
                self.nowRoomPerson[int(data[1]) - 1] = [0, 0, 0]
                roomFrame.freshQuitRoom(int(data[1]))
                print('old owner is {id}'.format(id=self.owner))
                self.owner = int(data[2])
                print('new owner is {id}'.format(id=self.owner))
                if self.pos == self.owner:
                    roomFrame.freshNewOwner(self.nowRoomPerson)
            if data[0] == 'color':
                self.nowRoomPerson[int(data[1])][2] = data[2]
                roomFrame.freshPersonColor(int(data[1]), data[2])
            if data[0] == 'map':
                if self.rid == int(data[1]):
                    self.map = data[2]
                    roomFrame.freshMap(self.map)
            if data[0] == 'kick':
                if self.pos == int(data[1]):
                    self.quitRoom()

    # 请求所有已创建的房间信息
    def askAllCreatedRoom(self):
        self.listenerSend.sendto("askAllCreatedRoom".encode(), self.ip_port)
        data = self.listenerSend.recv(8096).decode('utf-8').split(';')
        print(data)

    # 请求所有在线人物的名字
    def askAllLive(self):
        self.listenerSend.sendto('askAllLive'.encode(), self.ip_port)
        data = self.listenerSend.recv(8096).decode('utf-8').split(';')
        print(data)

    # 创建房间
    def createRoom(self):
        self.listenerSend.sendto('createRoom;{id};{name}'.format(id=self.id, name=self.name).encode(), self.ip_port)
        data = self.listenerSend.recv(1024).decode('utf-8').split(';')
        self.rid, self.pos, self.map = int(data[0]), int(data[1]), data[2]
        print(self.rid, self.pos, self.map)
        self.choose = 1
        self.nowRoomPerson = [[0, 0, 0] for _ in range(8)]
        self.nowRoomPerson[0] = [1, 1, 'red']
        self.owner = 1
        self.room[self.rid] = [1, self.map]

    # 加入房间
    def addRoom(self, rid):
        self.rid = rid
        self.listenerSend.sendto(
            'addRoom;{rid};{id};{name}'.format(rid=self.rid, id=self.id, name=self.name).encode(),
            self.ip_port)
        data = self.listenerSend.recv(8096).decode('utf-8').split(';')
        print(data)
        self.owner = int(data[3])
        self.pos, self.map = int(data[0]), data[1]
        self.nowRoomPerson = [[0, 0, 0] for _ in range(8)]
        data = data[2].split('#')
        cnt = 0
        for item in data:
            temp = item.split(':')
            temp1 = temp[1].split(',')
            self.nowRoomPerson[int(temp[0]) - 1] = [1, temp1[0], temp1[1]]
            cnt += 1
        self.room[int(rid)] = [cnt, self.map]
        self.choose = 1

    # 退出房间
    def quitRoom(self):
        print(self.room[self.rid])
        self.room[self.rid][0] -= 1
        temp = self.rid
        self.rid = 0
        self.choose = 0
        self.owner = -1
        self.listenerSend.sendto(
            'quitRoom;{rid};{id};{name};{pos}'.format(rid=temp, id=self.id, name=self.name, pos=self.pos).encode(),
            self.ip_port)

    # 退出游戏
    def quitGame(self):
        self.listenerSend.sendto('quitGame;{id};{name}'.format(id=self.id, name=self.name).encode(), self.ip_port)

    # 开始游戏
    def startGame(self):
        self.listenerSend.sendto('startGame;{rid}'.format(rid=self.rid).encode(), self.ip_port)
        self.choose = 2

    # 信息传输
    def gaming(self, string):
        self.listenerSend.sendto(
            'gaming;{rid};{pos}:{string}'.format(rid=self.rid, pos=self.pos, string=string).encode(), self.ip_port)

    # 发送聊天信息
    def sendText(self, string):
        self.listenerSend.sendto(
            'sendText;{name};{string};{rid}'.format(name=self.name, string=string, rid=self.rid).encode(),
            self.ip_port)

    # 发送房间中人物颜色信息
    def sendColor(self, color):
        self.listenerSend.sendto(
            'sendColor;{id};{rid};{pos};{color}'.format(id=self.id, rid=self.rid, pos=self.pos, color=color).encode(),
            self.ip_port)

    # 发送房间地图信息
    def sendMap(self, map):
        self.map = map
        self.listenerSend.sendto('sendMap;{rid};{map}'.format(rid=self.rid, map=self.map).encode(), self.ip_port)

    # 发送踢人信息
    def sendKick(self, pos):
        self.listenerSend.sendto('sendkick;{rid};{pos}'.format(rid=self.rid, pos=pos).encode(), self.ip_port)


def gaming(c):
    c.run()


def main():
    c = GameClient('xiaoming', 'xiaoming')
    thread = threading.Thread(target=gaming, args=(c,))
    thread.start()
    c.askAllCreatedRoom()
    c.askAllLive()
    c.createRoom()
    c.quitRoom()
    c.createRoom()
    c.startGame()
    while True:
        c.gaming('1')
    pass


if __name__ == '__main__':
    main()
