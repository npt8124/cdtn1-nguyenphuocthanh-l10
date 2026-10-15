Tự động phân loại yêu cầu bảo hành
Sinh viên:
Nguyễn Phước Thành - 2374802013578 - Track AI
Học phần:
Chuyên đề Tốt nghiệp 1, HK1 2026-2027
Luồng nghiệp vụ:
L10 – Tự động phân loại yêu cầu bảo hành
## 1. Mục tiêu
Hệ thống hỗ trợ nhân viên tiếp nhận bảo hành tự động phân loại yêu cầu dựa trên mô tả lỗi do khách hàng cung cấp.
Hệ thống cho phép nhập mô tả lỗi, tự động đề xuất nhóm sự cố và mức ưu tiên, đồng thời cho phép nhân viên kiểm tra, điều chỉnh và xác nhận kết quả phân loại.
## 2. Yêu cầu môi trường
Python 3.11
Streamlit, Pandas, Scikit-learn, Joblib, Pytest
SQLite 3 (tích hợp sẵn trong Python)
Biến môi trường: xem .env.example
## 3. Hướng dẫn chạy
(BT2 yêu cầu ≤ 4 bước)
cp .env.example .env và điền giá trị
npm install
npm run db:migrate
npm run dev → mở http://localhost:3000/health
## 4. Cấu trúc thư mục
Giải thích ngắn mỗi thư mục làm gì.
## 5. Kiểm thử
npm test → hiển thị số test PASS
## 6. Trạng thái hiện tại
[x] Khởi tạo project, smoke test chạy được (buổi 2)  
[x] Module tiếp nhận yêu cầu (buổi 8–10)  
[] Module phân công kỹ thuật viên (buổi 10–12)  
