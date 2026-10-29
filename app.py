
import streamlit as st

from src.models.predict import load_model, predict
from src.ui.report import show_report


st.set_page_config(
    page_title="L10 – Phân loại bảo hành",
    layout="wide"
)

st.title("L10 – Tự động phân loại yêu cầu bảo hành")

st.caption(
    "Bản minh họa BT2: mô hình gợi ý nhóm sự cố; "
    "nhân viên cần kiểm tra kết quả. "
)


@st.cache_resource
def get_model():
    """Chỉ tải mô hình khi cần dự đoán."""
    return load_model()


def show_prediction():
    st.header("Thử dự đoán nhóm sự cố")

    st.info(
        "Nhập mô tả lỗi của khách hàng. "
        "Hệ thống sẽ đề xuất một trong các nhóm sự cố."
    )

    # Trạng thái chưa có dữ liệu đầu vào
    text = st.text_area(
        "Mô tả lỗi",
        placeholder=(
            "Ví dụ: Điện thoại vẫn đổ chuông "
            "nhưng màn hình tối đen"
        ),
        height=120,
        key="issue_description",
    )

    # Tải mô hình độc lập với trang báo cáo
    with st.spinner("Đang kiểm tra mô hình..."):
        try:
            bundle = get_model()
            model_error = None
        except Exception as exc:
            bundle = None
            model_error = str(exc)

    if bundle is None:
        st.error(
            "Không thể tải mô hình dự đoán: "
            f"{model_error}"
        )

        st.info(
            "Hãy chạy lệnh huấn luyện để tạo "
            "artifacts/warranty_model.joblib."
        )

        st.code(
            "python -m src.models.train --config configs/train.yaml",
            language="powershell",
        )

        return

    st.success("Mô hình đã sẵn sàng.")

    if st.button("Phân loại", type="primary"):
        # Xóa kết quả cũ trước khi xử lý lần mới
        st.session_state.pop("last_prediction", None)

        if not text.strip():
            st.warning(
                "Mô tả đang rỗng. Hãy nhập nội dung."
            )
        else:
            with st.spinner("Đang phân loại..."):
                try:
                    result = predict(bundle, text)

                    st.session_state["last_prediction"] = {
                        "text": text,
                        "result": result,
                    }

                except ValueError as exc:
                    st.error(
                        f"Không thể phân loại: {exc}"
                    )

                except Exception:
                    st.error(
                        "Đã xảy ra lỗi khi dự đoán. "
                        "Vui lòng kiểm tra mô hình "
                        "hoặc thử lại."
                    )

    last = st.session_state.get("last_prediction")

    # Không hiển thị kết quả cũ khi người dùng đổi nội dung
    if last is None or last["text"] != text:
        return

    result = last["result"]

    st.subheader("Kết quả phân loại")

    st.success(
        f"Nhóm đề xuất: {result['label']}"
    )

    confidence = result.get("confidence")

    if confidence is None:
        st.warning(
            "Mô hình không cung cấp xác suất dự đoán. "
            "Cần nhân viên kiểm tra thủ công."
        )
    else:
        st.metric(
            "Điểm dự đoán",
            f"{confidence:.1%}"
        )

        if not result.get(
            "confidence_calibrated", False
        ):
            st.caption(
                "Điểm dự đoán chưa được hiệu chuẩn "
                "thành xác suất đúng thực tế."
            )

        if result.get("needs_review", True):
            st.warning(
                "Cần kiểm tra thủ công; "
                "chưa đạt ngưỡng tham khảo."
            )
        else:
            st.info(
                "Đã đạt ngưỡng tham khảo, "
                "nhưng vẫn cần nhân viên xác nhận."
            )

    st.caption(
        "Hệ thống không tự động xác nhận "
        "hoặc từ chối bảo hành."
    )


# Hai trang hoạt động độc lập
tab_predict, tab_report = st.tabs([
    "Thử dự đoán",
    "Kết quả đánh giá",
])

with tab_predict:
    show_prediction()

with tab_report:
    show_report()
