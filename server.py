from socket import *
import os

SERVER_PORT = 12000
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_FOLDER = os.path.join(SCRIPT_DIR, "serverFolder")
os.makedirs(SERVER_FOLDER, exist_ok=True)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', SERVER_PORT))
serverSocket.listen(1)
print("Server sẵn sàng nhận file...")
print(f"Lưu file tại: {SERVER_FOLDER}\n")

while True:
    connectionSocket, addr = serverSocket.accept()
    print(f"Kết nối từ client: {addr}")
    
    try:
        data = connectionSocket.recv(1024).decode().strip()
        if not data:
            print("Không nhận được dữ liệu từ client.")
            connectionSocket.close()
            continue
        num_files = int(data)
        print(f"Số file cần nhận: {num_files}")
        connectionSocket.send("ACK".encode())
        for i in range(num_files):
            header_data = b""
            while True:
                b = connectionSocket.recv(1)
                if b == b'\n': 
                    break
                header_data += b
            file_name, file_size_str = header_data.decode().split('|')
            file_size = int(file_size_str)
            print(f"Chuẩn bị nhận file: {file_name} ({file_size} bytes)")
            connectionSocket.send("ACK".encode()) 
            save_path = os.path.join(SERVER_FOLDER, file_name)
            with open(save_path, "wb") as f:
                bytes_received = 0
                while bytes_received < file_size:
                    bytes_to_read = min(4096, file_size - bytes_received)
                    chunk = connectionSocket.recv(bytes_to_read)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk) 
            print(f"Đã lưu thành công: {file_name}")
            connectionSocket.send("ACK".encode())
    except Exception as e:
        print(f"Lỗi: {e}\n")
    finally:
        connectionSocket.close()
