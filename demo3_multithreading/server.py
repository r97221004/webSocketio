import socket
import threading


def deal(link, clinet):
    print(f"新線程開始處理客戶端 {clinet}: {clinet} 的數據請求")
    while True:
        data = link.recv(1024).decode()

        if data == "exit":
            print(f"客戶端 {clinet}: {clinet} 發送完成，斷開連結。" )
            break

        print(f"接收到客戶端 {clinet} 發送來的信息: {data}")

        res = data.upper()

        # str
        link.sendall(res.encode())
    
    link.close()



hostaddress = ("127.0.0.1", 5000)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(hostaddress)
sk.listen(5)
print("啟動 socket 服務，等待客戶端的連接...")

while True:
    conn, clientaddress = sk.accept()
    xd = threading.Thread(target=deal, args=(conn, clientaddress))
    xd.start()







