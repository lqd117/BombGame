# 这是终极主函数
'''
在主函数中，首先调用登录界面类，同时传入一个参数client
在登录成功时由该类初始化client,然后关闭该窗口
之后调用大厅界面类，该类由两个模块组成，房间模块，聊天界面模块，该类中有这两个个模块的渲染方
法，在大厅中时，由线程中的client方法调用该类中的方法，当玩家创建或加入房间时，由该线程判断
该事件是否发生同时决定是否发生，当发生时，该线程关闭当前窗口并调用
房间界面类，同样该线程决定是否渲染，当游戏开始时，关闭当前窗口并调用pygame
当游戏结束时，重新调用房间界面类
'''

from gui.logIn import LogIn
from test.client import GameClient
from gui.hall import Hall
from gui.roomFrame import RoomFrame
from main import game
import threading
import pygame


def main():
    login, client = [], []
    login = LogIn()
    login.run(client, GameClient)
    client = client[0]
    print(client.id, client.name)
    hall = Hall()
    roomFrame = RoomFrame()
    pygame.init()
    bombgame = game()
    thread = threading.Thread(target=client.run, args=(hall,roomFrame,bombgame))
    thread.start()
    while 1:
        if client.choose == 0:
            hall.run(client)
        elif client.choose == 1:
            roomFrame.run(client)
        elif client.choose == 2:
            print('------',client.sum)
            bombgame.alivenum = client.sum
            bombgame.init(client.nowRoomPerson)
            bombgame.run(client)


    # client = GameClient()
    # client.init('xiaoming', 'xiaoming')
    # client.pos = 1
    # thread = threading.Thread(target=client.run, args=(hall, roomFrame, bombgame))
    # thread.start()
    # bombgame.run(client)



if __name__ == '__main__':
    main()
