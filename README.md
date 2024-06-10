# Face_Recognition

Hướng dẫn cài đặt môi trường
Cài đặt Python 3.7.9 và Visual Studio C++

Tải toàn bộ code về bằng git clone hoặc Code -> Download ZIP rồi giải nén

Vào folder Face_Recognition vừa có được

Mở Terminal:
Windows 11: Chuột phải -> Open in Windows Terminal
Windows 10: Shift + Chuột phải -> Open PowerShell window here

Cho phép Terminal chạy script:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy remotesigned
Tạo môi trường python ảo, rồi kích hoạt nó:

python -m venv .venv
./.venv/Scripts/Activate.ps1
Cài đặt các dependency cần thiết:

pip install -r requirements.txt
Nếu không báo lỗi, chương trình đã sẵn sàng được sử dụng

Trong trường hợp chúng ta muốn khôi phục lại trạng thái gốc của Terminal:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Undefined
deactivate

Hướng dẫn sử dụng:
Trước khi sử dụng, cần download bộ nhận dạng và dataset tại đây
Giải nén model_data rồi cho vào folder facial-expression-recognition-svm

Huấn luyện:
Chương trình có thể nhận diện được nhiều khuôn mặt khác nhau trong cùng 1 khung hình với độ chính xác trên tập dữ liệu nhỏ và vừa nằm trong khoảng 95.5 -> 98.5%:

Tuy nhiên, dữ được training mà chương trình huấn luyện càng lớn thì chương trình có thể nhận dạng thì độ chính xác sẽ càng thấp, cho nên trên mỗi tệp dữ liệu người dùng chúng ta cần tăng số lượng điểm ảnh khác nhau và số lượng ảnh trên mỗi tệp để tăng độ chính xác chung cho toàn bộ chương trình:

Cấu hình lại địa chỉ liên kết Mysql:

Khởi động chương trình: python app.py -> truy cập địa chỉ: http://127.0.0.1:5000 để thao tác với chương trình

Thu thập dữ liệu:
Nhấn vào nút thêm mới, điền đầy đủ thông tin và nhấn Submit, sau đó chờ khoảng 1 phút để hoàn thành quá trình quét và lấy dữ liệu khuôn mặt thông qua camera (Trong quá trình quét có thể xoay hoặc biểu thị cảm xúc nhằm tăng độ chính xác)

Bắt đầu quá trình huấn luyện:
python svm_model.py (hoặc restart lại app)
Nếu tập dữ liệu càng lớn thì thời gian chạy càng lâu

Chạy nhận dạng:
Trông của sổ chính của trang Web, nhấn điểm danh để thực hiện kiểm tra và đánh giá kết quả.
