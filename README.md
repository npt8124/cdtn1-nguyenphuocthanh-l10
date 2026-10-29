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
pandas==2.2.3   
numpy==2.1.3   
scikit-learn==1.5.2   
joblib==1.4.2   
PyYAML==6.0.2   
pytest==8.3.4   
streamlit==1.41.1   
PyYAML==6.0.2   
Biến môi trường: xem .env.example   
## 3. Hướng dẫn chạy
### Với người dùng VS code   
Bước 1: Tạo môi trường ảo Python 3.11   
Mở thu mục cdtn1-nguyenphuocthanh-l10-main, New Terminal

py -3.11 -m venv .venv

Bước 2: Kích hoạt môi trường ảo

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser   

.\.venv\Scripts\Activate.ps1

Bước 3: Cài đặt các thư viện cần thiết

python -m pip install -r requirements.txt

Bước 4: Huấn luyện, kiểm thử và khởi chạy hệ thống

python -m src.models.train --config configs/train.yaml

python -m pytest -q

python -m streamlit run app.py

### Lưu ý với người dùng VS Code
Kiểm tra tính tái lập   
Huấn luyện hai lần với cùng cấu hình và so sánh metrics.json:

python -m src.models.train --config configs/train.yaml   
Copy-Item reports\metrics.json reports\metrics_lan1.json

python -m src.models.train --config configs/train.yaml   
Compare-Object (Get-Content reports\metrics_lan1.json) (Get-Content reports\metrics.json)

Nếu Compare-Object không in ra khác biệt, hai file giống nhau.
### Với người dùng Git Bash   
Bước 1: Clone git về máy   
cd /tmp && rm -rf thu-nghiem && mkdir thu-nghiem && cd thu-nghiem

git clone https://github.com/npt8124/cdtn1-nguyenphuocthanh-l10

Bước 2: Tạo và kích hoạt môi trường ảo python 3.11

cd cdtn1-nguyenphuocthanh-l10

py -3.11 -m venv .venv

source .venv/Scripts/activate

Bước 3: Cài đặt các thư viên cần thiết

pip install -r requirements.txt

Bước 4: Huấn luyện, kiểm thử và khởi chạy hệ thống

python -m src.models.train --config configs/train.yaml

python -m pytest -q 

python -m streamlit run app.py
## 4. Cấu trúc thư mục
Cấu trúc thư mục 
cdtn1-nguyenphuocthanh-l10/   
├── artifacts/ # lưu mô hình ML đã huấn luyện   
│   └── warranty_model.joblib  # mô hình và TF-IDF vectorizer, sinh tự động   
├── configs # chứa cấu hình huấn luyện   
│ └── train.yaml # siêu tham số, hạt giống ngẫu nhiên   
├── docs # tài liệu phân tích và đặc tả hệ thống   
│ └── ai-disclosure.md # bảng khai báo sử dụng công cụ AI   
│ └── architecture.drawio # sơ đồ kiến trúc hệ thống   
│ └── Buổi 2 Phiếu phạm vi bài toán cá nhân 261_71ITGR40203_06_Base.docx # báo cáo buổi 2   
│ └── Buổi 4 Báo cáo thực hành 261_71ITGR40203_06.docx # báo cáo buổi 4   
│ └── ml-pipeline.drawio # sơ đồ pipeline    
│ └── ml-problem-statement.md # các vấn đề gặp phải   
│ └── srs.md # file SRS đặc tả yêu cầu hệ thống   
│ └── thay-doi-thiet-ke.md # file thể hiện chi tiết những thay đổi trong thiết kế   
│ └── usecase.drawio # các usecase    
│ └── wireframe1.jpg # ảnh màn hình 1, 2   
│ └── wireframe2.jpg # ảnh màn hình 3   
├── src/ # mã nguồn chính của hệ thống     
│ ├── data/ xử lý và chuẩn bị dữ liệu   
│ │ ├── mau/ # chứa tập dữ liệu mẫu   
│ │ │   └── issue_descriptions.csv   
│ │ ├── load.py # đọc và kiểm tra dữ liệu thô   
│ │ └── split.py # CHIA dữ liệu train/valid/test   
│ ├── features/ # tiền xử lý và trích xuất đặc trưng   
│ │ └── text.py # làm sạch văn bản, vector hoá   
│ ├── models/ # các mô hình ML   
│ │ ├── baseline.py # mô hình cơ sở BẮT BUỘC để so sánh   
│ │ └── train.py # huấn luyện mô hình chính   
│ │ └── predict.py         # dự đoán nhóm sự cố từ mô tả lỗi   
│ ├── ui/                    # thành phần giao diện báo cáo    
│ │ └── report.py          # hiển thị kết quả đánh giá mô hình   
│ └── evaluate.py # đo và ghi kết quả   
├── reports/ #lưu báo cáo kết quả đánh giá   
│ └── metrics.json # metrics, kết quả theo nhãn, ma trận nhầm lẫn   
├── tests/ # các bài kiểm thử tự động   
│ └── test_predict.py # kiểm thử chức năng dự đoán   
│ └── test_split.py # kiểm thử chia dữ liệu   
│ └── test_text.py # kiểm thử xử lý văn bản   
├── .env.example # mẫu khai báo biến môi trường   
├── .gitignore # danh sách file/thư mục không đưa lên Git   
├── app.py # code khởi chạy giao diện Streamlit   
├── README.md # giới thiệu và hướng dẫn sử dụng   
├── requirements.txt # các thư viện Python cần thiết   
## 5. Kiểm thử 
Chạy bộ kiểm thử tự động:

python -m pytest -q

Kết quả mong đợi: tất cả bài kiểm thử PASS.

Huấn luyện mô hình:

python -m src.models.train --config configs/train.yaml

Kết quả mong đợi: chương trình tạo hai tệp artifacts/warranty_model.joblib và reports/metrics.json.

Khởi chạy giao diện:

python -m streamlit run app.py

Truy cập http://localhost:8501 và kiểm tra:

Giao diện hiển thị bình thường.

Nhập mô tả lỗi hợp lệ và nhận nhóm sự cố đề xuất.

Nhập mô tả rỗng và nhận thông báo lỗi rõ ràng.

Tab kết quả đánh giá hiển thị số liệu được đọc từ reports/metrics.json.

Khi thiếu mô hình hoặc báo cáo, giao diện hiển thị thông báo thay vì ngừng hoạt động.
## 6. Trạng thái hiện tại
[x] Khởi tạo project, smoke test chạy được (buổi 2)  
[x] Module tiếp nhận yêu cầu (buổi 8–10)  
[x] Module phân công kỹ thuật viên (buổi 10–12)  
