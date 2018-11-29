import socket
import threading
import operat

bind_ip = "127.0.0.1"
bind_port = 40000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#将套接字与指定的ip和端口相连
server.bind((bind_ip, bind_port))
#启动监听，并将最大连接数设为5
server.listen(5)
print ("[*] listening on %s:%d" %(bind_ip, bind_port))

#存放每个ID的IP地址和端口号
global allIp
allIp = {}


#定义函数，回发信息给客户端
def handle_client(client_socket,addr):
    global allIp
    request = client_socket.recv(1024)
    request = request.decode('utf-8')
    request = request.split(';')
    id = operat.getId(request[0], request[1])
    if id is None:
        operat.createNewId(request[0], request[1])
        id = operat.getId(request[0], request[1])
    client_socket.send('success'.encode())
    operat.changeperson(id,'live',1)
    allIp[id] = (addr[0],20000)
    while(1):
        #打印客户端发送的消息
        request = client_socket.recv(1024)
        request = request.decode('utf-8')
        print ("[*] Received: %s" % request)
        request = request.split(';')
        print(request)
        #返回一个数据包，内容为ACK!
        if request[0] == "end":
            operat.changeperson(id,'live',0)
            client_socket.send('good-bye'.encode())
            client_socket.shutdown(2)
            client_socket.close()
            break
        elif request[0] == "createRoom":
            rid = operat.findId()
            operat.changeperson(id,'rid',rid)
            operat.changeroom(rid,'num',1)
            operat.changeroom(rid,'map',1)
            operat.changeroom(rid,'owner',id)
            client_socket.send('success'.encode())
        elif request[0] == "askAllRoom":
            ls = operat.askroom()
            temp = []
            for x in ls:
                for y in x:
                    temp.append(y)
            if len(temp):
                client_socket.send(str(temp)[1:-1].encode())
            else:
                client_socket.send("No".encode())
        elif request[0] == "startGame":
            pass
        elif request[0] == "addRoom":
            x = operat.askoneroom(int(request[1]))
            y = int(x[1]) + 1
            operat.changeroom(int(request[1]),'num',y)
            print("-----------")
            print(id,request[1])
            operat.changeperson(id,'rid',int(request[1]))
            print("------------")
            client_socket.send('success'.encode())
        elif request[0] == 'quitRoom':
            rid = operat.findRid(id)
            operat.changeperson(id,'rid',0)
            x = operat.askoneroom(rid)
            y = int(x[1]) - 1
            operat.changeroom(rid,'num',y)
            if id == int(operat.askoneroom(rid)[4]):
                ls = []
                if y != 0:
                    ls = operat.findIdOfRoom(rid)
                    operat.changeroom(rid,'owner',ls[0])
                #需要通知房间中的人刷新
                for item in ls:
                    operat.send('fresh',allIp[item])
            client_socket.send('success'.encode())
        else:
            client_socket.send('success'.encode())


#服务端进入主循环，等待连接
while True:
    #当有连接时，将接收到的套接字存到client中，远程连接细节保存到addr中
    client, addr = server.accept()
    print ("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    #创建新线程，回发信息给客户端
    client_handler = threading.Thread(target=handle_client, args=(client,addr))
    client_handler.start()

