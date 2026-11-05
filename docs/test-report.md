### Luồng đúng
| TC-01: Dự đoán mô tả hợp lệ · Ưu tiên: Cao   
| Bước      : 1. Nhập mô tả lỗi hợp lệ: "Màn hình điện thoại xuất hiện sọc xanh"   
| Mong đợi  : Nhóm AI đề xuất: Màn hình. Điểm dự đoán theo nhóm sự cố: 40%   
| Thực tế   : Nhóm AI đề xuất: Màn hình. Điểm dự đoán theo nhóm sự cố: 35.87%   
| PASS · docs/screenshots/TC-01.png   

| TC-02: Dự đoán lỗi sạc · Ưu tiên: Trung bình   
| Bước      : 1. Nhập mô tả lỗi hợp lệ: "Chân sạc bị lỏng phải giữ mới sạc được"   
| Mong đợi  : Nhóm AI đề xuất: Sạc. Điểm dự đoán theo nhóm sự cố: 45%   
| Thực tế   : Nhóm AI đề xuất: Sạc. Điểm dự đoán theo nhóm sự cố: 53.19%   
| PASS · docs/screenshots/TC-02.png 

### Giá trị biên
| TC-03: Mô tả đủ 10 ký tự · Ưu tiên: Cao   
| Bước      : 1. Nhập mô tả lỗi hợp lệ: "pin bi loi"   
| Mong đợi  : Nhóm AI đề xuất: Pin. Điểm dự đoán theo nhóm sự cố: 40%   
| Thực tế   : Nhóm AI đề xuất: Pin. Điểm dự đoán theo nhóm sự cố: 29.07%   
| PASS · docs/screenshots/TC-03.png 

| TC-04: Mô tả dưới 10 ký tự· Ưu tiên: Cao   
| Bước      : 1. Nhập mô tả lỗi không hợp lệ: "pin bi hu"   
| Mong đợi  : Mô tả lỗi phải có ít nhất 10 ký tự.   
| Thực tế   : Mô tả lỗi phải có ít nhất 10 ký tự.   
| PASS · docs/screenshots/TC-04.png 

### Dữ liệu sai
| TC-05: Không nhập mô tả · Ưu tiên: Cao   
| Bước      : 1. Không nhập mô tả lỗi   
| Mong đợi  : Vui lòng nhập mô tả lỗi.   
| Thực tế   : Vui lòng nhập mô tả lỗi.    
| PASS · docs/screenshots/TC-05.png 

| TC-06: Mô tả chỉ có khoảng trống · Ưu tiên: Thấp   
| Bước      : 1. Nhập mô tả lỗi là một khoảng trống: "          "   
| Mong đợi  : Vui lòng nhập mô tả lỗi.    
| Thực tế   : Vui lòng nhập mô tả lỗi.    
| PASS · docs/screenshots/TC-06.png 

| TC-07: Ký tự vô nghĩa · Ưu tiên: Thấp   
| Bước      : 1. Nhập mô tả lỗi: "^$ư4grge$^%&GR#r"   
| Mong đợi  : Mô tả chứa quá nhiều ký tự đặc biệt.     
| Thực tế   : Mô tả chứa quá nhiều ký tự đặc biệt.    
| PASS · docs/screenshots/TC-07.png 

| TC-11 (TC-03): Xử lý chuỗi rỗng và khoảng trắng · Ưu tiên: Cao   
| Bước      : 1. Chạy môi trường ảo: ./.venv/Scripts/Activate.ps1
              2. python -m pytest -q hoặc python -m pytest -v   
| Mong đợi  : PASSED   
| Thực tế   : tests/test_text.py::test_TT03_chuoi_rong_hoac_chi_co_khoang_trang PASSED             
| PASS · docs/screenshots/TC-11.png 

### Chất lượng dữ liệu/Tái lập
| TC-08 (test_split_disjoint_and_deterministic): Kiểm tra tập dữ liệu không trùng và chia có tính xác định · Ưu tiên: Cao   
| Bước      : 1. Chạy môi trường ảo: ./.venv/Scripts/Activate.ps1
              2. python -m pytest -q hoặc python -m pytest -v   
| Mong đợi  : PASSED   
| Thực tế   : tests/test_split.py::test_split_disjoint_and_deterministic PASSED       
| PASS · docs/screenshots/TC-08.png 

### Chất lượng dữ liệu
| TC-09 (TT-01): Giữ giấu và về chữ thường · Ưu tiên: Cao   
| Bước      : 1. Chạy môi trường ảo: ./.venv/Scripts/Activate.ps1
              2. python -m pytest -q hoặc python -m pytest -v   
| Mong đợi  : PASSED   
| Thực tế   : tests/test_text.py::test_TT01_giu_dau_va_ve_chu_thuong PASSED         
| PASS · docs/screenshots/TC-09.png 

| TC-10 (TT-02): Ẩn SĐT, mail, mã serial · Ưu tiên: Cao   
| Bước      : 1. Chạy môi trường ảo: ./.venv/Scripts/Activate.ps1
              2. python -m pytest -q hoặc python -m pytest -v   
| Mong đợi  : PASSED   
| Thực tế   : tests/test_text.py::test_TT02_thay_thong_tin_dinh_danh_bang_the PASSED          
| PASS · docs/screenshots/TC-10.png 

