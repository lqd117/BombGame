# 该文件是登录界面类
import tkinter as tk
from PIL import ImageTk, Image


class LogIn():
    def __init__(self):
        self.root = tk.Tk()
        self.user_text = ''
        self.pwd_text = ''
        self.buttonLogIn = ''
        self.canvas = tk.Canvas(self.root, width=950, height=750, bd=0, highlightthickness=0)

    def go(self, client, GameClient):
        user = self.user_text.get()
        pwd = self.pwd_text.get()
        client.append(GameClient())
        client[0].init(user, pwd)
        print(client[0].id, client[0].name)
        self.root.destroy()

    def run(self, client, GameClient):
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
        imgpath = 'photos/SignIn.gif'
        img = Image.open(imgpath)
        photo = ImageTk.PhotoImage(img)
        self.buttonLogIn = tk.Button(self.root, text="Sign In", command=lambda: self.go(client, GameClient),
                                     image=photo)
        imgpath2 = 'photos/login.gif'
        img2 = Image.open(imgpath2)
        photo2 = ImageTk.PhotoImage(img2)
        self.canvas.create_image(475, 375, image=photo2)
        defaultValue1 = tk.StringVar()
        defaultValue1.set("your account number")
        defaultValue2 = tk.StringVar()
        defaultValue2.set("Your password")
        self.user_text = tk.Entry(textvariable=defaultValue1)
        self.pwd_text = tk.Entry(textvariable=defaultValue2, show='*')
        self.canvas.pack()
        self.user_text.pack()
        self.pwd_text.pack()
        self.buttonLogIn.pack()

        self.canvas.create_window(475, 330, width=200, height=30, window=self.user_text)
        self.canvas.create_window(475, 380, width=200, height=30, window=self.pwd_text)
        self.canvas.create_window(475, 430, width=100, height=30, window=self.buttonLogIn)

        tk.mainloop()


def main():
    pass


if __name__ == '__main__':
    main()
