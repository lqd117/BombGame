import tkinter as tk
from PIL import ImageTk, Image
from test.client import GameClient
root = tk.Tk()
root.overrideredirect(True)#移除标题栏
root.attributes("-alpha", 0.8)#窗口透明度60 %
width = 950
height = 750
#获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)
#设置窗口是否可变长、宽，True：可变，False：不可变
root.resizable(width=False, height=True)


canvas = tk.Canvas(root, width=950, height=750, bd=0, highlightthickness=0)
imgpath = 'photos/login.gif'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas.create_image(475,375, image=photo)
canvas.pack()


#账号密码
defaultValue1 = tk.StringVar()
defaultValue1.set("your account number")
defaultValue2 = tk.StringVar()
defaultValue2.set("Your password")

client = '111'

def go():
    global client
    user = user_text.get()
    pwd = pwd_text.get()
    client[0] = GameClient(user,pwd)
    print(client[0].id,client[0].name)

def close():
    global root
    root.destroy()

user_text=tk.Entry(textvariable = defaultValue1)
user_text.pack()
pwd_text=tk.Entry(textvariable = defaultValue2,show = '*')
pwd_text.pack()
imgpath1 = 'photos/SignIn.gif'
img1 = Image.open(imgpath1)
photo1 = ImageTk.PhotoImage(img1)
buttonLogIn = tk.Button(root,text="Sign In",command = go,image=photo1)
buttonLogIn.pack()
imgpath2 = 'photos/quit.gif'
img2 = Image.open(imgpath2)
photo2 = ImageTk.PhotoImage(img2)
buttonClose= tk.Button(root,text="Quit",command = close,image=photo2)
buttonClose.pack()

canvas.create_window(475, 330, width=200, height=30,window=user_text)
canvas.create_window(475, 380, width=200, height=30,window=pwd_text)
canvas.create_window(475, 430, width=100, height=30,window=buttonLogIn)
canvas.create_window(880, 710, width=100, height=30,window=buttonClose)


tk.mainloop()
