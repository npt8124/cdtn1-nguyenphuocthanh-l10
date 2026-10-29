
import json
from html import escape
from pathlib import Path

import streamlit as st


REPORT_PATH = Path("reports/metrics.json")


def read_report(path=REPORT_PATH):
    """Đọc báo cáo thật, phân biệt trạng thái rỗng và lỗi."""
    path = Path(path)

    if not path.is_file():
        return "empty", None, (
            "Chưa có báo cáo đánh giá. "
            "Hãy chạy lệnh huấn luyện để tạo metrics.json."
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict) or not data:
            return "empty", None, "Báo cáo chưa có dữ liệu."

        required = [
            "f1_macro_mo_hinh_chinh",
            "accuracy_mo_hinh_chinh",
            "f1_macro_baseline_da_so",
            "classification_report",
            "confusion_matrix",
            "so_sanh_mo_hinh_validation",
            "nhan",
            "trang_thai_tung_nhan",
        ]

        missing = [key for key in required if key not in data]

        if missing:
            return (
                "error",
                None,
                "Báo cáo thiếu trường: " + ", ".join(missing),
            )

        labels = data["nhan"]
        matrix = data["confusion_matrix"]

        if (
            not isinstance(labels, list)
            or not labels
            or not isinstance(matrix, list)
            or len(matrix) != len(labels)
            or any(
                not isinstance(row, list)
                or len(row) != len(labels)
                for row in matrix
            )
        ):
            return (
                "error",
                None,
                "Confusion matrix hoặc danh sách nhãn không hợp lệ.",
            )

        if not isinstance(
            data["so_sanh_mo_hinh_validation"], list
        ):
            return "error", None, "Danh sách mô hình không hợp lệ."

        if not isinstance(
            data["trang_thai_tung_nhan"], dict
        ):
            return "error", None, "Dữ liệu từng nhãn không hợp lệ."

        return "success", data, None

    except json.JSONDecodeError:
        return (
            "error",
            None,
            "Tệp metrics.json không phải JSON hợp lệ.",
        )
    except (OSError, UnicodeError) as exc:
        return "error", None, f"Không thể đọc báo cáo: {exc}"


def render_table(headers, rows):
    """Hiển thị bảng HTML không cần pandas/pyarrow."""
    html = [
        '<div style="overflow-x:auto;">',
        '<table style="width:100%;border-collapse:collapse;">',
        "<thead><tr>",
    ]

    for header in headers:
        html.append(
            '<th style="border-bottom:1px solid #888;'
            'padding:9px;text-align:left;">'
            + escape(str(header))
            + "</th>"
        )

    html.append("</tr></thead><tbody>")

    for row in rows:
        html.append("<tr>")

        for value in row:
            html.append(
                '<td style="border-bottom:1px solid #8884;'
                'padding:9px;">'
                + escape(str(value))
                + "</td>"
            )

        html.append("</tr>")

    html.append("</tbody></table></div>")

    st.markdown("".join(html), unsafe_allow_html=True)


def show_model_comparison(data):
    st.subheader("So sánh các mô hình trên Validation")

    candidates = data["so_sanh_mo_hinh_validation"]
    selected = data.get("chon_mo_hinh_tren_validation")

    if not candidates:
        st.warning("Chưa có kết quả so sánh mô hình.")
        return

    rows = []

    for item in candidates:
        name = item["model"]
        score = float(item["f1_macro_validation"])

        rows.append([
            name,
            f"{score:.4f}",
            "Được chọn" if name == selected else "",
        ])

    render_table(
        ["Mô hình", "Macro F1 – Validation", "Lựa chọn"],
        rows,
    )

    if selected:
        st.info(f"Mô hình được chọn: {selected}")

    st.caption(
        "Các mô hình ứng viên được lựa chọn dựa trên Validation. "
        "Test không được dùng để lựa chọn siêu tham số."
    )


def show_test_metrics(data):
    st.subheader("Kết quả đánh giá trên Test")

    f1 = float(data["f1_macro_mo_hinh_chinh"])
    accuracy = float(data["accuracy_mo_hinh_chinh"])
    dummy = float(data["f1_macro_baseline_da_so"])

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Macro F1 – Test",
        f"{f1:.4f}",
        delta=f"{f1 - dummy:+.4f} so với Dummy",
    )

    
    dummy_accuracy = data.get("accuracy_baseline_da_so")

    if dummy_accuracy is not None:
        col2.metric(
            "Accuracy – Test",
            f"{accuracy:.4f}",
            delta=(
                f"{accuracy - float(dummy_accuracy):+.4f} "
                "so với Dummy"
            ),
        )
    else:
        col2.metric(
            "Accuracy – Test",
            f"{accuracy:.4f}",
        )


    col3.metric(
        "Macro F1 – Dummy",
        f"{dummy:.4f}",
    )

    st.caption(
        "Accuracy và Macro F1 được đo trên cùng tập Test. "
        "Macro F1 của DummyClassifier là mốc so sánh "
        "cho mô hình chính; Accuracy là chỉ số bổ sung."
    )

    baseline_logistic = data.get(
        "f1_macro_baseline_tfidf_logistic"
    )

    if baseline_logistic is not None:
        st.write(
            "Macro F1 – Logistic Regression baseline: "
            f"{float(baseline_logistic):.4f}"
        )

    train = data.get("so_mau_train")
    val = data.get("so_mau_val")
    test = data.get("so_mau_test")

    st.caption(
        f"Số mẫu Train / Validation / Test: "
        f"{train} / {val} / {test}"
    )


def show_label_metrics(data):
    st.subheader("Chỉ số theo từng nhãn")

    labels = data["nhan"]
    statuses = data["trang_thai_tung_nhan"]

    rows = []
    warnings = []

    for label in labels:
        item = statuses.get(label)

        if item is None:
            warnings.append(
                f"Nhãn {label} không có thông tin đánh giá."
            )
            continue

        status = item["status"]

        if status == "KHONG_CO_DU_LIEU":
            display_status = "Thiếu dữ liệu"
            warnings.append(
                f"{label}: không có mẫu trong Test."
            )
        elif status == "F1_BANG_0":
            display_status = "F1 = 0"
            warnings.append(
                f"{label}: có dữ liệu nhưng F1 bằng 0."
            )
        else:
            display_status = "Có dữ liệu"

        rows.append([
            label,
            item["support"],
            f"{float(item['precision']):.4f}",
            f"{float(item['recall']):.4f}",
            f"{float(item['f1']):.4f}",
            display_status,
        ])

    render_table(
        [
            "Nhãn",
            "Support",
            "Precision",
            "Recall",
            "F1",
            "Trạng thái",
        ],
        rows,
    )

    for warning in warnings:
        st.warning(warning)

    if not warnings:
        st.success(
            "Tất cả nhãn đều có dữ liệu trong Test "
            "và có F1 lớn hơn 0."
        )

    st.caption(
        "Support là số mẫu thực tế của từng nhãn. "
        "F1 = 0 và Support = 0 là hai tình trạng khác nhau."
    )


def show_confusion_matrix(data):
    st.subheader("Confusion matrix – Test")

    labels = data["nhan"]
    matrix = data["confusion_matrix"]

    rows = []

    for label, values in zip(labels, matrix):
        rows.append([label] + values)

    render_table(
        ["Thực tế / Dự đoán"] + labels,
        rows,
    )

    st.caption(
        "Hàng là nhãn thực tế, cột là nhãn dự đoán. "
        "Đường chéo chính thể hiện số mẫu dự đoán đúng."
    )


def show_report():
    st.header("Báo cáo đánh giá mô hình")

    # Trạng thái đang tải
    with st.spinner("Đang tải báo cáo đánh giá..."):
        status, data, message = read_report()

    # Trạng thái rỗng
    if status == "empty":
        st.info(message)
        st.code(
            "python -m src.models.train --config configs/train.yaml",
            language="powershell",
        )
        return

    # Trạng thái lỗi
    if status == "error":
        st.error(message)
        st.info(
            "Kiểm tra reports/metrics.json hoặc "
            "chạy lại script huấn luyện."
        )
        return

    try:
        st.success("Đã tải báo cáo đánh giá.")

        show_model_comparison(data)
        st.divider()

        show_test_metrics(data)
        st.divider()

        show_label_metrics(data)
        st.divider()

        show_confusion_matrix(data)

        st.caption(
            "Nguồn dữ liệu: reports/metrics.json"
        )

    except (KeyError, TypeError, ValueError, IndexError) as exc:
        st.error(
            "Báo cáo có cấu trúc hoặc giá trị không hợp lệ: "
            f"{exc}"
        )
