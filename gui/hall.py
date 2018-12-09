# 该文件是大厅界面类
import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk, Image
import tkinter.font as tkFont
import os


class Hall():
    def __init__(self):
        self.root = ''
        for i in range(1, 9):
            exec("self.buttonRoom{id} = ''".format(id=i))
            exec("self.buttonRoomtext{id} = ''".format(id=i))
        self.canvas = ''
        self.labelPerson = ''
        self.buttonYes = ''
        self.buttonQuit = ''
        self.buttonNewRoom = ''
        self.text = ''
        self.string = ''
        self.allText = ''
        self.allRoomData = ''  # 只存放8个房间的信息
        self.buttonid_rid = ''  # 存放每个button对应的rid

    def closeWindow(self):
        tkinter.messagebox.showerror(message="Don't close from here")
        return

    def go(self, client):
        string = self.text.get()
        print(string)
        client.sendText(string)
        self.text.delete(0, tk.END)

    def quitGame(self, client):
        client.quitGame()
        os._exit(0)

    def createRoom(self, client):
        client.createRoom()
        self.root.destroy()

    def allRoom(self, room):  # 更新房间信息,由client调用
        for i in range(1, 9):
            exec("self.buttonRoom{id}['state'] = tk.DISABLED".format(id=i))
            exec("self.buttonRoomtext{id}.set('NO\\nROOM')".format(id=i))
        self.allRoomData = []  # 从client中选择可以进去的最多8个房间信息
        self.buttonid_rid = [0 for _ in range(8)]
        cnt = 0
        for i in range(1,401):
            if cnt == 8:
                break
            if room[i][0] == 0:
                continue
            print(room[i])
            self.allRoomData.append([i, room[i][0], room[i][1]])  # 分别是rid,num,map
            cnt += 1
        for i in range(1, cnt + 1):
            exec("self.buttonRoom{id}['state'] = tk.NORMAL".format(id=i))
            self.buttonid_rid[i] = self.allRoomData[i - 1][0]
            exec("self.buttonRoomtext{id}.set('{rid}   {map}\\n"
                 "      {num}/8')".format(id=i, rid=str(self.buttonid_rid[i]).zfill(3),
                                          map=self.allRoomData[i - 1][2], num=self.allRoomData[i - 1][1]))

    def runText(self, string=""):  # 用于更新聊天内容
        self.allText.set(string)

    def room(self, id, client):
        client.addRoom(self.buttonid_rid[id])
        self.root.destroy()

    def run(self, client):
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

        ft = tkFont.Font(size=15)

        imgpath5 = 'photos/1.gif'
        img5 = Image.open(imgpath5)
        photo5 = ImageTk.PhotoImage(img5)

        self.allText = tk.StringVar()
        self.allText.set('')
        self.labelPerson = tk.Label(self.root, textvariable=self.allText, bg='white',
                                    image=photo5,compound=tk.CENTER,justify="left", font=ft)

        self.text = tk.Entry(font=ft)
        self.text.bind('<Key-Return>', lambda x: self.go(client))

        imgpath2 = 'photos/yes.gif'
        img2 = Image.open(imgpath2)
        photo2 = ImageTk.PhotoImage(img2)
        self.buttonYes = tk.Button(self.root, image=photo2, command=lambda: self.go(client))

        self.buttonQuit = tk.Button(self.root, text='Quit Game', bg='white', command=lambda: self.quitGame(client))

        self.buttonNewRoom = tk.Button(self.root, text='New Room', bg='white', command=lambda: self.createRoom(client))

        arr = []
        arr.append([100 + 50, 60 + 50])
        arr.append([100 + 50 + 200 + 50, 60 + 50])
        for i in range(0, 3):
            arr.append([arr[i * 2][0], arr[i * 2][1] + 120 + 20])
            arr.append([arr[i * 2 + 1][0], arr[i * 2 + 1][1] + 120 + 20])
        print(arr)
        ft1 = tkFont.Font(size=30)
        for i in range(1, 9):
            exec('self.buttonRoomtext{id} = tk.StringVar()'.format(id=i))
            exec("self.buttonRoomtext{id}.set('NO\\nROOM')".format(id=i))

        imgpath3 = 'photos/room12.gif'
        img3 = Image.open(imgpath3)
        photo3 = ImageTk.PhotoImage(img3)

        self.buttonRoom1 = tk.Button(self.root, textvariable=self.buttonRoomtext1, image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(1, client))
        self.buttonRoom2 = tk.Button(self.root, textvariable=self.buttonRoomtext2,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(2, client))
        self.buttonRoom3 = tk.Button(self.root, textvariable=self.buttonRoomtext3,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(3, client))
        self.buttonRoom4 = tk.Button(self.root, textvariable=self.buttonRoomtext4,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(4, client))
        self.buttonRoom5 = tk.Button(self.root, textvariable=self.buttonRoomtext5,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(5, client))
        self.buttonRoom6 = tk.Button(self.root, textvariable=self.buttonRoomtext6,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(6, client))
        self.buttonRoom7 = tk.Button(self.root, textvariable=self.buttonRoomtext7,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1, state=tk.DISABLED,
                                     command=lambda: self.room(7, client))
        self.buttonRoom8 = tk.Button(self.root, textvariable=self.buttonRoomtext8,image=photo3,compound=tk.CENTER,
                                     bg='white', font=ft1,  state=tk.DISABLED,
                                     command=lambda: self.room(8, client))

        for i in range(1, 9):
            exec('self.buttonRoom{id}.pack()'.format(id=i))
            exec('self.canvas.create_window({x}, {y}, width=200, height=100,'
                 ' window=self.buttonRoom{id})'.format(x=arr[i - 1][0], y=arr[i - 1][1], id=i))

        self.canvas.pack()
        self.labelPerson.pack()
        self.text.pack()
        self.buttonYes.pack()
        self.buttonQuit.pack()
        self.buttonNewRoom.pack()

        self.canvas.create_window(750, 250, width=400, height=500, window=self.labelPerson)
        self.canvas.create_window(725, 520, width=350, height=40, window=self.text)
        self.canvas.create_window(925, 520, width=50, height=40, window=self.buttonYes)
        self.canvas.create_window(850, 620, width=100, height=40, window=self.buttonQuit)
        self.canvas.create_window(650, 620, width=100, height=40, window=self.buttonNewRoom)

        self.allRoom(client.room)

        self.root.mainloop()


def main():
    pass


if __name__ == '__main__':
    main()
