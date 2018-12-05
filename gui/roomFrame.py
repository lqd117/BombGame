# 该文件是房间界面类
import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk, Image
import tkinter.font as tkFont
import os
import threading

import inspect
import ctypes

class RoomFrame():
    def __init__(self):
        self.root = ''
        self.canvas = ''
        for i in range(1, 9):
            exec("self.buttonPerson{id} = ''".format(id=i))  # 房主可点击每个人物对应的按钮确定是否踢出该玩家
            exec("self.buttonMap{id} = ''".format(id=i))  # 该按钮用来选择题图
            exec("self.buttonColor{id}=''".format(id=i))  # 用来选择自己角色的颜色
            exec("self.buttonPersonFlag{id} = ''".format(id=i))  # 用来显然自己是不是房主以及名字
        self.buttonText = ''  # 聊天输入按钮
        self.buttonStart = ''  # 开始游戏按钮
        self.buttonQuit = ''  # 退出房间按钮
        self.labelText = ''  # 用来显示聊天界面
        self.allText = ''  # 用来显示聊天内容
        self.entryText = ''  # 用来输入聊天内容
        self.buttonYes = ''  # 用来发送聊天内容
        self.arrButtonColor = ''  # 用来存放按钮颜色
        self.labelMap = ''  # 用来显示地图
        self.mapName = ['乾', '震', '坎', '艮', '坤', '巽', '离', '兑']  # 八个地图名字
        self.start = 0 # 用来判断是否开始游戏

    def closeWindow(self):
        tkinter.messagebox.showerror(message="Don't close from here")
        return

    def quitRoom(self, client):
        client.quitRoom()
        self.root.destroy()

    def startGame(self, client):
        client.sendStartGame()
        self.root.destroy()

    def runText(self, string=""):  # 用于更新聊天内容
        self.allText.set(string)

    def sendText(self, client):  # 用于发送聊天内容
        string = self.entryText.get()
        print(string)
        client.sendText(string)
        self.entryText.delete(0, tk.END)

    def sendColor(self, colorId, client):  # 用于发送玩家所改变的颜色
        print(self.arrButtonColor[colorId])
        # client.sendColor(self.arrButtonColor[colorId])

    def sendMap(self, mapId, client):  # 用于发送地图信息
        print(self.mapName[mapId - 1])
        # client.sendMap(self.mapName[mapId-1])

    def kickPerson(self, pos, client):  # 判断是否踢出此人
        if pos != client.pos:
            a = tkinter.messagebox.askquestion('Warning', 'Do you want to kick this person?')
            print(a)
            if a == 'yes':
                client.sendKick(pos)

    def freshNewPerson(self, flag, pos, name, color):  # 当有人加入房间时的渲染
        exec("self.buttonPersonFlag{id}.set('        {name}')".format(id=pos, name=name))
        print(flag)
        if flag == 1:
            exec("self.buttonPerson{id}['state'] = tk.NORMAL".format(id=pos))
        self.freshPersonColor(pos, color)

    def freshNewOwner(self,room):
        exec("self.buttonStart['state'] = tk.NORMAL")
        for i in range(1,9):
            exec("self.buttonMap{id}['state'] = tk.NORMAL".format(id=i))
        for i in range(0,8):
            if room[i][0] == 1:
                exec("self.buttonPerson{id}['state'] = tk.NORMAL".format(id=i + 1))

    def freshQuitRoom(self, pos):
        exec("self.buttonPersonFlag{id}.set('')".format(id=pos))
        exec("self.buttonPerson{id}['state'] = tk.DISABLED".format(id=pos))
        self.freshPersonColor(pos, 'no')

    def freshEntryText(self, string):
        self.allText.set(string)

    def freshPersonColor(self, pos, color):
        exec("imgpath = 'photos/roomperson.gif'")
        exec("img = Image.open(imgpath)")
        exec("photo = ImageTk.PhotoImage(img)")
        exec("self.buttonPerson{id}.config(image=photo)".format(id=pos))
        exec("self.buttonPerson{id}.image = photo".format(id=pos))


    def freshMap(self, map):
        exec("imgpath = 'photos/roomperson.gif'")
        exec("img = Image.open(imgpath)")
        exec("photo = ImageTk.PhotoImage(img)")
        exec("self.labelMap.config(image=photo)")
        exec("self.labelMap.image = photo")

    def freshAll(self, client):
        #exec("self.buttonStart['state'] = tk.DISABLED")
        for i in range(1, 9):
            exec("self.buttonPerson{id}['state'] = tk.DISABLED".format(id=i))
            exec("self.buttonMap{id}['state'] = tk.DISABLED".format(id=i))
        if client.owner == client.pos:
            exec("self.buttonStart['state'] = tk.NORMAL")
            for i in range(0, 8):
                exec("self.buttonMap{id}['state'] = tk.NORMAL".format(id=i + 1))
                if client.nowRoomPerson[i][0] == 0:
                    continue
                exec("self.buttonPerson{id}['state'] = tk.NORMAL".format(id=i + 1))
        exec("imgpath = 'photos/roomperson.gif'")
        exec("img = Image.open(imgpath)")
        exec("photo = ImageTk.PhotoImage(img)")
        exec("self.labelMap.config(image=photo)")
        exec("self.image = photo")
        print(client.nowRoomPerson)
        for i in range(0, 8):
            if client.nowRoomPerson[i][0] == 0:
                continue
            if client.pos == i + 1:
                exec(
                    "self.buttonPersonFlag{id}.set('Owner   {name}')".format(id=i + 1, name=client.nowRoomPerson[i][1]))
            else:
                exec(
                    "self.buttonPersonFlag{id}.set('        {name}')".format(id=i + 1, name=client.nowRoomPerson[i][1]))
            exec("imgpath{id} = 'photos//roomperson.gif'".format(id=i + 1))
            exec("img{id} = Image.open(imgpath{id})".format(id=i + 1))
            exec("photo{id} = ImageTk.PhotoImage(img{id})".format(id=i + 1))
            exec("self.buttonPerson{id}.config(image=photo{id})".format(id=i + 1))
            exec("self.buttonPerson{id}.image = photo{id}".format(id=i + 1))

    def run(self, client):
        self.start = 0
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=950, height=750, bd=0, highlightthickness=0)
        self.root.protocol('WM_DELETE_WINDOW', self.closeWindow)
        # self.root.overrideredirect(True)  # 移除标题栏
        self.root.attributes("-alpha", 0.9)  # 窗口透明度60 %
        width = 950
        height = 750
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.root.resizable(width=False, height=True)

        imgpath = 'photos/room.gif'
        img = Image.open(imgpath)
        photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(475, 375, image=photo)

        imgpath2 = 'photos/yes.gif'
        img2 = Image.open(imgpath2)
        photo2 = ImageTk.PhotoImage(img2)

        self.allText = tk.StringVar()
        self.allText.set('')
        ft = tkFont.Font(size=15)
        ft1 = tkFont.Font(size=25)

        for i in range(1, 9):
            exec('self.buttonPersonFlag{id} = tk.StringVar()'.format(id=i))
            exec("self.buttonPersonFlag{id}.set('')".format(id=i))

        self.arrButtonColor = ['gray', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black']  # 存放按钮颜色
        arrButtonPos = [[575, 653]]  # 存放八个颜色按钮的位置
        for i in range(1, 8):
            arrButtonPos.append([arrButtonPos[i - 1][0] + 50, arrButtonPos[i - 1][1]])
        arrButtonColorPos = [[875, 450], [925, 450]]  # 存放八个地图按钮的位置
        for i in range(0, 3):
            arrButtonColorPos.append([arrButtonColorPos[i * 2][0], arrButtonColorPos[i * 2][1] + 50])
            arrButtonColorPos.append([arrButtonColorPos[i * 2 + 1][0], arrButtonColorPos[i * 2 + 1][1] + 50])
        arrButtonPersonPos = [[130, 100]]
        for i in range(0, 3):
            arrButtonPersonPos.append([arrButtonPersonPos[i][0] + 200 + 30, arrButtonPersonPos[i][1]])
        for i in range(0, 4):
            arrButtonPersonPos.append([arrButtonPersonPos[i][0], arrButtonPersonPos[i][1] + 200 + 10])
        print(arrButtonPersonPos)
        self.buttonQuit = tk.Button(self.root, text='Quit Room', bg='white', command=lambda: self.quitRoom(client))
        self.buttonStart = tk.Button(self.root, text='Start Game', bg='white', command=lambda: self.startGame(client))
        self.buttonYes = tk.Button(self.root, image=photo2, bg='white', command=lambda: self.sendText(client))
        self.labelText = tk.Label(self.root, textvariable=self.allText, bg='white', justify="left", font=ft,
                                  anchor=tk.SW)
        self.entryText = tk.Entry(font=ft)
        self.entryText.bind('<Key-Return>', lambda x: self.sendText(client))
        self.buttonColor1 = tk.Button(self.root, bg=self.arrButtonColor[1], command=lambda: self.sendColor(1, client))
        self.buttonColor2 = tk.Button(self.root, bg=self.arrButtonColor[2], command=lambda: self.sendColor(2, client))
        self.buttonColor3 = tk.Button(self.root, bg=self.arrButtonColor[3], command=lambda: self.sendColor(3, client))
        self.buttonColor4 = tk.Button(self.root, bg=self.arrButtonColor[4], command=lambda: self.sendColor(4, client))
        self.buttonColor5 = tk.Button(self.root, bg=self.arrButtonColor[5], command=lambda: self.sendColor(5, client))
        self.buttonColor6 = tk.Button(self.root, bg=self.arrButtonColor[6], command=lambda: self.sendColor(6, client))
        self.buttonColor7 = tk.Button(self.root, bg=self.arrButtonColor[7], command=lambda: self.sendColor(7, client))
        self.buttonColor8 = tk.Button(self.root, bg=self.arrButtonColor[8], command=lambda: self.sendColor(8, client))
        self.labelMap = tk.Label(self.root, bg='white')
        self.buttonMap1 = tk.Button(self.root, text=self.mapName[0], command=lambda: self.sendMap(1, client))
        self.buttonMap2 = tk.Button(self.root, text=self.mapName[1], command=lambda: self.sendMap(2, client))
        self.buttonMap3 = tk.Button(self.root, text=self.mapName[2], command=lambda: self.sendMap(3, client))
        self.buttonMap4 = tk.Button(self.root, text=self.mapName[3], command=lambda: self.sendMap(4, client))
        self.buttonMap5 = tk.Button(self.root, text=self.mapName[4], command=lambda: self.sendMap(5, client))
        self.buttonMap6 = tk.Button(self.root, text=self.mapName[5], command=lambda: self.sendMap(6, client))
        self.buttonMap7 = tk.Button(self.root, text=self.mapName[6], command=lambda: self.sendMap(7, client))
        self.buttonMap8 = tk.Button(self.root, text=self.mapName[7], command=lambda: self.sendMap(8, client))
        self.buttonPerson1 = tk.Button(self.root, textvariable=self.buttonPersonFlag1, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(1, client))
        self.buttonPerson2 = tk.Button(self.root, textvariable=self.buttonPersonFlag2, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(2, client))
        self.buttonPerson3 = tk.Button(self.root, textvariable=self.buttonPersonFlag3, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(3, client))
        self.buttonPerson4 = tk.Button(self.root, textvariable=self.buttonPersonFlag4, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(4, client))
        self.buttonPerson5 = tk.Button(self.root, textvariable=self.buttonPersonFlag5, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(5, client))
        self.buttonPerson6 = tk.Button(self.root, textvariable=self.buttonPersonFlag6, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(6, client))
        self.buttonPerson7 = tk.Button(self.root, textvariable=self.buttonPersonFlag7, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(7, client))
        self.buttonPerson8 = tk.Button(self.root, textvariable=self.buttonPersonFlag8, font=ft1, anchor=tk.NW,
                                       command=lambda: self.kickPerson(8, client))

        self.canvas.pack()
        self.buttonQuit.pack()
        self.buttonStart.pack()
        self.buttonYes.pack()
        self.labelText.pack()
        self.entryText.pack()
        self.labelMap.pack()

        self.canvas.create_window(850, 700, width=100, height=40, window=self.buttonQuit)
        self.canvas.create_window(650, 700, width=100, height=40, window=self.buttonStart)
        self.canvas.create_window(250, 550, width=500, height=250, window=self.labelText)
        self.canvas.create_window(225, 700, width=450, height=40, window=self.entryText)
        self.canvas.create_window(475, 700, width=50, height=40, window=self.buttonYes)
        for i in range(1, 9):
            exec('self.buttonColor{id}.pack()'.format(id=i))
            exec('self.canvas.create_window({x}, {y}, width=50, height=34, window=self.buttonColor{id})'.format(
                x=arrButtonPos[i - 1][0], y=arrButtonPos[i - 1][1], id=i))
        self.canvas.create_window(700, 530, width=300, height=210, window=self.labelMap)
        for i in range(1, 9):
            exec('self.buttonMap{id}.pack()'.format(id=i))
            exec('self.canvas.create_window({x}, {y}, width=50, height=50, window=self.buttonMap{id})'.format(
                x=arrButtonColorPos[i - 1][0], y=arrButtonColorPos[i - 1][1], id=i))
        for i in range(1, 9):
            exec('self.buttonPerson{id}.pack()'.format(id=i))
            exec('self.canvas.create_window({x}, {y}, width=200, height=200, window=self.buttonPerson{id})'.format(
                x=arrButtonPersonPos[i - 1][0], y=arrButtonPersonPos[i - 1][1], id=i))

        self.freshAll(client)

        self.root.mainloop()


def main():
    pass


if __name__ == '__main__':
    main()
