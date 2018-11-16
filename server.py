import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#将套接字与指定的ip和端口相连
server.bind((bind_ip, bind_port))
#启动监听，并将最大连接数设为5
server.listen(5)
print "[*] listening on %s:%d" % (bind_ip, bind_port)

#定义函数，回发信息给客户端
def handle_client(client_socket):
    #打印客户端发送的消息
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request
    #返回一个数据包，内容为ACK!
    client_socket.send('ACK!')
    client_socket.close()

#服务端进入主循环，等待连接
while True:
    #当有连接时，将接收到的套接字存到client中，远程连接细节保存到addr中
    client, addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
    #创建新线程，回发信息给客户端
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
