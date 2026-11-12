# BUG LOG - HỆ THỐNG TỰ ĐỘNG PHÂN LOẠI YÊU CẦU BẢO HÀNH

## BUG-01 — Từ chối mô tả có đúng 10 ký tự

1. **Mã và mức độ:** BUG-01 · MAJOR — Người dùng không thể phân loại mô tả hợp lệ có độ dài đúng bằng ngưỡng tối thiểu.

2. **Phát hiện bởi:** TC-03 — Mô tả đủ 10 ký tự (`tests/test_predict.py::test_TC03_mo_ta_dung_10_ky_tu`).

3. **Triệu chứng:** Mô tả `"pin bi loi"` có đúng 10 ký tự nhưng hệ thống phát sinh `ValueError`, yêu cầu mô tả phải có ít nhất 10 ký tự.

4. **Cách tái lập:** Thay điều kiện `len(cleaned) < MIN_LENGTH` thành `len(cleaned) <= MIN_LENGTH`, sau đó chạy `python -m pytest -v tests/test_predict.py::test_TC03_mo_ta_dung_10_ky_tu`. Kết quả: FAIL.

5. **Nguyên nhân:** Điều kiện kiểm tra độ dài sử dụng toán tử `<=` thay vì `<`, khiến giá trị bằng ngưỡng `MIN_LENGTH = 10` bị đánh giá nhầm là không hợp lệ.

6. **Cách sửa:** Thay toán tử `<=` bằng `<` trong hàm `validate_description()`, bảo đảm chỉ từ chối mô tả có độ dài dưới 10 ký tự. Chạy lại TC-03: PASS.

7. **Commit và xác nhận:** https://github.com/npt8124/cdtn1-nguyenphuocthanh-l10/commit/d424e086b1d0d4e1aaa97b9e654d45f485f1cdc5. TC-03 PASS sau sửa; 9/11 test PASS.

---

## BUG-02 — Chấp nhận mô tả chỉ chứa khoảng trắng

1. **Mã và mức độ:** BUG-02 · MAJOR — Hệ thống có thể tiếp nhận mô tả không chứa nội dung thực tế, ảnh hưởng đến chất lượng dữ liệu đầu vào của mô hình.

2. **Phát hiện bởi:** TC-06 — Mô tả chỉ có khoảng trống (`tests/test_predict.py::test_TC06_mo_ta_chi_co_khoang_trang`).

3. **Triệu chứng:** Khi nhập chuỗi chỉ chứa dấu cách, tab và ký tự xuống dòng, hệ thống không phát sinh thông báo yêu cầu nhập mô tả lỗi.

4. **Cách tái lập:** Thay điều kiện `if not description.strip()` thành `if description == ""`, sau đó chạy `python -m pytest -v tests/test_predict.py::test_TC06_mo_ta_chi_co_khoang_trang`. Kết quả: FAIL.

5. **Nguyên nhân:** Hàm `validate_description()` chỉ so sánh đầu vào với chuỗi rỗng `""`, không chuẩn hóa hoặc kiểm tra nội dung sau khi loại bỏ khoảng trắng bằng `strip()`.

6. **Cách sửa:** Sử dụng `if not description.strip()` để từ chối cả chuỗi rỗng và chuỗi chỉ chứa khoảng trắng. Chạy lại TC-06: PASS.

7. **Commit và xác nhận:** https://github.com/npt8124/cdtn1-nguyenphuocthanh-l10/commit/a1d902104bf751fbd9fba8a297e0b8d991e2b132. TC-06 PASS sau sửa; 10/11 test PASS.

---

## BUG-03 — Chấp nhận mô tả chứa quá nhiều ký tự đặc biệt

1. **Mã và mức độ:** BUG-03 · MAJOR — Dữ liệu không đáp ứng yêu cầu mô tả sự cố vẫn có thể được đưa vào mô hình phân loại, làm giảm độ tin cậy của kết quả dự đoán.

2. **Phát hiện bởi:** TC-07 — Ký tự vô nghĩa (`tests/test_predict.py::test_TC07_ky_tu_vo_nghia`).

3. **Triệu chứng:** Khi nhập mô tả `"^$ư4grge$^%&GR#r"`, hệ thống không phát sinh `ValueError` với thông báo mô tả chứa quá nhiều ký tự đặc biệt.

4. **Cách tái lập:** Thay ngưỡng kiểm tra `special_count / len(raw) > 0.4` thành `special_count / len(raw) > 1.0`, sau đó chạy `python -m pytest -v tests/test_predict.py::test_TC07_ky_tu_vo_nghia`. Kết quả: FAIL.

5. **Nguyên nhân:** Ngưỡng tỷ lệ ký tự đặc biệt trong hàm `validate_description()` bị cấu hình sai thành `1.0` thay vì `0.4`, khiến nhiều mô tả không hợp lệ vượt qua bước kiểm tra dữ liệu đầu vào.

6. **Cách sửa:** Khôi phục ngưỡng kiểm tra về `0.4`, bảo đảm mô tả có tỷ lệ ký tự đặc biệt vượt quá 40% bị từ chối. Chạy lại TC-07: PASS.

7. **Commit và xác nhận:** https://github.com/npt8124/cdtn1-nguyenphuocthanh-l10/commit/2910c6ea721015c2655782cc22d5683929c2175c. TC-07 PASS sau sửa; 11/11 test PASS.