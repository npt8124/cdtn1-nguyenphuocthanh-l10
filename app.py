
import streamlit as st

from src.models.predict import load_model, predict
from src.ui.report import show_report
from src.data.database import (
    initialize,
    save_request,
    list_requests,
    list_history,
)

st.set_page_config(
    page_title="L10 – Phân loại bảo hành",
    layout="wide",
)

LABEL_NAMES = {
    "MAN_HINH": "Màn hình",
    "PIN": "Pin",
    "SAC": "Sạc",
    "PHAN_MEM": "Phần mềm",
    "NUOC_VAO": "Nước vào",
    "KHAC": "Khác",
}

PRIORITIES = ["Thấp", "Trung bình", "Cao"]


@st.cache_resource
def get_model():
    return load_model()


def suggest_priority(description):
    """Quy tắc minh họa, không phải dự đoán ML."""
    text = description.lower()

    urgent_terms = [
        "khẩn cấp",
        "nguy hiểm",
        "cháy",
        "bốc khói",
        "nóng bất thường",
    ]

    if any(term in text for term in urgent_terms):
        return "Cao"

    return "Trung bình"


def display_scores(result):
    scores = result.get("scores", [])
    score_type = result.get("score_type")

    st.subheader("Điểm dự đoán theo nhóm sự cố")

    if not scores:
        st.warning(
            "Mô hình không cung cấp điểm theo từng nhãn."
        )
        return

    if score_type == "probability":
        st.caption(
            "Tỷ lệ ước lượng của mô hình, "
            "chưa hiệu chuẩn thành xác suất đúng thực tế."
        )

        for item in scores:
            label = item["label"]
            value = item["score"]

            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(
                    f"**{LABEL_NAMES.get(label, label)}**"
                )
                st.progress(
                    min(max(float(value), 0.0), 1.0)
                )

            with col2:
                st.write(f"{value:.2%}")

    elif score_type == "decision":
        st.info(
            "LinearSVC cung cấp điểm quyết định, "
            "không phải xác suất. "
            "Các điểm không được biểu diễn dưới dạng %."
        )

        for item in scores:
            label = item["label"]
            st.write(
                f"{LABEL_NAMES.get(label, label)}: "
                f"{item['score']:.4f}"
            )


def show_prediction():
    st.header("Tiếp nhận và phân loại yêu cầu")

    text = st.text_area(
        "Mô tả lỗi khách hàng",
        placeholder=(
            "Ví dụ: Điện thoại vẫn đổ chuông "
            "nhưng màn hình tối đen"
        ),
        height=120,
        key="issue_description",
    )

    try:
        with st.spinner("Đang tải mô hình..."):
            bundle = get_model()
    except Exception as exc:
        st.error(f"Không thể tải mô hình: {exc}")
        st.code(
            "python -m src.models.train "
            "--config configs/train.yaml",
            language="powershell",
        )
        return

    if st.button("Phân loại", type="primary"):
        st.session_state.pop("last_prediction", None)

        with st.spinner("Đang phân loại..."):
            try:
                result = predict(bundle, text)
                st.session_state["last_prediction"] = {
                    "text": text,
                    "result": result,
                }
            except ValueError as exc:
                st.error(str(exc))
            except Exception:
                st.error(
                    "Không thể dự đoán. "
                    "Vui lòng kiểm tra mô hình."
                )

    last = st.session_state.get("last_prediction")

    if last is None or last["text"] != text:
        st.info(
            "Nhập mô tả hợp lệ và chọn Phân loại "
            "để xem kết quả."
        )
        return

    result = last["result"]

    st.divider()
    st.subheader("Kết quả phân loại")

    predicted_label = result["label"]

    st.success(
        "Nhóm AI đề xuất: "
        f"{LABEL_NAMES.get(predicted_label, predicted_label)}"
    )

    display_scores(result)

    if result.get("needs_review", True):
        st.warning(
            "Kết quả cần được nhân viên kiểm tra."
        )
    else:
        st.info(
            "Điểm dự đoán đạt ngưỡng tham khảo. "
            "Nhân viên vẫn cần xác nhận."
        )

    st.divider()
    st.subheader("Điều chỉnh và xác nhận kết quả")

    labels = list(bundle.get("labels", []))

    if not labels:
        labels = [
            item["label"]
            for item in result.get("scores", [])
        ]

    if predicted_label not in labels:
        st.error(
            "Nhãn dự đoán không nằm trong danh sách "
            "nhãn hợp lệ."
        )
        return

    suggested_priority = suggest_priority(text)

    with st.form("confirm_form"):
        final_label = st.selectbox(
            "Nhóm sự cố sau khi kiểm tra",
            options=labels,
            index=labels.index(predicted_label),
            format_func=lambda label: (
                LABEL_NAMES.get(label, label)
            ),
        )

        st.caption(
            "Mức ưu tiên do quy tắc nghiệp vụ "
            "minh họa đề xuất, không phải ML."
        )

        final_priority = st.selectbox(
            "Mức ưu tiên",
            options=PRIORITIES,
            index=PRIORITIES.index(
                suggested_priority
            ),
        )

        confirmed = st.form_submit_button(
            "Xác nhận và lưu kết quả",
            type="primary",
        )

    if confirmed:
        try:
            request_id = save_request(
                description=text,
                result=result,
                suggested_priority=suggested_priority,
                final_label=final_label,
                final_priority=final_priority,
            )

            st.success(
                f"Đã xác nhận yêu cầu #{request_id}."
            )

            st.session_state.pop(
                "last_prediction", None
            )
        except Exception as exc:
            st.error(
                f"Không thể lưu yêu cầu: {exc}"
            )


def show_requests():
    st.header("Danh sách yêu cầu bảo hành")

    try:
        rows = list_requests()
    except Exception as exc:
        st.error(f"Không thể tải danh sách: {exc}")
        return

    if not rows:
        st.info("Chưa có yêu cầu được xác nhận.")
        return

    st.caption(f"Tổng số yêu cầu: {len(rows)}")

    for row in rows:
        with st.expander(
            f"#{row['id']} – "
            f"{LABEL_NAMES.get(row['final_label'], row['final_label'])} "
            f"– {row['created_at']}"
        ):
            st.write(
                "**Mô tả:**", row["description"]
            )
            st.write(
                "**AI đề xuất:**",
                LABEL_NAMES.get(
                    row["suggested_label"],
                    row["suggested_label"],
                ),
            )
            st.write(
                "**Nhân viên xác nhận:**",
                LABEL_NAMES.get(
                    row["final_label"],
                    row["final_label"],
                ),
            )
            st.write(
                "**Mức ưu tiên:**",
                row["final_priority"],
            )


def show_history():
    st.header("Lịch sử phân loại")

    try:
        rows = list_history()
    except Exception as exc:
        st.error(f"Không thể tải lịch sử: {exc}")
        return

    if not rows:
        st.info("Chưa có lịch sử phân loại.")
        return

    for row in rows:
        if row["action"] == "CONFIRM":
            st.write(
                f"Yêu cầu #{row['request_id']}: "
                f"Đã xác nhận – {row['created_at']}"
            )
        else:
            st.write(
                f"Yêu cầu #{row['request_id']}: "
                f"Điều chỉnh {row['field']} "
                f"từ {row['old_value']} "
                f"sang {row['new_value']} "
                f"– {row['created_at']}"
            )


st.title("L10 – Tự động phân loại yêu cầu bảo hành")

st.caption(
    "Hệ thống hỗ trợ nhân viên phân loại và "
    "xác nhận yêu cầu bảo hành."
)

try:
    initialize()
    database_ready = True
except Exception as exc:
    database_ready = False
    st.error(f"Không thể khởi tạo SQLite: {exc}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Tiếp nhận và phân loại",
    "Danh sách yêu cầu",
    "Lịch sử phân loại",
    "Kết quả đánh giá ML",
])

with tab1:
    if database_ready:
        show_prediction()
    else:
        st.warning(
            "Chức năng lưu yêu cầu tạm thời không khả dụng."
        )

with tab2:
    if database_ready:
        show_requests()

with tab3:
    if database_ready:
        show_history()

with tab4:
    show_report()
