import socket

serveraddress = ("127.0.0.1", 5000)
sk = socket.socket()
sk.connect(serveraddress)


while True: 
    message = input("發送內容: ").strip()
    sk.sendall(message.encode())
     
    if message == "exit":
        print("客戶端退出連結。")
        break
        
    answer = sk.recv(1024).decode()
    print("收到服務器的應答: %s" % answer )

sk.close()