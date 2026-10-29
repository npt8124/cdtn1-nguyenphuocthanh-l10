
import pytest

from src.models.predict import load_model, predict


@pytest.fixture(scope="module")
def model_bundle():
    """
    Tải mô hình đã huấn luyện một lần cho toàn bộ test.
    Yêu cầu chạy train.py trước khi kiểm thử.
    """
    return load_model()


# =====================================================
# LOẠI 1: LUỒNG ĐÚNG
# =====================================================

def test_TC01_du_doan_mo_ta_hop_le(model_bundle):
    """
    Nhập mô tả hợp lệ.
    Hệ thống phải trả về nhãn thuộc 6 nhóm sự cố.
    """
    description = "Màn hình điện thoại xuất hiện sọc xanh"

    result = predict(model_bundle, description)

    assert result["label"] in model_bundle["labels"]
    assert result["confidence"] is None or (
        0.0 <= result["confidence"] <= 1.0
    )
    assert isinstance(result["needs_review"], bool)


def test_TC02_du_doan_loi_sac(model_bundle):
    """
    Nhập mô tả lỗi sạc.
    Kiểm tra hệ thống phân loại đúng nhóm SAC.
    """
    description = "Chân sạc bị lỏng phải giữ mới sạc được"

    result = predict(model_bundle, description)

    assert result["label"] == "SAC"


# =====================================================
# LOẠI 2: GIÁ TRỊ BIÊN
# =====================================================

def test_TC03_mo_ta_dung_10_ky_tu(model_bundle):
    """Giá trị biên: đúng 10 ký tự, được chấp nhận."""
    description = "pin bi loi"

    assert len(description) == 10

    result = predict(model_bundle, description)

    assert result["label"] in model_bundle["labels"]


def test_TC04_mo_ta_duoi_10_ky_tu(model_bundle):
    """Giá trị biên: 9 ký tự, phải từ chối."""
    description = "pin bi hu"

    assert len(description) == 9

    with pytest.raises(
        ValueError,
        match="ít nhất 10 ký tự"
    ):
        predict(model_bundle, description)


# =====================================================
# LOẠI 3: DỮ LIỆU SAI
# =====================================================

def test_TC05_mo_ta_rong(model_bundle):
    """Dữ liệu sai: không nhập mô tả."""

    with pytest.raises(
        ValueError,
        match="Vui lòng nhập mô tả lỗi"
    ):
        predict(model_bundle, "")


def test_TC06_mo_ta_chi_co_khoang_trang(model_bundle):
    """Dữ liệu sai: mô tả chỉ chứa khoảng trắng."""

    with pytest.raises(
        ValueError,
        match="Vui lòng nhập mô tả lỗi"
    ):
        predict(model_bundle, "    \n\t    ")

def test_TC07_ky_tu_vo_nghia(model_bundle):
    with pytest.raises(ValueError):
        predict(model_bundle, "^$ư4r")