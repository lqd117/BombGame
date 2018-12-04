import socket,sys,select
import threading

target_host = '39.107.241.25'
target_port = 40000

global client
#建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
#连接到服务器
client.connect((target_host, target_port))

def handle_udp(udpSocket):
    global client
    while 1:
        data = udpSocket.recvfrom(1024)
        print(data)
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(("",20000))
udp_handle = threading.Thread(target=handle_udp,args=(udpSocket,))
udp_handle.start()




def main():
    while 1:
        string = input()
        client.send(string.encode())
        print(client.recv(4096).decode('utf-8'))
        if string == "end":
            break

if __name__ == '__main__':
    main()