Công nghệ cần thiết để chạy chương trình và link hướng dẫn cài đặt trên hệ điều hành windows:
-MySQL và Workbench: https://youtu.be/BYwb50Xbf8s
-Visual studio code: https://youtu.be/YWODbdejecU
-Python3: https://youtu.be/tYu8oHG3vqk

Hướng dẫn khởi tạo và cấu hình MySQL server
B1: Sau khi cài đặt và cấu hình database xong hết, mở Workbench vào file, vào "open SQL script" và mở file "init.sql" 
B2: Ở ngay đầu file "inti.sql" bôi đen dòng "create database crawler" và bấm vào biểu tượng tia sét để chạy câu lệnh
Tương tự với dòng kế tiếp "use crawler"
B3: Bôi đen toàn bộ các câu lệnh trong các phần "create table" tức đến trước phần "select *" và bấm vào biểu tượng tia sét
B4: Lặp đi lặp lại các bước sau:
B4.1: bôi đen lần lượt từng dòng "select *" và bấm vào biểu tượng tia sét ở trên thanh công cụ để chạy
B4.2: cạnh chữ export/import có biểu tượng khi chỉ vào sẽ có chữ import record from external file, click vào 
B4.3: click vào browse, tim file dữ liệu đầu vào với bảng tương ứng hoặc có thể dùng dữ liệu thử nghiệm có tên trùng với tên bảng có đuôi.csv ở trong tệp test_data
B4.4: click chọn exist table và tìm bảng tương ứng rồi bấm next tới khi hoàn thành việc import
**Nếu xảy ra lỗi, hãy thử để ý xem bảng import vào đã đúng với bảng trong database hay chưa
B5: Mở visual studio code, trong termial ở phần dưới của ứng dụng gõ lệnh "cd <đường dẫn tới file file ClusterPoint_3.py >" để dẫn tới đường dẫn của file ClusterPoint_3.py 
B6: sửa đổi file config.txt theo đúng cấu hình, khi cài đặt MySQL trên máy user và chạy thành công file init.sql, file config.txt có dạy sau:
localhost
user_name
password
crawler 
Trong đó user_name và password cần thay đổi theo cài đặt ban đầu khi cài đặt workbench
B7: gõ python ClusterPoint3.py để xử lí dữ liệu đầu vào, nếu thành công sẽ báo connection successful
* nếu kết nối thất bại sẽ có mã code để tìm kiếm lí do kết nối thất bại trên GOOGLE

Hướng dẫn chạy chương trình để cho tìm kiếm nhà cung cấp đám mây phù hợp với như cầu
B1: Mở visual studio code, trong termial ở phần dưới của ứng dụng gõ lệnh "cd <đường dẫn tới file file manipulation_3.py >" để dẫn tới đường dẫn của file manipulation_3.py
B2: gõ tiếp "python maipulation_3.py"
B3: nếu kết nối thành công,menu tùy chọn hiện ra:
1. Search for Cloud Storage Provider 
2. Search for Hosting Provider
Your the Number of your choose:
Gõ 1 hoặc 2 tùy theo mục đích tìm kiếm 
* nếu kết nối thất bại sẽ có mã code để tìm kiếm lí do kết nối thất bại trên GOOGLE
B4: trả lời các câu hỏi về cấu hình cần tìm kiếm hoặc Enter để bỏ qua
B5: khi chương trình hỏi đến câu "Do you need any other specific requirement? Y/n:", bấm "y" hoặc "Y" để hiện thị các tùy chọn đặc biệt
B5.1: nếu chọn "Y" hoặc "y", cần bôi đen và copy tùy chọn cần thiết bằng tổ hợp ctrl+C và paste vào sau "Enter the Option you want:" bằng tổ hợp Ctrl+shift+V
B6: hệ thống sẽ in ra terminal số lượng dữ liệu trong database, top 5 hoặc ít hơn các tùy chọn đáp ứng được cấu hình tìm kiếm hoặc trả lại rằng không có tùy chọn nào phù hợp
B7: kết thức chương trình, lặp lại bước 1 nếu muốn chạy lại chương trình