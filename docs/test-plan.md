# TEST PLAN – HỆ THỐNG TỰ ĐỘNG PHÂN LOẠI YÊU CẦU BẢO HÀNH

## 1. Phạm vi kiểm thử

**Mục tiêu:** Kiểm tra tính đúng đắn của các chức năng xử lý văn bản, dự đoán nhóm sự cố và chia tập dữ liệu trong hệ thống tự động phân loại yêu cầu bảo hành.

**Phạm vi kiểm thử:**
- Kiểm tra chức năng dự đoán nhóm sự cố với mô tả hợp lệ.
- Kiểm tra điều kiện đầu vào: mô tả rỗng, chỉ chứa khoảng trắng, ký tự không hợp lệ và độ dài tối thiểu.
- Kiểm tra chức năng tiền xử lý văn bản tiếng Việt và thay thế thông tin định danh.
- Kiểm tra quá trình chia dữ liệu Train, Validation và Test về số lượng, tính độc lập và khả năng tái lập.

**Phần chủ ý không kiểm thử:**
- Kiểm thử hiệu năng, khả năng chịu tải và nhiều người dùng đồng thời.
- Kiểm thử bảo mật toàn diện, phân quyền và xác thực tài khoản.
- Kiểm thử triển khai trên máy chủ thực tế hoặc môi trường Cloud.
- Kiểm thử tích hợp với hệ thống quản lý bảo hành bên ngoài.
- Đánh giá khả năng tổng quát hóa của mô hình trên dữ liệu bảo hành thực tế chưa có trong bộ dữ liệu thử nghiệm.

## 2. Loại kiểm thử và số lượng

Bộ kiểm thử được tổ chức theo các nhóm sau:

| Nhóm kiểm thử | Nội dung | Số lượng |
|---|---|---:|
| Luồng đúng | Dự đoán mô tả hợp lệ, kiểm tra kết quả phân loại | 2 |
| Kiểm thử biên | Kiểm tra mô tả tại và dưới giới hạn 10 ký tự | 2 |
| Dữ liệu sai | Mô tả rỗng, khoảng trắng, ký tự vô nghĩa | 4 |
| Chất lượng dữ liệu | Chuẩn hóa tiếng Việt, ẩn thông tin định danh | 2 |
| Tái lập | Kiểm tra chia tập dữ liệu không trùng lặp và có tính xác định | 1 |
| **Tổng cộng** | | **11** |

*Lưu ý: TT03 kiểm tra chuỗi rỗng và khoảng trắng, được tính trong nhóm dữ liệu sai. Nhóm bảo mật chưa có test chuyên biệt; TT02 chỉ kiểm tra việc thay thế thông tin định danh trong bước tiền xử lý.*

## 3. Tiêu chí thành công

Một lần kiểm thử được đánh giá PASS khi thỏa mãn các điều kiện sau:

- Mô tả hợp lệ được xử lý và trả về nhãn dự đoán thuộc sáu nhóm sự cố đã định nghĩa.
- Mô tả có độ dài đúng 10 ký tự được chấp nhận; mô tả dưới 10 ký tự bị từ chối theo quy tắc đầu vào.
- Dữ liệu rỗng, chỉ chứa khoảng trắng hoặc không đáp ứng điều kiện hợp lệ được xử lý đúng, không làm chương trình phát sinh lỗi ngoài dự kiến.
- Văn bản tiếng Việt giữ nguyên dấu và được chuẩn hóa chữ thường; thông tin định danh được thay thế bằng các thẻ tương ứng.
- Ba tập Train, Validation và Test có số lượng đúng theo tỷ lệ 70% – 15% – 15%, không có bản ghi trùng lặp giữa các tập và cho kết quả giống nhau khi chia lại với cùng cấu hình.

**Tiêu chí hoàn thành bộ kiểm thử:** 100% test case PASS, không có test case FAIL hoặc ERROR. Kết quả phải được ghi nhận bằng báo cáo chạy pytest.

## 4. Môi trường và dữ liệu thử nghiệm

**Môi trường kiểm thử:**
- Hệ điều hành: Windows 11.
- Ngôn ngữ lập trình: Python 3.11.9.
- Môi trường ảo: `.venv`.
- Framework kiểm thử: pytest 8.3.4.
- Thư viện xử lý dữ liệu: Pandas.
- Thư viện Machine Learning: Scikit-learn.
- Công cụ chạy kiểm thử: PowerShell / Terminal trong VS Code.

**Dữ liệu thử nghiệm:**
- Dữ liệu huấn luyện: `src/data/mau/issue_descriptions.csv`.
- Dữ liệu kiểm thử đơn vị: dữ liệu mẫu được tạo trực tiếp trong các file thuộc thư mục `tests/`.
- Dữ liệu chia tập: DataFrame gồm 120 bản ghi giả lập, chia thành 60 mẫu PIN và 60 mẫu SAC.
- Dữ liệu kiểm tra tiền xử lý: các chuỗi tiếng Việt, chuỗi rỗng, khoảng trắng và chuỗi chứa số điện thoại, mã serial, địa chỉ email.

**Lệnh thực hiện kiểm thử:**

```powershell
python -m pytest -v
```

Kết quả được lưu lại thông qua ảnh chụp màn hình Terminal và tổng hợp trong tài liệu Test Report.