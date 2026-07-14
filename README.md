# Hệ thống Truyền tải File qua Mạng (Client-Server Socket TCP)

Dự án này tạo ra một hệ thống để gửi file giữa Client và Server sử dụng giao thức TCP thông qua thư viện `socket` của Python. Chương trình được xây dựng để đảm bảo dữ liệu không bị lỗi, xử lý vấn đề "dính gói tin" và có khả năng chuyển các file lớn mà không làm đầy bộ nhớ RAM.

## Tính năng nổi bật

* **Truyền tải ổn định:** Sử dụng giao thức TCP (AF_INET, SOCK_STREAM) để đảm bảo không có dữ liệu nào bị mất trong quá trình truyền.
* **Cơ chế đồng bộ hóa:** Giao tiếp giữa Client và Server diễn ra hai chiều một cách hiệu quả qua thông điệp `ACK`, giúp kiểm soát việc gửi và nhận, ngăn ngừa tình trạng dính hoặc mất gói tin.
* **Tối ưu bộ nhớ:** Dữ liệu được truyền đi từng phần nhỏ (tối đa 4096 bytes) thay vì tải toàn bộ vào RAM, giúp quá trình chuyển file lớn diễn ra trơn tru.
* **Hỗ trợ nhiều loại file:** Hệ thống có thể truyền tải mọi kiểu tệp (từ văn bản `.txt`, tài liệu `.pdf` đến hình ảnh `.jpg`, `.png`) bằng cách sử dụng chế độ mã hóa nhị phân (`rb`/`wb`).
* **Tự động hóa thư mục:** Hệ thống tự động kiểm tra và tạo ra các thư mục gốc (`clientFolder`, `serverFolder`) nếu chúng chưa tồn tại.

## Cấu trúc hệ thống và Giao thức

Quá trình gửi file được thiết lập với một Header tùy chỉnh giúp Server xác định thông tin file một cách chính xác:

1. **Bước khởi đầu:** Client gửi số lượng file cần truyền. Server sẽ phản hồi với `ACK`.
2. **Gửi Header:** Đối với mỗi file, Client sẽ đóng gói tên file và kích thước thành chuỗi Header theo định dạng: `file_name|file_size\n`.
3. **Xử lý dòng dữ liệu:** * Server đọc từng byte cho đến khi gặp ký tự `\n` để tách Header.
* Dựa vào `file_size`, Server sử dụng công thức `min(4096, file_size - bytes_received)` để kiểm soát chính xác số byte cần nhận trong vòng lặp cuối cùng, ngăn chặn việc đọc nhầm dữ liệu của file tiếp theo.



## Hướng dẫn Cài đặt và Sử dụng

### Yêu cầu hệ thống

* **Python:** 3.x
* **Cổng sử dụng mặc định:** `12000`

### Các bước khởi động

**Bước 1: Khởi động Server** Mở Terminal và chạy file `server.py`. Hệ thống sẽ tạo thư mục `serverFolder` và bắt đầu nhận kết nối.

```bash
python3 server.py 

```

**Bước 2: Khởi động Client** Đặt các file cần gửi vào thư mục `clientFolder` (hệ thống sẽ tự tạo nếu chưa có). Chạy file `client.py`.

```bash
python3 client.py 

```

**Bước 3: Kết nối và gửi dữ liệu** Nhập địa chỉ IP của máy chủ khi được yêu cầu (chẳng hạn: `127.0.0.1` nếu bạn đang chạy trên cùng một máy tính). Hệ thống sẽ tự động kiểm tra thư mục và bắt đầu gửi tệp tin.
