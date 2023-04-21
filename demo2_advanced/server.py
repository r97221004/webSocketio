import socket

hostaddress = ("127.0.0.1", 5000)

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.bind(hostaddress)
sk.listen(5)
print("啟動 socket 服務, 等待客戶端連接...")

conn, clientaddress = sk.accept()

while True:
    data = conn.recv(1024).decode()

    if data == "exit":
        print("客戶端發送完成, 斷開連結")
        break

    print(f"接收到客戶端 {clientaddress} 發送的訊息 {data} ")
    res = data.upper()
    conn.sendall(res.encode())

conn.close()


