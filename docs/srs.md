## 1.1 Giới thiệu, phạm vi và BẢNG THUẬT NGỮ

### Bảng thuật ngữ

| Thuật ngữ | Giải thích |
|---|---|
| SRS | Tài liệu đặc tả yêu cầu phần mềm. |
| User Story (US) | Mô tả nhu cầu của người dùng theo vai trò, mục tiêu và giá trị nhận được. |
| Functional Requirement (FR) | Yêu cầu chức năng hệ thống phải thực hiện. |
| Non-functional Requirement (NFR) | Yêu cầu về chất lượng hoặc giới hạn vận hành có thể đo lường. |
| MoSCoW | Phương pháp phân mức ưu tiên: MUST, SHOULD, COULD, WON’T. |
| Actor | Vai trò bên ngoài tương tác với hệ thống. |
| Use Case (UC) | Mô tả một chức năng theo góc nhìn tác nhân sử dụng. |
| Nhóm sự cố | Nhãn phân loại lỗi, gồm MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO và KHAC. |
| Mức ưu tiên | Mức độ cần ưu tiên xử lý yêu cầu theo quy tắc nghiệp vụ. |
| Macro F1 | Chỉ số đánh giá phân loại, tính F1 cho từng lớp rồi lấy trung bình không trọng |

## 1.2 Các bên liên quan và vai trò người dùng

## 1.3 Yêu cầu chức năng và User Story

### 1.3.1 Yêu cầu chức năng

| Mã | Yêu cầu chức năng | Tiêu chí kiểm chứng |
|---|---|---|
| FR01 | Hệ thống phải cho phép nhân viên nhập mô tả lỗi do khách hàng cung cấp. | Khi mô tả hợp lệ được gửi, hệ thống tiếp nhận nội dung để xử lý. |
| FR02 | Hệ thống phải tự động đề xuất nhóm sự cố dựa trên mô tả lỗi. | Với đầu vào hợp lệ, hệ thống trả về một trong sáu nhóm sự cố đã định nghĩa hoặc thông báo không đủ độ tin cậy. |
| FR03 | Hệ thống phải đề xuất mức độ ưu tiên của yêu cầu bảo hành. | Với thông tin đáp ứng điều kiện của quy tắc, hệ thống hiển thị mức ưu tiên tương ứng. |
| FR04 | Hệ thống phải hiển thị nhóm sự cố và mức độ ưu tiên được đề xuất để nhân viên kiểm tra. | Kết quả được hiển thị trước khi nhân viên xác nhận yêu cầu. |
| FR05 | Hệ thống phải cho phép nhân viên điều chỉnh nhóm sự cố hoặc mức độ ưu tiên. | Sau khi điều chỉnh hợp lệ, hệ thống hiển thị giá trị đã sửa. |
| FR06 | Hệ thống phải cho phép quản lý xem danh sách các yêu cầu bảo hành đã được phân loại. | Danh sách hiển thị các yêu cầu đã lưu cùng thông tin phân loại liên quan. |
| FR07 | Hệ thống phải cho phép quản lý xem lịch sử phân loại và các trường hợp điều chỉnh kết quả. | Khi quản lý mở lịch sử, hệ thống hiển thị các bản ghi lịch sử có sẵn và thông tin điều chỉnh được lưu. Nếu chưa có lịch sử, hệ thống thông báo chưa có dữ liệu. |

### 1.3.2 User Story

| Mã | User Story | MoSCoW |
|---|---|---|
| US1 | Là nhân viên tiếp nhận bảo hành, tôi muốn nhập mô tả lỗi do khách hàng cung cấp để hệ thống có dữ liệu phân tích và phân loại yêu cầu bảo hành. | MUST |
| US2 | Là nhân viên tiếp nhận bảo hành, tôi muốn hệ thống tự động đề xuất nhóm sự cố dựa trên mô tả lỗi để giảm thời gian phân loại yêu cầu. | MUST |
| US3 | Là nhân viên tiếp nhận bảo hành, tôi muốn hệ thống đề xuất mức độ ưu tiên của yêu cầu bảo hành để hỗ trợ xác định thứ tự xử lý. | SHOULD |
| US4 | Là nhân viên tiếp nhận bảo hành, tôi muốn xem kết quả phân loại và mức ưu tiên được hệ thống đề xuất để kiểm tra trước khi xác nhận yêu cầu. | MUST |
| US5 | Là nhân viên tiếp nhận bảo hành, tôi muốn điều chỉnh nhóm sự cố hoặc mức ưu tiên khi kết quả đề xuất chưa phù hợp để đảm bảo thông tin bảo hành chính xác. | SHOULD |
| US6 | Là quản lý bảo hành, tôi muốn xem danh sách các yêu cầu đã được phân loại theo nhóm sự cố và mức ưu tiên để theo dõi tình hình tiếp nhận và xử lý bảo hành. | SHOULD |
| US7 | Là quản lý bảo hành, tôi muốn xem lịch sử kết quả phân loại và các trường hợp nhân viên điều chỉnh kết quả để đánh giá và cải thiện chất lượng phân loại. | COULD |

## 1.4 Yêu cầu phi chức năng

| Mã | Yêu cầu phi chức năng | Ngưỡng |
|---|---|---|
| NFR01 | Thời gian phản hồi khi thực hiện phân loại một yêu cầu phải đáp ứng nhu cầu tiếp nhận | Không quá 5 giây/yêu cầu trong môi trường thử nghiệm |
| NFR02 | Hệ thống phải hỗ trợ xử lý bộ dữ liệu mẫu của case study. | Đọc và xử lý được tối thiểu 4.000 bản ghi dữ liệu mẫu |
| NFR03 | Hệ thống hỡ trợ dùng đồng thời | Hỗ trợ ít nhất 10 người dùng đồng thời |
| NFR04 | Giao diện phải hiển thị danh sách yêu cầu đã lưu trong thời gian phù hợp | Thời gian tải danh sách không quá 3 giây với bộ dữ liệu thử nghiệm 4.000 bản ghi |
| NFR05 | Mô hình phân loại phải đạt mức chất lượng tối thiểu trước khi được xem là đáp ứng yêu cầu thử nghiệm | Macro F1 trên tập kiểm thử đạt tối thiểu 0,70 |

## 1.5 Ràng buộc và quy tắc nghiệp vụ

| Mã | Ràng buộc và quy tắc nghiệp vụ |
|---|---|
| BR01 – Danh mục nhóm sự cố | Mô hình chỉ được đề xuất một trong sáu nhãn: MAN_HINH, PIN, SAC, PHAN_MEM, NUOC_VAO hoặc KHAC. Nếu nội dung không phù hợp với các nhóm đã định nghĩa, cần xử lý theo nhãn KHAC hoặc yêu cầu nhân viên kiểm tra lại. |
| BR02 – Ngưỡng tin cậy của mô hình | Nếu độ tin cậy của dự đoán đạt từ 0,70 trở lên, hệ thống có thể hiển thị nhóm sự cố như một gợi ý. Nếu thấp hơn 0,70, hệ thống không tự động điền nhóm sự cố như kết quả đã được xác nhận và yêu cầu nhân viên kiểm tra, lựa chọn. |
| BR03 – Xác nhận của nhân viên | Kết quả do mô hình đề xuất không phải kết luận cuối cùng. Nhân viên phải kiểm tra và xác nhận trước khi lưu kết quả phân loại chính thức. |
| BR04 – Xác định mức ưu tiên | Mức ưu tiên được đề xuất theo quy tắc nghiệp vụ đã cấu hình; không được coi là đầu ra của mô hình học máy khi chưa có bộ dữ liệu nhãn ưu tiên được xác thực. |
| BR05 – Phạm vi sử dụng dữ liệu | Dữ liệu mô tả lỗi dùng cho huấn luyện và đánh giá phải được kiểm tra, hạn chế thông tin định danh cá nhân và giữ riêng tập huấn luyện, kiểm định, kiểm thử để tránh rò rỉ dữ liệu. |

## 1.6 BẢNG TRUY VẾT (FR <-> US <-> Use Case <-> MoSCoW)

| FR | User Story | Use Case | MoSCoW |
|---|---|---|---|
| FR01 | US1 | UC01 – Tiếp nhận yêu cầu bảo hành | MUST |
| FR02 | US2 | UC02 – Tự động phân loại yêu cầu bảo hành | MUST |
| FR03 | US3 | UC02 – Tự động phân loại yêu cầu bảo hành | SHOULD |
| FR04 | US4 | UC03 – Xem kết quả phân loại | MUST |
| FR05 | US5 | UC04 – Điều chỉnh kết quả phân loại | SHOULD |
| FR06 | US6 | UC06 – Xem danh sách yêu cầu bảo hành | SHOULD |
| FR07 | US7 | UC07 – Xem lịch sử phân loại | COULD |