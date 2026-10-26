Tự động phân loại yêu cầu bảo hành
Sinh viên:
Nguyễn Phước Thành - 2374802013578 - Track AI
Học phần:
Chuyên đề Tốt nghiệp 1, HK1 2026-2027
Luồng nghiệp vụ:
L10 – Tự động phân loại yêu cầu bảo hành
## 1. Giới thiệu
Hệ thống hỗ trợ nhân viên nhập mô tả lỗi, dự đoán nhóm sự cố bằng TF-IDF + Logistic Regression, gợi ý mức ưu tiên theo quy tắc, điều chỉnh và xác nhận trước khi lưu SQLite.

## 2. Yêu cầu môi trường
- Python 3.11
- Streamlit, Pandas, Scikit-learn, Joblib, Pytest
- SQLite 3 (tích hợp sẵn trong Python)
- Các thư viện và phiên bản: xem `requirements.txt`

## 3. Cài đặt (PowerShell)
```powershell
cd "D:\Learning\Chuyên đề TN 1\CDTN1 - Test"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
Nếu PowerShell chặn kích hoạt môi trường ảo, chạy trực tiếp `.venv\Scripts\python.exe` thay cho `python` trong các lệnh.

## 4. Dataset
Đặt **toàn bộ** CSV do trường cung cấp tại `src/data/mau/issue_descriptions.csv`. Các cột bắt buộc:
`desc_id,issue_desc,issue_category,center_id`.
Không đưa `desc_id` hay `center_id` vào mô hình. Dữ liệu được loại bỏ dòng trống, nhãn không hợp lệ, trùng văn bản; mô tả trùng nhưng khác nhãn bị loại khỏi huấn luyện.

## 5. Huấn luyện và chạy
```powershell
python -m src.models.train --csv src/data/mau/issue_descriptions.csv
python -m streamlit run app.py
```
Đánh giá được lưu tại `models/evaluation.json`; mô hình tại `models/warranty_classifier.joblib`. Chỉ nạp mô hình Joblib đáng tin cậy.

## 6. Kiểm thử
```powershell
python -m pytest -q
```

## 7. Lưu ý phạm vi
- Đây là prototype, **chưa có đăng nhập và phân quyền**: không đưa dữ liệu khách hàng thật lên bản demo công khai.
- Ngưỡng confidence 0.70 là giá trị đề xuất, chưa hiệu chỉnh xác suất.
- Mức ưu tiên là quy tắc minh họa, cần xác nhận lại với giảng viên/nghiệp vụ.
- Kết quả test chỉ là số liệu đánh giá trên dữ liệu hiện có; không khẳng định đạt Macro F1 ≥ 0.70 trước khi chạy.
- Dữ liệu CSV đầy đủ chưa được đính kèm cuộc trò chuyện; không thể xác nhận số dòng hay phân bố nhãn thực tế.

## 8. Trạng thái hiện tại
[x] Khởi tạo project, smoke test chạy được (buổi 2)  
[x] Module tiếp nhận yêu cầu (buổi 8–10)  
[] Module phân công kỹ thuật viên (buổi 10–12)  
