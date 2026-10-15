# Nhật ký thay đổi thiết kế
## Sau phản hồi Bài tập 1 (buổi 6, ngày 15/10/2026)
### TD-01 Thay đổi lỗi nhất quán NFR03 thành NFR04 trong SRS
- Phản hồi của GV : Lập luận 3 ghi "NFR03 yêu cầu tải danh sách ≤ 3 giây", nhưng trong SRS đó là NFR04; NFR03 là 10 người dùng đồng thời. Mã NFR phải khớp.
- Quyết định : SỬA
- Lý do : Đúng sự nhất quán.
- Ảnh hưởng : Cập nhật SRS.
### TD-02 Thêm chú thích cho sơ đồ ML pipeline mục 4
- Phản hồi của GV : Sơ đồ ML pipeline ở Mục 4 chưa có chú thích ký hiệu.
- Quyết định : SỬA
- Lý do : Cần chú thích để hiểu rõ sơ đồ
- Ảnh hưởng : Không. 
### TD-03 Thêm phần ngoài phạm vi cho sơ đồ kiến trúc
- Phản hồi của GV : Sơ đồ kiến trúc chưa có dòng ghi phần ngoài phạm vi.
- Quyết định : SỬA
- Lý do : Thêm phần ngoài phạm vi theo đúng yêu cầu.
- Ảnh hưởng : Không. 
### TD-04 Xóa US8
- Phản hồi của GV : Có 8 User Story, đề yêu cầu 5–7.
- Quyết định : SỬA
- Lý do : Đề chỉ yêu cầu 5-7 US nhưng lại có 8 US.
- Ảnh hưởng : Cập nhật SRS
### TD-05 Thay đổi bảng thuật ngữ
- Phản hồi của GV : Bảng thuật ngữ nên tập trung thuật ngữ nghiệp vụ (mô tả lỗi, nhóm sự cố, độ tin cậy, mức ưu tiên), bớt các từ như SRS, FR, Actor.
- Quyết định : SỬA
- Lý do : Bỏ bớt các thuật ngữ không có trong chuyên môn nghiệp vụ
- Ảnh hưởng : Cập nhật SRS
### TD-06 Bổ sung các file và tập commit chuẩn hơn
- Phản hồi của GV : Repo thiếu .gitignore, thiếu file gốc của sơ đồ ML pipeline; commit message chưa theo chuẩn.
- Quyết định : SỬA
- Lý do : Cần bổ sung file cần thiết, commit chuẩn.
- Ảnh hưởng : Sửa lại các file, cập nhật SRS.