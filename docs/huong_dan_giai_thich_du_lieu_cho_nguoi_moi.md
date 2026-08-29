# 📘 CẨM NANG TOÀN TẬP: GIẢI THÍCH DỮ LIỆU & KIẾN TRÚC DỰ ÁN CCIP
> **Dành cho người mới bắt đầu (Beginner-Friendly)**  
> *Không cần nền tảng sâu về kinh tế hay kỹ thuật dữ liệu vẫn có thể hiểu 100%.*

---

## MỤC LỤC
1. [Bối cảnh kinh doanh: Dự án này giải quyết bài toán gì?](#1-bối-cảnh-kinh-doanh)
2. [Từ điển thuật ngữ tài chính - kinh tế "bình dân học vụ"](#2-từ-điển-thuật-ngữ-kinh-tế)
3. [Kiến trúc 3 Schema (Raw -> Staging -> DW): Tại sao phải chia 3 tầng?](#3-kiến-trúc-3-schema)
4. [Mô hình Star Schema: Fact & Dimension là gì? Tại sao lại có?](#4-mô-hình-fact--dimension)
5. [Chi tiết từng Bảng & Ý nghĩa từng Biến số (Field-by-Field)](#5-chi-tiết-từng-biến-số)
6. [Tóm tắt luồng đi của dữ liệu từ A -> Z](#6-tóm-tắt-luồng-dữ-liệu)

---

<a name="1-bối-cảnh-kinh-doanh"></a>
## 1. BỐI CẢNH KINH DOANH: BÀI TOÁN TÍN DỤNG

Hãy tưởng tượng bạn mở một **công ty cho vay tài chính tiêu dùng** (giống như FE Credit hay Home Credit).
Mỗi ngày có hàng ngàn người đến xin vay tiền để:
- Mua xe máy, điện thoại trả góp
- Vay tiền mặt tiêu dùng cá nhân

### 🎯 Thách thức lớn nhất của bạn là gì?
- Nếu **cho vay quá dễ dãi**: Nhiều người không chịu trả hoặc không có khả năng trả $\rightarrow$ Công ty **mất vốn, phá sản** (Rủi ro vỡ nợ).
- Nếu **quá khắt khe**: Từ chối cả những người tốt $\rightarrow$ Công ty **mất khách hàng, không có doanh thu** từ lãi suất.

👉 **Mục tiêu của dự án CCIP:** Xây dựng một đường ống xử lý dữ liệu (Pipeline) và hệ thống phân tích thông minh giúp công ty:
1. Nhìn rõ chân dung ai là người hay trả trễ, ai là người đáng tin cậy.
2. Cảnh báo sớm các hồ sơ vay có rủi ro cao để đưa ra quyết định chuẩn xác.

---

<a name="2-từ-điển-thuật-ngữ-kinh-tế"></a>
## 2. TỪ ĐIỂN THUẬT NGỮ TÀI CHÍNH "BÌNH DÂN HỌC VỤ"

Nếu bạn không học kinh tế, hãy dùng các so sánh đời thường sau:

| Thuật ngữ | Tên tiếng Anh | Giải thích dễ hiểu nhất | Ví dụ thực tế |
| :--- | :--- | :--- | :--- |
| **Vỡ nợ (Default)** | *Default / Target = 1* | Người vay "bùng nợ" hoặc quá hạn quá lâu (thường >90 ngày) không trả được. | Vay 50 triệu mua xe nhưng sau 3 tháng không đóng tiền và tắt máy bỏ trốn. |
| **Khoản trả góp (Annuity)** | *AMT_ANNUITY* | Số tiền cố định mà người vay phải trả **mỗi tháng** (gồm cả gốc + lãi). | Vay 12 triệu trong 12 tháng, mỗi tháng trả đều đặn 1.2 triệu. |
| **Tỷ lệ Vay / Giá trị hàng (LTV)** | *Loan-to-Value (LTV)* | Tỷ lệ giữa **số tiền muốn vay** so với **giá trị thực của món hàng**. | Mua điện thoại 20 triệu, trả trước 2 triệu, vay 18 triệu $\rightarrow$ LTV = 18/20 = 90% (0.9). |
| **Khả năng trả nợ (DTI / Income to Annuity)** | *Income to Annuity* | Thu nhập hàng tháng gấp bao nhiêu lần số tiền phải trả góp hàng tháng. | Lương 15 triệu/tháng, góp 3 triệu/tháng $\rightarrow$ Tỷ lệ = 5 lần (An toàn). |
| **Trung tâm thông tin tín dụng (CIC / Bureau)** | *Credit Bureau* | Một tổ chức "ghi sổ đen/sổ đỏ" lịch sử vay nợ của mọi người dân ở tất cả các ngân hàng. | Bạn từng quỵt tiền bên ngân hàng A, khi sang công ty B vay, công ty B tra CIC là biết ngay. |
| **Điểm tín dụng bên ngoài (External Score)** | *EXT_SOURCE* | Điểm đánh giá độ uy tín do các công ty chấm điểm độc lập cung cấp (như điểm FICO, điểm tín dụng viễn thông). | Thang điểm từ 0.0 đến 1.0. Điểm 0.8 là rất uy tín, điểm 0.1 là rủi ro cao. |
| **Hệ số tương quan Point-Biserial** | *Point-Biserial Correlation* | Đo lường mức độ liên kết giữa **1 biến số đo lường liên tục** (như điểm tín dụng) và **1 biến nhị phân Có/Không** (như Vỡ nợ 1/0). | Hệ số = -0.22 cho thấy: Điểm tín dụng càng cao thì xác suất vỡ nợ càng giảm rõ rệt. |
| **Vay quay vòng (Revolving Loans)** | *Revolving Loan* | Giống như **Thẻ tín dụng (Credit Card)**. Bạn được cấp 1 hạn mức (ví dụ 20tr), tiêu bao nhiêu trả bấy nhiêu, trả xong hạn mức lại đầy. | Khác với Vay tiền mặt (Cash loan) nhận 1 cục rồi trả dần đến hết hợp đồng. |

---

<a name="3-kiến-trúc-3-schema"></a>
## 3. KIẾN TRÚC 3 SCHEMA: TẠI SAO PHẢI CHIA 3 TẦNG?

Trong cơ sở dữ liệu `ccip_dw`, dữ liệu được chia làm 3 "phòng/tầng" riêng biệt gọi là **Schema**:

```
[ Nguồn bên ngoài: Kaggle CSV, API ]
                 │
                 ▼ (1. Nạp nguyên vẹn)
        ┌──────────────────┐
        │   Schema: RAW    │  <-- Tầng "Kho nguyên liệu thô"
        └────────┬─────────┘
                 │
                 ▼ (2. Rửa sạch, gọt giũa, đổi đơn vị)
        ┌──────────────────┐
        │ Schema: STAGING  │  <-- Tầng "Sơ chế & Chuẩn bị"
        └────────┬─────────┘
                 │
                 ▼ (3. Đóng gói thành mô hình phân tích)
        ┌──────────────────┐
        │    Schema: DW    │  <-- Tầng "Bàn tiệc / Báo cáo Power BI"
        └──────────────────┘
```

### 1️⃣ Tầng `RAW` (Dữ liệu thô)
* **Ý nghĩa:** Chứa dữ liệu gốc 100% như lúc tải về từ nguồn (Kaggle CSV, World Bank API).
* **Tại sao phải có?** Để làm "bằng chứng gốc". Nếu sau này code biến đổi bị lỗi, ta luôn có bản gốc để đối chiếu lại mà không sợ mất mát. Tầng này **tuyệt đối không chỉnh sửa thủ công**.

### 2️⃣ Tầng `STAGING` (Khu vực chế biến & làm sạch)
* **Ý nghĩa:** Là nơi sửa chữa các lỗi phi lý của dữ liệu thô:
  * Đổi số ngày âm thành số năm dương (`DAYS_BIRTH = -14600` $\rightarrow$ `40 tuổi`).
  * Xử lý mã lỗi bí mật của hệ thống (`DAYS_EMPLOYED = 365243` $\rightarrow$ Đổi thành `Không có việc làm`).
  * Gom 27 triệu dòng lịch sử quẹt thẻ/trả góp thành 1 dòng tóm tắt duy nhất cho mỗi khách hàng.
* **Tại sao phải có?** Dữ liệu thô quá cồng kềnh và nhiều "rác". Cần một bước đệm để làm sạch trước khi đưa vào bảng báo cáo.

### 3️⃣ Tầng `DW` (Data Warehouse - Kho dữ liệu chuẩn)
* **Ý nghĩa:** Dữ liệu sau khi sạch sẽ được sắp xếp theo cấu trúc **Star Schema (Hình ngôi sao)**.
* **Tại sao phải có?** Giúp phần mềm báo cáo như **Power BI** hoặc các câu lệnh SQL chạy siêu nhanh, kéo-thả báo cáo dễ dàng mà không bị đơ máy.

---

<a name="4-mô-hình-fact--dimension"></a>
## 4. MÔ HÌNH FACT & DIMENSION (STAR SCHEMA) LÀ GÌ?

Mô hình dữ liệu chuẩn của kho dữ liệu (Data Warehouse) được ví như việc trả lời câu hỏi:
> **"Sự việc gì đã xảy ra (FACT), bởi AI, ở ĐÂU và vào THỜI GIAN NÀO (DIMENSIONS)?"**

```
                     ┌───────────────────────────┐
                     │       dw.dim_time         │
                     │ (Thời gian: Năm, Quý,...) │
                     └───────┬───────────┬───────┘
                             │           │
                             ▼           ▼
┌──────────────────┐  ┌───────────┐  ┌──────────────┐  ┌──────────────────┐
│  dw.dim_region   │  │ fact_loan │  │ fact_economy │  │ dw.dim_customer  │
│ (Địa lý: Vùng...)├──┤ (Khoản vay│  │(Chỉ số vĩ mô:│──┤(Tuổi, Thu nhập,  │
└──────────────────┘  │ cá nhân)  │  │ GDP, Lạm phát│  │ Lịch sử nợ...)   │
                      └───────────┘  └──────────────┘  └──────────────────┘
```

### 🌟 1. Các Bảng FACT (Bảng Sự Kiện / Đo Lường Số Liệu)
- **Fact là gì?** Là bảng ghi lại **hành động hoặc số liệu đo lường theo thời gian**.
- **Trong hệ thống CCIP có 2 bảng Fact:**
  1. `dw.fact_loan` (307,511 dòng): Đo lường **từng khoản vay cụ thể của từng khách hàng** (số tiền vay, tiền trả góp hàng tháng, trạng thái vỡ nợ 0 hay 1).
  2. `dw.fact_economy` (171 dòng): Đo lường **bối cảnh kinh tế vĩ mô** theo từng quốc gia và thời gian (Tỷ lệ tăng trưởng GDP, lạm phát, thất nghiệp, lãi suất FED). *Tại sao lại có?* Vì khi kinh tế suy thoái hoặc lạm phát cao, người dân dễ mất việc và tỷ lệ bùng nợ tăng cao trên toàn hệ thống.

### 🏷️ 2. Các Bảng DIMENSION (`dw.dim_*`) — Bảng Chi Tiết / Chiều Phân Tích
- **Dimension là gì?** Là bảng chứa các **thông tin mô tả bối cảnh** xung quanh sự kiện. Dùng để cắt lát, lọc dữ liệu (Filter / Group by).
- **Gồm những bảng nào?**
  1. `dw.dim_customer` (Chiều Con Người): Trả lời câu hỏi **Ai vay?** $\rightarrow$ Tuổi tác, giới tính, nghề nghiệp, trình độ học vấn, lịch sử nợ nần ngoài CIC.
  2. `dw.dim_region` (Chiều Không Gian): Trả lời câu hỏi **Vay ở đâu?** $\rightarrow$ Vùng sinh sống được đánh giá mức độ rủi ro Loại 1, Loại 2 hay Loại 3.
  3. `dw.dim_time` (Chiều Thời Gian): Trả lời câu hỏi **Xảy ra khi nào?** $\rightarrow$ Dùng chung để nối cả `fact_loan` lẫn `fact_economy` theo Năm, Quý, Tháng.

---

<a name="5-chi-tiết-từng-biến-số"></a>
## 5. CHI TIẾT TỪNG BẢNG & Ý NGHĨA TỪNG BIẾN SỐ

### A. Bảng Sự Kiện: `dw.fact_loan` (307,511 dòng = 307,511 khoản vay)

| Tên Cột | Ý nghĩa thực tế | Tại sao lại có cột này? |
| :--- | :--- | :--- |
| `loan_sk` | Mã định danh duy nhất của khoản vay (Khóa chính - PK) | Để phân biệt khoản vay này với khoản vay khác. |
| `customer_sk` | Mã nối sang bảng khách hàng `dim_customer` | Để biết khoản vay này là của ai. |
| `region_sk` | Mã nối sang bảng vùng địa lý `dim_region` | Để biết khoản vay này thuộc khu vực nào. |
| `date_id` | Mã nối sang bảng thời gian `dim_time` | Để biết khoản vay phát sinh vào tháng/năm nào. |
| `is_default` | **0 = Trả nợ tốt, 1 = Bị vỡ nợ (Bùng nợ)** | **Đây là biến quan trọng nhất** toàn dự án. Mọi phân tích đều nhằm giải thích tại sao biến này = 1. |
| `loan_amount` | Số tiền khách hàng đã vay (USD) | Để tính tổng dư nợ cho vay và số tiền tổn thất nếu vỡ nợ. |
| `annuity_amount` | Số tiền khách hàng phải trả góp mỗi tháng | Để kiểm tra xem số tiền trả hàng tháng có quá sức với người vay không. |
| `goods_price` | Giá trị món hàng khách mua (nếu là vay mua hàng) | Để so sánh số tiền vay với giá trị món hàng thật. |
| `loan_to_value_ratio` | Tỷ lệ `loan_amount / goods_price` (LTV) | Người vay 100% giá trị hàng thường dễ bỏ nợ hơn người đã bỏ tiền túi ra trả trước 30%. |
| `income_to_annuity_ratio`| Tỷ lệ `Thu nhập năm / Tiền trả góp năm` | Đo lường mức độ dư dả tài chính của người vay. |
| `contract_type` | Loại hình vay: `Cash loans` (tiền mặt) hay `Revolving loans` (thẻ tín dụng) | Hai sản phẩm tài chính này có đặc thù rủi ro rất khác nhau. |

---

### B. Bảng Chiều Khách Hàng: `dw.dim_customer` (307,511 khách hàng)

Bảng này tổng hợp toàn bộ chân dung của một người đi vay từ 4 góc nhìn:

#### 1. Nhóm Nhân khẩu học & Cá nhân (Ai là người vay?)
- `age_years`: Tuổi thực của khách hàng (VD: 25.5 tuổi).
- `age_group`: Nhóm tuổi (`< 25`, `25–34`, `35–44`, `45–54`, `55+`). *Tại sao có?* Vì người trẻ thường bốc đồng, tỷ lệ đổi việc cao $\rightarrow$ rủi ro nợ xấu cao hơn người lớn tuổi có gia đình ổn định.
- `gender`: Giới tính (`M` - Nam, `F` - Nữ). *Tại sao có?* Thống kê cho thấy Nam giới có tỷ lệ nợ xấu cao hơn Nữ giới (10.14% vs 7.00%).
- `education_level`: Học vấn (Cấp 2, Cấp 3, Đại học, Sau đại học). Người có học vấn cao thường có thu nhập ổn định và ý thức tài chính tốt hơn.
- `occupation`: Nghề nghiệp (Lái xe, Lao động phổ thông, Kế toán, Quản lý...).

#### 2. Nhóm Tài sản & Việc làm (Họ có tiền và tài sản không?)
- `annual_income`: Tổng thu nhập 1 năm của khách hàng.
- `years_employed`: Số năm đã làm việc tại công ty hiện tại. Làm việc càng lâu năm ở một chỗ chứng minh công việc càng vững chắc.
- `has_employment`: `1 = Đang có việc làm`, `0 = Đang thất nghiệp hoặc nghỉ hưu`.
- `owns_car` / `owns_realty`: Khách hàng có xe ô tô / nhà đất riêng không? (Có tài sản là một điểm cộng lớn khi xét duyệt vay).

#### 3. Nhóm Điểm tín dụng độc lập (Thế giới bên ngoài đánh giá họ thế nào?)
- `ext_score_1`, `ext_score_2`, `ext_score_3`: Điểm tín dụng từ 3 nguồn độc lập khác nhau.
- `ext_score_avg`: Điểm trung bình của 3 nguồn trên. **Đây là biến có khả năng dự đoán nợ xấu mạnh nhất toàn bộ hệ thống**. Điểm càng thấp $\rightarrow$ Tỷ lệ vỡ nợ càng tăng vọt.

#### 4. Nhóm Lịch sử vay nợ quá khứ tại các tổ chức khác (Họ có thói quen trả nợ tốt không?)
- `num_external_credits`: Tổng số hợp đồng vay từng mở ở các ngân hàng khác.
- `max_overdue_days`: Số ngày quá hạn trễ nhất mà người này từng ghi nhận trong quá khứ.
- `pct_late_months`: Tỷ lệ phần trăm số tháng từng trả trễ tiền trong lịch sử. (VD: 0.62 nghĩa là 10 tháng đi vay thì có 6 tháng đóng trễ tiền).

---

### C. Bảng Chiều Khu Vực & Thời Gian: `dw.dim_region` & `dw.dim_time`

- **`dw.dim_region`**:
  - `region_rating`: Điểm đánh giá mức độ rủi ro khu vực (1, 2, 3).
  - `risk_level`: Mức độ rủi ro tương ứng (`Thấp`, `Trung bình`, `Cao`).
  - *Tại sao có?* Một số khu vực có điều kiện kinh tế khó khăn hoặc tình trạng lừa đảo tín dụng phức tạp hơn các khu vực khác.
- **`dw.dim_time`**:
  - `date_id`, `year`, `quarter`, `month`, `year_month`.
  - *Tại sao có?* Để phân tích xu hướng theo thời gian (VD: Tháng giáp Tết người dân có xu hướng vay nhiều hơn hay không?).

---

### D. Bảng Sự Kiện Kinh Tế Vĩ Mô: `dw.fact_economy` (171 dòng)

Bảng này chứa các chỉ số kinh tế toàn cầu & quốc gia được thu thập từ World Bank và Cục Dự trữ Liên bang Mỹ (FRED):
- `gdp_growth_pct`: Tốc độ tăng trưởng kinh tế (% GDP).
- `inflation_cpi_pct`: Tỷ lệ lạm phát (giá cả hàng hóa leo thang).
- `unemployment_rate_pct`: Tỷ lệ thất nghiệp của người dân.
- `fed_funds_rate`: Lãi suất điều hành của FED (Mỹ) — ảnh hưởng đến chi phí vốn và lãi suất cho vay toàn cầu.
- `m2_money_supply_bn`: Cung tiền M2 của Mỹ.

👉 *Tại sao cần bảng này?* Giúp phân tích xem **trong những giai đoạn kinh tế suy thoái hoặc lạm phát cao**, tỷ lệ vỡ nợ của khách hàng có tăng đột biến hay không.

---

<a name="6-tóm-tắt-luồng-dữ-liệu"></a>
## 6. TÓM TẮT LUỒNG ĐI CỦA DỮ LIỆU TỪ A $\rightarrow$ Z

Để dễ hình dung toàn bộ dự án đang làm gì, hãy xem sơ đồ tóm tắt sau:

```
[ DỮ LIỆU GỐC (58.5 Triệu dòng) ]
  ├── 307K đơn xin vay
  ├── 1.7M lịch sử tín dụng ngoài
  └── 27M tháng trả nợ thẻ/góp
              │
              ▼ (load_raw_fast.py: nạp siêu tốc bằng PostgreSQL COPY trong ~9 phút)
      [ SCHEMA RAW ]
              │
              ▼ (transform/staging/*.sql: Rửa dữ liệu, tính tuổi, xử lý lỗi 365243)
    [ SCHEMA STAGING ]
              │
              ▼ (transform/dw/*.sql: Gom thành 1 Fact + 3 Dimensions)
      [ SCHEMA DW ]
              │
      ┌───────┴────────────────────────┐
      ▼                                ▼
[ Phân tích SQL (CH1-CH5) ]    [ Kết nối Power BI Dashboard ]
- Nhóm tuổi nào dễ vỡ nợ?       - Báo cáo trực quan kéo thả
- Điểm tín dụng nào cảnh báo?   - Bộ lọc theo Vùng / Nghề nghiệp
```

---
*Tài liệu được biên soạn nhằm phục vụ học tập và trình bày đồ án phân tích dữ liệu tín dụng CCIP.*
