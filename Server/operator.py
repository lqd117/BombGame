import lib
import random
global HOST,USER,PWD,DB
HOST,USER,PWD,DB = "0.0.0.0","SA","lqdLQD!!","BombGame"

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
    print(ls)
    return ls

#改变某个id某个状态,num为变量
def changeperson(id,name,num):
    global HOST, USER, PWD, DB
    ms = lib.mssql(host=HOST, user=USER, pwd=PWD, db=DB)
    ms.ExecNonQuery("update person set " +name+" = "+str(num)+" where id = "+str(id))


def main():
    #print(findId())
    change(1,"bomb",1)
    display(1)
    askroom()
    changeperson(1,'live',1)
    display(1)

if __name__ == '__main__':
    main()