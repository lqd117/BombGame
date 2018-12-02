import socket
import threading


class GameClient():
    def __init__(self, user, pwd):
        self.ip_port = ("127.0.0.1", 20000)  # 服务端ip和port
        self.listenerSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listenerRecv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rid, self.pos, self.map = 0, 0, 0
        self.listenerSend.sendto("logIn;{user};{pwd}".format(user=user, pwd=pwd).encode(), self.ip_port)
        data = self.listenerSend.recv(1024).decode('utf-8').split(';')
        self.id = int(data[0])
        self.name = data[1]
        self.listenerRecv.sendto('listen;{id}'.format(id=self.id).encode(), self.ip_port)
        self.string = ''  # 存放大厅中的聊天信息
        self.room = {}  # 存放大厅中的房间信息 rid,num
        self.choose = 0  # 当前界面是哪个类，0：大厅，1：房间，2：游戏

    '''
    大厅界面中房间信息（5s）和人物信息(5mins)由客户端定时请求，函数外控制时间
    聊天信息由服务端广播得到
    '''

    # 接受并处理广播的信息，这里包括游戏中的信息,函数外开启线程

    def run(self, hall):
        while True:
            data = self.listenerRecv.recv(1024).decode('utf-8').split(';')
            print(data)
            if data[0] == 'text':
                string = '{name}: {string}'.format(name=data[1], string=data[2])
                newstring, temp = '', ''
                i, cnt = 0, 0
                while i < len(string):
                    if cnt >= 33:
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
                hall.runText(self.string)
            if data[0] == 'createNewRoom':
                self.room[int(data[1])] = [1, data[2]]
                hall.allRoom(self.room)
            if data[0] == 'addRoom':
                self.room[int(data[1])][0] += 1
                hall.allRoom(self.room)
            if data[0] == 'quitRoom':
                self.room[int(data[1])][0] -= 1
                hall.allRoom(self.room)

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

    # 加入房间
    def addRoom(self, rid):
        print("beahbadf")
        self.rid = rid
        self.listenerSend.sendto(
            'addRoom;{rid};{id};{name}'.format(rid=self.rid, id=self.id, name=self.name).encode(),
            self.ip_port)
        print("211111")
        data = self.listenerSend.recv(8096).decode('utf-8').split(';')
        print(data)
        self.choose = 1

    # 退出房间
    def quitRoom(self):
        self.listenerSend.sendto(
            'quitRoom;{rid};{id};{name};{pos}'.format(rid=self.rid, id=self.id, name=self.name, pos=self.pos).encode(),
            self.ip_port)
        self.choose = 0

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
        self.listenerSend.sendto('sendText;{name};{string}'.format(name=self.name, string=string).encode(),
                                 self.ip_port)


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
