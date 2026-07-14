from socket import *
import os

SERVER_PORT = 12000
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_FOLDER = os.path.join(SCRIPT_DIR, "clientFolder")
os.makedirs(CLIENT_FOLDER, exist_ok=True)

files = [f for f in os.listdir(CLIENT_FOLDER)
         if os.path.isfile(os.path.join(CLIENT_FOLDER, f))]
if len(files) == 0:
    print(f"Không tìm thấy file nào trong: {CLIENT_FOLDER}")
    exit()
print(f"Tìm thấy {len(files)} file: {files}")
serverName = input("Nhập địa chỉ IP của server: ")
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, SERVER_PORT))
print(f"Đã kết nối tới server: {serverName}:{SERVER_PORT}")
try:
    clientSocket.send(str(len(files)).encode())
    clientSocket.recv(1024)
    for file_name in files:
        file_path = os.path.join(CLIENT_FOLDER, file_name)
        file_size = os.path.getsize(file_path)
        header = f"{file_name}|{file_size}\n"
        clientSocket.sendall(header.encode())
        clientSocket.recv(1024)
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                clientSocket.sendall(chunk)
        clientSocket.recv(1024) 
        print(f"Đã gửi: {file_name} ({file_size} bytes)")
except Exception as e:
    print(f"Lỗi: {e}")
finally:
    clientSocket.close()
