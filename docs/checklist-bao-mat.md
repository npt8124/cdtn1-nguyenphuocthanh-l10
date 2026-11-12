# Checklist bảo mật — Tự đánh giá

Checklist gồm 7 mục bắt buộc theo Bài tập 3. Mỗi mục được đánh giá theo ba trạng thái: **ĐÃ LÀM / CHƯA LÀM / KHÔNG ÁP DỤNG**. Minh chứng được ghi dựa trên cấu trúc và mã nguồn thực tế của dự án.

| # | Mục | Kết quả | Minh chứng |
|---|---|---|---|
| 1 | Không có secret nào trong repository | **ĐÃ LÀM** | Đã rà soát cấu hình và mã nguồn, không phát hiện thông tin bí mật cần thiết cho việc vận hành ứng dụng. Dự án không sử dụng API key hoặc dịch vụ API bên ngoài. Tệp `.env` được sử dụng để lưu cấu hình môi trường riêng; `.env.example` dùng làm mẫu cấu hình. Lưu ý: chưa xác minh được toàn bộ lịch sử commit Git do thư mục làm việc hiện tại không có thư mục `.git`. |
| 2 | Dữ liệu đầu vào được kiểm tra tại tầng ứng dụng | **ĐÃ LÀM** | Hàm `validate_description()` trong `src/models/predict.py` kiểm tra kiểu dữ liệu, nội dung rỗng, tỷ lệ ký tự đặc biệt, độ dài tối thiểu 10 ký tự và số từ tối thiểu 2 từ trước khi dự đoán. Nội dung được loại bỏ khoảng trắng thừa và làm sạch trước khi đưa vào mô hình. |
| 3 | Kiểm soát quyền truy cập | **KHÔNG ÁP DỤNG** ở phạm vi prototype | Ứng dụng hiện là prototype sử dụng Streamlit, chưa triển khai tài khoản đăng nhập, xác thực người dùng hoặc phân quyền theo chủ sở hữu yêu cầu bảo hành. Vì vậy, chưa có cơ chế phân quyền giữa các nhân viên hoặc người dùng. Khi triển khai thực tế cần bổ sung xác thực, phân quyền và giới hạn quyền truy cập dữ liệu. |
| 4 | Dữ liệu nhạy cảm được xử lý trước khi sử dụng | **ĐÃ LÀM** | Hàm `lam_sach()` trong `src/features/text.py` thay thế thông tin nhận dạng như địa chỉ email, số điện thoại và số serial bằng các thẻ đại diện `<EMAIL>`, `<SDT>`, `<SERIAL>` trước khi vector hóa văn bản. Việc này giúp hạn chế thông tin định danh xuất hiện trong dữ liệu đầu vào của mô hình TF-IDF. |
| 5 | Thông báo lỗi không để lộ cấu trúc bên trong hệ thống | **CHƯA LÀM** | Trong app.py, một số khối except sử dụng st.error() để hiển thị trực tiếp nội dung ngoại lệ thông qua biến exc. Trong src/ui/report.py, lỗi khi xử lý dữ liệu báo cáo cũng được hiển thị kèm nội dung ngoại lệ. Việc hiển thị trực tiếp chi tiết ngoại lệ có thể làm lộ thông tin kỹ thuật nội bộ như đường dẫn hệ thống hoặc chi tiết lỗi cơ sở dữ liệu. |
| 6 | Nhật ký không ghi secret hoặc dữ liệu cá nhân | **CHƯA LÀM** | Chưa triển khai cơ chế ghi log ứng dụng riêng bằng thư viện logging. Các lệnh print() được tìm thấy trong src/models/train.py chủ yếu phục vụ việc thông báo kết quả huấn luyện mô hình. Qua kiểm tra docker compose logs --tail=200 app, log thu được chỉ hiển thị thông tin khởi chạy Streamlit; chưa phát hiện nội dung mô tả yêu cầu bảo hành hoặc thông tin cá nhân. Chưa có quy định cụ thể về loại dữ liệu được phép ghi vào log và cách bảo vệ thông tin nhạy cảm. |
| 7 | Phụ thuộc được ghim phiên bản và đã kiểm cảnh báo lỗ hổng | **ĐÃ LÀM MỘT PHẦN** | 	**ĐÃ LÀM**: requirements.txt ghim phiên bản chính xác bằng == cho cả chín gói; ảnh nền ghim python:3.11-slim, không dùng thẻ latest. Ghim scikit-learn==1.5.2 đặc biệt quan trọng: tệp mô hình lưu bởi phiên bản khác có thể nạp lỗi (đã ghi ở docs/deployment-guide.md mục 7). **CHƯA LÀM**: chưa chạy pip-audit. Việc cần làm: pip install pip-audit && pip-audit -r requirements.txt. |


## Những hạn chế bảo mật đã biết

1. **Chưa có cơ chế xác thực và phân quyền:** Ứng dụng hiện chưa quản lý tài khoản người dùng. Khi triển khai trong môi trường thực tế cần bổ sung đăng nhập và phân quyền theo vai trò.
2. **Chưa có giới hạn số lần gửi yêu cầu:** Ứng dụng chưa triển khai rate limiting. Nếu có nhiều yêu cầu liên tục, tài nguyên xử lý có thể bị quá tải.
3. **Chưa triển khai HTTPS:** Cấu hình hiện tại phục vụ ứng dụng Streamlit qua HTTP. Khi triển khai trên môi trường mạng thực tế cần sử dụng HTTPS thông qua reverse proxy có chứng chỉ TLS.