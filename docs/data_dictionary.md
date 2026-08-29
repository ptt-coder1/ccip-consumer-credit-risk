# Data Dictionary — CCIP

Giải thích các cột quan trọng trong từng tầng dữ liệu.

---

## Schema `raw` — Dữ liệu gốc

### `raw.hc_application_train` (307,511 dòng)
Bảng chính — mỗi dòng = 1 đơn vay.

| Cột gốc | Kiểu | Mô tả |
|---------|------|-------|
| `SK_ID_CURR` | INT | Khóa chính — ID khách hàng |
| `TARGET` | INT | **Nhãn**: 1=vỡ nợ, 0=không vỡ nợ |
| `AMT_CREDIT` | FLOAT | Số tiền vay |
| `AMT_ANNUITY` | FLOAT | Số tiền trả góp hàng tháng |
| `AMT_INCOME_TOTAL` | FLOAT | Thu nhập hàng năm |
| `DAYS_BIRTH` | INT | Số ngày âm tính từ ngày nộp đơn đến ngày sinh (ví dụ -14000 = khoảng 38 tuổi) |
| `DAYS_EMPLOYED` | INT | Số ngày âm tính từ ngày nộp đơn đến ngày bắt đầu làm việc. **Giá trị 365243 = không có việc làm (mã đặc biệt — không phải 1000 năm làm việc)** |
| `EXT_SOURCE_1/2/3` | FLOAT | Điểm tín dụng từ 3 nguồn bên ngoài (0–1, cao = ít rủi ro) |
| `FLAG_DOCUMENT_*` | INT | 1 nếu khách hàng cung cấp loại tài liệu đó, 0 nếu không |

---

## Schema `staging` — Dữ liệu đã làm sạch

### `staging.stg_application`
| Cột | Kiểu | Mô tả / Công thức |
|-----|------|-------------------|
| `customer_id` | INT | = SK_ID_CURR |
| `is_default` | INT | = TARGET |
| `age_years` | INT | = ABS(DAYS_BIRTH) / 365 |
| `age_group` | VARCHAR | Nhóm tuổi: '< 25', '25–34', '35–44', '45–54', '55+' |
| `years_employed` | NUMERIC | = ABS(DAYS_EMPLOYED) / 365, NULL nếu DAYS_EMPLOYED = 365243 |
| `loan_to_value_ratio` | NUMERIC | = AMT_CREDIT / AMT_GOODS_PRICE |
| `income_to_annuity_ratio` | NUMERIC | = AMT_INCOME_TOTAL / AMT_ANNUITY — cao = dễ trả nợ hơn |
| `ext_score_avg` | NUMERIC | Trung bình EXT_SOURCE_1/2/3 (bỏ qua NULL) |
| `num_documents_provided` | INT | Tổng số FLAG_DOCUMENT_* = 1 |

### `staging.stg_bureau_summary`
| Cột | Mô tả |
|-----|-------|
| `num_external_credits` | Tổng số khoản vay tại tổ chức tín dụng bên ngoài |
| `pct_credits_overdue` | % số khoản từng quá hạn |
| `pct_late_months` | % số tháng trả trễ (từ bureau_balance) |
| `max_overdue_days` | Số ngày quá hạn lớn nhất từng ghi nhận |

---

## Schema `dw` — Star Schema

### Sơ đồ quan hệ (Star Schema)

```
                    ┌──────────────┐
                    │  dim_time    │
                    │  date_id PK  │
                    └──────┬───────┘
                           │ FK
┌──────────────┐    ┌──────▼───────┐    ┌──────────────┐
│  dim_region  │    │  fact_loan   │    │ dim_customer  │
│  region_sk PK├────┤  loan_sk PK  ├────┤ customer_sk PK│
└──────────────┘ FK │  is_default  │ FK └──────────────┘
                    │  loan_amount │
                    │  ...         │
                    └──────────────┘

                    ┌──────────────┐
                    │ fact_economy │
                    │  date_id FK  │→ dim_time
                    └──────────────┘
```

### `dw.fact_loan` — Bảng sự kiện khoản vay
| Cột | Vai trò | Mô tả |
|-----|---------|-------|
| `loan_sk` | PK | Surrogate key |
| `customer_sk` | FK → dim_customer | |
| `date_id` | FK → dim_time | |
| `region_sk` | FK → dim_region | |
| `is_default` | **Measure** | 1=vỡ nợ, 0=không |
| `loan_amount` | **Measure** | Số tiền vay |
| `loan_to_value_ratio` | **Measure** | LTV ratio |

### `dw.dim_customer` — Thông tin khách hàng
| Nhóm | Các cột |
|------|---------|
| Nhân khẩu học | age_years, age_group, gender, family_status |
| Tài chính | annual_income, income_type, years_employed |
| Tài sản | owns_car, owns_realty, housing_type |
| Tín dụng bên ngoài | ext_score_avg, pct_late_months, max_overdue_days |
| Lịch sử vay HC | num_prev_applications, approval_rate_pct |

### `dw.fact_economy` — Bảng sự kiện chỉ số kinh tế vĩ mô (171 dòng)
Bảng Fact đo lường bối cảnh kinh tế theo thời gian và quốc gia (World Bank & FRED API).
| Cột | Vai trò | Mô tả / Ý nghĩa |
|-----|---------|-----------------|
| `economy_sk` | PK | Surrogate key |
| `date_id` | FK → dim_time | Khóa nối sang bảng thời gian (tháng/năm) |
| `country_code` / `country_name` | Thuộc tính | Mã (VN, US, RU, PL, UA, CZ, SK) và tên quốc gia |
| `source` | Thuộc tính | Nguồn dữ liệu (`worldbank` hoặc `fred`) |
| `gdp_growth_pct` | **Measure** | Tăng trưởng GDP hàng năm (%) |
| `inflation_cpi_pct` | **Measure** | Tỷ lệ lạm phát theo chỉ số CPI (%) |
| `unemployment_rate_pct` | **Measure** | Tỷ lệ thất nghiệp quốc gia (%) |
| `domestic_credit_gdp_pct` | **Measure** | Tín dụng nội địa cung cấp cho khu vực tư nhân (% GDP) |
| `fed_funds_rate` | **Measure** | Lãi suất điều hành của Cục Dự trữ Liên bang Mỹ (FED Funds Rate %) |
| `m2_money_supply_bn` | **Measure** | Cung tiền M2 của Mỹ (tỷ USD) |
| `cpi_us` / `unemployment_us_pct` | **Measure** | Chỉ số giá tiêu dùng CPI & tỷ lệ thất nghiệp của Mỹ |

---

## Giả định quan trọng (cần ghi vào báo cáo)

| # | Giả định | Lý do |
|---|----------|-------|
| 1 | `DAYS_EMPLOYED = 365243` được xử lý thành NULL | Đây là mã lỗi đặc biệt trong bộ dữ liệu gốc, không phải giá trị thật |
| 2 | Ngày vay được ước tính từ mốc 2017-09-01 | Bộ dữ liệu không có ngày vay tuyệt đối — đây là giả định rõ ràng |
| 3 | `raw` schema trong PostgreSQL ≠ Data Lake thật | raw chỉ là "vùng lưu thô nội bộ", không phải object storage |
| 4 | Dữ liệu World Bank cho tháng = dùng tháng 1 | World Bank chỉ có độ chi tiết theo năm |
