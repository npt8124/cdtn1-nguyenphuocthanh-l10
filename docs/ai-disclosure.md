# BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI BT1

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| ChatGPT | Hỗ trợ xây dựng và rà soát yêu cầu chức năng, User Story, mức ưu tiên MoSCoW và tiêu chí kiểm chứng. | Mục 1: Bản SRS rút gọn. | Đối chiếu với checklist của giảng viên; rà soát sự nhất quán giữa FR, US, Use Case và bảng truy vết. |
| ChatGPT | Hỗ trợ xây dựng Use Case Diagram, xác định Actor, Use Case, luồng chính và luồng ngoại lệ. | Mục 2: Use Case. | Đối chiếu với yêu cầu đề bài; kiểm tra mã UC01–UC07 và các ánh xạ với SRS. |
| ChatGPT | Hỗ trợ xây dựng sơ đồ ML Pipeline, mô tả Input/Output, loại bài toán, định nghĩa nhãn và metric đánh giá. | Mục 4: Mô hình dữ liệu theo chuyên ngành AI. | Đối chiếu với dataset và tài liệu case study; kiểm tra số mẫu, phân bố nhãn, cách chia dữ liệu và các metric dự kiến. |
| — Không dùng — | | Mục 3: Thiết kế kiến trúc<br>Mục 5: Wireframe 3 màn hình | Không áp dụng |

# BẢNG KHAI BÁO SỬ DỤNG CÔNG CỤ AI BT2

| Công cụ | Dùng vào việc gì | Áp dụng ở phần nào | Đã kiểm chứng thế nào |
| :--- | :--- | :--- | :--- |
| ChatGPT | Gợi ý code toàn bộ phần | `src/data/database.py`<br>`src/models`<br>`src/ui`<br>`app.py` | Viết dựa theo gợi ý của ChatGPT kết hợp cùng với src mẫu của tài liệu tham khảo có sẵn |
| Gemini | Hướng dẫn sử dụng các lệnh trên Terminal và Git Bash | Tạo môi trường, tự kiểm thử | Chạy các câu lệnh đó |
| — Không dùng — | | Toàn bộ `tests/`<br>`src/features/text.py`<br>`.gitignore`<br>`.env.example` | Không áp dụng |
