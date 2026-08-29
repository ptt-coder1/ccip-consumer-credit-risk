"""
extract_homecredit.py — Giai đoạn 1 [E] Extract
Tải bộ dữ liệu Home Credit Default Risk từ Kaggle về thư mục data/raw/.

Yêu cầu:
  - Đã có KAGGLE_USERNAME và KAGGLE_KEY trong .env
  - Hoặc có file ~/.kaggle/kaggle.json (nếu đã cài Kaggle CLI trước)

Cách chạy:
  python extract/extract_homecredit.py
"""

import os
import sys
import zipfile
from pathlib import Path

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# -----------------------------------------------------------
# Cấu hình
# -----------------------------------------------------------
KAGGLE_DATASET = "competitions/home-credit-default-risk"
DATA_DIR = ROOT_DIR / "data" / "raw" / "home_credit"

# Danh sách file cần dùng trong dự án (bộ đầy đủ có ~10 file)
# Chỉ tải các file chính để tiết kiệm dung lượng
REQUIRED_FILES = [
    "application_train.csv",   # Bảng chính: mỗi dòng = 1 đơn vay (có nhãn TARGET)
    "application_test.csv",    # Bảng test (không có TARGET — dùng để validate)
    "bureau.csv",              # Lịch sử tín dụng tại các tổ chức tín dụng khác
    "bureau_balance.csv",      # Số dư tài khoản tín dụng theo tháng
    "previous_application.csv",# Đơn vay cũ tại chính Home Credit
    "installments_payments.csv",# Lịch sử trả góp
    "credit_card_balance.csv", # Số dư thẻ tín dụng theo tháng
    "POS_CASH_balance.csv",    # Số dư POS/cash loan theo tháng
]


def setup_kaggle_env():
    """Thiết lập biến môi trường Kaggle nếu dùng .env thay vì kaggle.json."""
    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")

    if username and key:
        os.environ["KAGGLE_USERNAME"] = username
        os.environ["KAGGLE_KEY"] = key
        return True

    # Kiểm tra file kaggle.json mặc định
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if kaggle_json.exists():
        print("  ℹ️  Dùng ~/.kaggle/kaggle.json để xác thực")
        return True

    print("❌  Chưa có thông tin xác thực Kaggle!")
    print("    Cách 1: Thêm KAGGLE_USERNAME và KAGGLE_KEY vào file .env")
    print("    Cách 2: Tải kaggle.json từ kaggle.com/settings → API")
    print("            rồi đặt vào C:\\Users\\<tên>\\.kaggle\\kaggle.json")
    return False


def download_dataset():
    """Tải dataset Home Credit từ Kaggle về data/raw/home_credit/."""
    import kaggle  # import sau khi set env vars

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*55}")
    print("  CCIP — Extract: Home Credit Default Risk")
    print(f"{'='*55}")
    print(f"  Thư mục lưu: {DATA_DIR}\n")

    # Tải từng file thay vì tải cả competition (tránh tải những file không cần)
    # Kaggle API: kaggle competitions download -c home-credit-default-risk -f <file>
    for filename in REQUIRED_FILES:
        dest_file = DATA_DIR / filename
        if dest_file.exists():
            print(f"  ⏭️   {filename} — đã có, bỏ qua")
            continue

        print(f"  ⬇️   Đang tải {filename}...")
        try:
            kaggle.api.competition_download_file(
                competition="home-credit-default-risk",
                file_name=filename,
                path=str(DATA_DIR),
                quiet=False,
                force=False,
            )
            # File tải về có thể ở dạng .zip — giải nén
            zip_path = DATA_DIR / (filename + ".zip")
            if zip_path.exists():
                print(f"       Giải nén {zip_path.name}...")
                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(DATA_DIR)
                zip_path.unlink()  # Xóa file zip sau khi giải nén
            print(f"  ✅  {filename} — tải xong")
        except Exception as e:
            print(f"  ❌  Lỗi khi tải {filename}: {e}")

    # Kiểm tra kết quả
    print(f"\n  Tổng kết:")
    for filename in REQUIRED_FILES:
        status = "✅" if (DATA_DIR / filename).exists() else "❌"
        size = ""
        if (DATA_DIR / filename).exists():
            mb = (DATA_DIR / filename).stat().st_size / 1_048_576
            size = f"({mb:.1f} MB)"
        print(f"    {status}  {filename} {size}")


if __name__ == "__main__":
    if not setup_kaggle_env():
        sys.exit(1)
    download_dataset()
    print("\n✅  Extract Home Credit hoàn thành!\n")
