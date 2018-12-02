import socket
class ServerTCP():
    def __init__(self):
        self.target_host = '39.107.241.25'
        self.target_port = 40000

    def connectServer(self,string):
        # 建立一个socket对象,AF_INET说明将使用标准的IPv4地址或主机名，SOCK_STREAM说明是一个TCP客户端
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到服务器
        client.connect((target_host, target_port))
        # 发送数据
        client.sendall(string.encode())
        # 接收数据
        response = client.recv(4096)
        return response




