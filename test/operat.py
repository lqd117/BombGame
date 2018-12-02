import lib

#询问可以创建的房间ID
def askCreateRoomId(id):
    st = lib.ServerTCP()
    return st.connectServer('askCreatedRoomId;'+str(id))

#询问所有已被创建的房间状态
def askAllRoom():
    st = lib.ServerTCP()
    return st.connectServer('askAllRoom')

#开始游戏请求服务端处理
def startGame(id):
    st = lib.ServerTCP()
    st.connectServer('startGame;'+str(id))

#加入房间时请求服务端处理
def addRoom(id,rid):
    st = lib.ServerTCP()
    st.connectServer('addRoom;'+str(id)+';'+str(rid))

#捡到道具时请求服务端处理
def changeItem(id,name):
    st = lib.ServerTCP()
    st.connectServer('item;'+str(id)+';'+str(name))

#死亡时请求服务端处理
def death(id,array):
    st = lib.ServerTCP()
    st.connectServer('death;'+str(id)+";"+str(array))

#修改地图请求服务端处理
def changeMap(id,name):
    st = lib.ServerTCP()
    st.connectServer('changeMap;'+str(id)+';'+str(name))

#游戏结束请求服务端处理
def gameOver(id):
    pass






def main():
    pass
if __name__ == '__main__':
    main()












