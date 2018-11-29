import lib
import random,socket
global HOST,USER,PWD,DB
HOST,USER,PWD,DB = "39.107.241.25","SA","lqdLQD!!","BombGame"

#创建房间时返回一个可以创建的房间id
def findId():
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery("select rid from room where num = 0")
    return ls[random.randint(0,len(ls)-1)][0]

#改变某个id某个道具值,num为增量
def change(id,name,num):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery("select " +name+" from person where id = "+str(id))
    temp = int(ls[0][0]) + num
    ms.ExecNonQuery("update person set " +name+" = "+str(temp)+" where id = "+str(id))

#展示某个id的所有情况
def display(id):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery("select * from person where id = "+str(id))
    print(ls)
    return ls

#返回所有已被创建房间的状态
def askroom():
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery("select * from room where num != 0")
    return ls

#返回所有在线ID状态
def askAllId():
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery('select * from person where live = 1 or rid != 0')
    return ls

#删除某个ID记录
def deletId(id:int):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery('delete from person where id = ' + str(id))

#返回某一房间的状态
def askoneroom(rid:int):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery('select * from room where rid = '+str(rid))
    return ls[0]

#改变某个id某个状态,num为变量
def changeperson(id,name:str,num):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery("update person set " +name+" = "+str(num)+" where id = "+str(id))

#改变某个房间的状态,num为变量
def changeroom(rid:int,name:str,num:int):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery("update room set " + name + " = "+ str(num) + "where rid = "+str(rid))


#根据账号密码得到人物ID
def getId(user:str,pwd:str):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    id = ms.ExecQuery("select id from person where person.account = '"+ user +"' and person.pwd = '" + pwd+"'")
    if len(id) == 0:return None
    return id[0][0]

#创建新的人物
def createNewId(user:str,pwd:str):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery("insert into person (name,rid,live,bomb,power,speed,account,pwd) values ( '"+ user + "',0,1,0,0,0,'"+ user +
                    "','"+ pwd+ "')")

#查找某个ID在哪个房间
def findRid(id:int):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery('select rid from person where id = '+str(id))
    return ls[0][0]

#查询某个房间有哪些id
def findIdOfRoom(rid:int):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ls = ms.ExecQuery('select id from person where rid = '+str(rid))
    ls = [item[0] for item in ls]
    return ls

#清空所有房间
def clearRoom():
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery('update room set num = 0,play = 0,map = null,owner = null')
    ms.ExecNonQuery('update person set rid = 0')

#向某个client发送数据(udp)
def send(sendData,sendArr):
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpSocket.sendto(sendData.encode('utf-8'), sendArr)
    udpSocket.shutdown(2)
    udpSocket.close()

import socket
def main():
    #udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #send(udpSocket,"hello",('127.0.0.1',20000))
    #changeperson(9,'rid',277)

    print(askAllId())
    print(askroom())

if __name__ == '__main__':
    main()