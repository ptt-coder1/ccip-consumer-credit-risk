# BÁO CÁO HỌC THUẬT NGHIÊN CỨU & ỨNG DỤNG HỆ THỐNG
# CONSUMER CREDIT INTELLIGENCE PLATFORM (CCIP)
## Nền tảng Phân tích Rủi ro Tín dụng Tiêu dùng Đa chiều: Từ Kiến trúc Dữ liệu, Trực quan hóa Điều hành đến Xếp hạng Rủi ro Máy học & Ma trận Khuyến nghị Quản trị

---

> **Tên đề tài:** Xây dựng Nền tảng Phân tích Rủi ro Tín dụng Tiêu dùng (Consumer Credit Intelligence Platform - CCIP)  
> **Lĩnh vực:** Hệ thống Thông tin Quản lý (MIS) / Khoa học Dữ liệu & Phân tích Kinh doanh (Data Analytics & BI)  
> **Quy mô danh mục chuẩn hóa (SSOT Data Grain):** 307,511 hồ sơ vay (`dw.fact_loan` + `dw.dim_customer` + `dw.dim_region`)  
> **Các chỉ số khóa (Frozen SSOT Baseline):**
> - **Tổng số hồ sơ vay (Loan Applications):** `307,511` hồ sơ
> - **Tổng giá trị phơi nhiễm (Total Loan Exposure):** `184.2 tỷ CU` (Currency Units)
> - **Tỷ lệ vỡ nợ danh mục (Portfolio Default Rate):** `8.07%` (`24,825` khoản vỡ nợ / `282,686` khoản trả đúng hạn)
> - **Tổng dư nợ chịu rủi ro (Amount at Risk):** `~13.8 tỷ CU`
> - **Phân khúc điểm nóng (Hotspot Q4 × T1):** Tỷ lệ vỡ nợ `19.90%` (Quy mô: `16,158` hồ sơ | Phơi nhiễm rủi ro: `2.10 tỷ CU`)

---

## 📑 MỤC LỤC TỔNG THỂ

1. **[Chương 1: Tổng quan Đề tài, Mục tiêu & Câu hỏi Nghiên cứu](#chương-1-tổng-quan-đề-tài-mục-tiêu--câu-hỏi-nghiên-cứu)**
   - 1.1. Bối cảnh Nghiên cứu & Thực tiễn Ngành Tín dụng Tiêu dùng
   - 1.2. Phát biểu Vấn đề (Problem Statement)
   - 1.3. Mục tiêu Đề tài (Project Objectives)
   - 1.4. Hệ thống Câu hỏi Nghiên cứu (Research Questions RQ1 → RQ6)
   - 1.5. Phạm vi & Giới hạn Nghiên cứu (Scope & Boundaries)
2. **[Chương 2: Kiến trúc Nền tảng Dữ liệu & Quy trình ETL/DWH](#chương-2-kiến-trúc-nền-tảng-dữ-liệu--quy-trình-etldwh)**
   - 2.1. Kiến trúc Hệ thống Tổng thể (End-to-End Pipeline)
   - 2.2. Thiết kế Mô hình Dữ liệu Star Schema (Data Warehouse Layer)
   - 2.3. Hợp đồng Hạt nhân Dữ liệu & Tính Toàn vẹn (Data Grain Contract & SSOT)
   - 2.4. Xử lý Chất lượng Dữ liệu & Kỹ thuật Tính toán Thuộc tính (Data Quality & Feature Engineering)
3. **[Chương 3: Phân tích Thống kê Mô tả & Khám phá Rủi ro](#chương-3-phân-tích-thống-kê-mô-tả--khám-phá-rủi-ro)**
   - 3.1. Phân tầng Rủi ro Đơn biến theo Điểm tín dụng (Monotonic Risk Gradient Q1 → Q4)
   - 3.2. Phân tích Rủi ro Đa chiều & Vùng Điểm nóng (Hotspot Q4 × T1)
   - 3.3. Đặc trưng Nhân khẩu học: Độ tuổi, Thu nhập và Nghề nghiệp
   - 3.4. Bối cảnh Kinh tế Vĩ mô Tham chiếu (Macroeconomic Reference Context)
4. **[Chương 4: Kiến trúc Dashboard Điều hành & Trực quan hóa Thông tin](#chương-4-kiến-trúc-dashboard-điều-hành--trực-quan-hóa-thông-tin)**
   - 4.1. Triết lý Thiết kế & Storyboard 4 Trang (Executive Storyboard)
   - 4.2. Chi tiết Cấu trúc Từng Trang Báo cáo (P1 → P4)
   - 4.3. Thiết kế Hệ thống Đo lường Tập trung (Centralized DAX Architecture)
   - 4.4. Đánh giá Trải nghiệm Người dùng Điều hành (Executive UX Validation)
5. **[Chương 5: Phân tích Dự đoán & Khả năng Giải thích Mô hình Máy học](#chương-5-phân-tích-dự-đoán--khả-năng-giải-thích-mô-hình-máy-học)**
   - 5.1. Thiết kế Thực nghiệm & Cơ chế Chia Dữ liệu Không Rò rỉ (60/20/20 Stratified Split)
   - 5.2. Mô hình Hồi quy Logistic Chuẩn mực (Logistic Regression Baseline)
   - 5.3. Mô hình Cây Quyết định Nâng cao (LightGBM Main Model)
   - 5.4. Đánh giá Hiệu năng Phân biệt trên Tập Kiểm thử Độc lập (Test Set Holdout)
   - 5.5. Phân tích Đánh đổi Ngưỡng Vận hành trên Tập Kiểm định (Validation Threshold Trade-off)
   - 5.6. Ước lượng Mức độ Đóng góp Thuộc tính bằng SHAP (Global Explainability Estimation)
   - 5.7. Kiểm định Đối chiếu Tính Nhất quán (SQL DWH vs ML Consistency Analysis)
6. **[Chương 6: Ma trận Phát hiện & Khuyến nghị Kinh doanh](#chương-6-ma-trận-phát-hiện--khuyến-nghị-kinh-doanh)**
   - 6.1. Khung Cấu trúc Phân cấp Quyết định 3 Tầng (Decision Framework)
   - 6.2. Ma trận 5 Phát hiện Trọng yếu & Khuyến nghị Hành động (INS-001 → INS-005)
   - 6.3. Bảng Phân công Trách nhiệm & Thực thi (Action Plan & Owner Assignment)
7. **[Chương 7: Giới hạn Đề tài & Hướng Phát triển Mở rộng](#chương-7-giới-hạn-đề-tài--hướng-phát-triển-mở-rộng)**
   - 7.1. Giới hạn Dữ liệu Cắt ngang & Kiểm định Thời gian (Temporal & Point-in-Time Limitations)
   - 7.2. Giới hạn Mô hình & Vấn đề Hiệu chỉnh Xác suất (Probability Calibration & Scoring Limits)
   - 7.3. Lộ trình Nâng cấp Hệ thống Quản trị Rủi ro Sản xuất (Future Roadmap)

---

# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI, MỤC TIÊU & CÂU HỎI NGHIÊN CỨU

### 1.1. Bối cảnh Nghiên cứu & Thực tiễn Ngành Tín dụng Tiêu dùng
Trong kỷ nguyên số hóa tài chính, tín dụng tiêu dùng không thế chấp (Unsecured Consumer Lending) đã trở thành một động lực tăng trưởng kinh tế quan trọng. Tuy nhiên, phân khúc này mang bản chất rủi ro bất đối xứng thông tin cao, thiếu tài sản bảo đảm và danh mục hồ sơ quy mô lớn nhưng phân tán. Các tổ chức tín dụng phải đối mặt với bài toán kép: vừa phải tối ưu hóa quy trình phê duyệt tự động (Straight-Through Processing) để mở rộng thị phần, vừa phải kiểm soát chặt chẽ tỷ lệ nợ xấu (Non-Performing Loans - NPL) nhằm bảo toàn vốn.

### 1.2. Phát biểu Vấn đề (Problem Statement)
Thực tiễn quản trị rủi ro tại nhiều tổ chức tài chính thường gặp các hạn chế cốt lõi:
1. **Dữ liệu phân mảnh và thiếu Nhất quán (Data Silos):** Dữ liệu đơn vay, lịch sử tín dụng ngoài (Credit Bureau) và lịch sử giao dịch nội bộ lưu trữ rời rạc, dẫn đến sai lệch định nghĩa và thiếu một Nguồn Sự thật Duy nhất (Single Source of Truth - SSOT).
2. **Khoảng cách giữa Báo cáo Mô tả và Dự đoán:** Báo cáo BI truyền thống thường dừng lại ở mức mô tả tĩnh (Descriptive), không chỉ ra được các điểm nóng rủi ro phi tuyến tính đa chiều và thiếu sự đối soát kiểm chứng với các thuật toán máy học hiện đại.
3. **Thiếu Khung Chuyển đổi từ Insight sang Quyết định:** Các phát hiện phân tích thường không được phân cấp mức độ can thiệp (vận hành vs chính sách) và thiếu phân định trách nhiệm thực thi rõ ràng, làm giảm tính hành động của dữ liệu.

### 1.3. Mục tiêu Đề tài (Project Objectives)
Đề tài hướng tới việc xây dựng **Consumer Credit Intelligence Platform (CCIP)** — một nền tảng phân tích kinh doanh tích hợp toàn diện với các mục tiêu cụ thể:
- **Về Kỹ thuật Dữ liệu (Data Engineering):** Xây dựng kho dữ liệu Star Schema trên PostgreSQL, thiết lập hợp đồng hạt nhân dữ liệu chuẩn mực (307,511 dòng hồ sơ) và tự động hóa trích xuất tập dữ liệu ML-ready định dạng Parquet.
- **Về Trực quan hóa & Phân tích Nghiệp vụ (BI & Business Analytics):** Phát triển Dashboard điều hành 4 trang chuyên nghiệp trên Power BI, cung cấp câu chuyện trực quan từ tổng quan danh mục, phân tầng rủi ro, đào sâu điểm nóng đến hồ sơ khách hàng.
- **Về Khoa học Dữ liệu & Máy học (Predictive Analytics & Explainability):** Triển khai mô hình phân loại LightGBM kết hợp giải thích SHAP để xếp hạng rủi ro và kiểm định tính nhất quán với thống kê DWH trên tập holdout độc lập.
- **Về Ứng dụng Quản trị (Actionable Governance):** Xây dựng Ma trận Khuyến nghị Kinh doanh phân tầng theo 3 cấp độ quyết định gắn liền với Decision Owner theo chuẩn `dashboard-insight-workflow`.

### 1.4. Hệ thống Câu hỏi Nghiên cứu (Research Questions)
Hệ thống 6 câu hỏi nghiên cứu (RQ) định hướng xuyên suốt mọi khâu phân tích:
* **RQ1 (Phân khúc Nhân khẩu học & Nghề nghiệp):** Các đặc điểm nhân khẩu học (tuổi tác, giới tính, học vấn) và loại hình thu nhập có mối quan hệ như thế nào với khả năng vỡ nợ; nhóm đối tượng nào mang rủi ro tập trung cao nhất? *(Evidence: Association)*
* **RQ2 (Lịch sử Tín dụng & Điểm số Ngoài):** Lịch sử tín dụng quá khứ và điểm đánh giá bên ngoài (`ext_score_avg`) có giá trị dự báo mạnh đến mức nào đối với rủi ro vỡ nợ? *(Evidence: Predictive Association)*
* **RQ3 (Địa lý & Khu vực):** Khu vực địa lý và xếp hạng kinh tế vùng (`region_rating`) phản ánh sự khác biệt về quy mô khoản vay và rủi ro tín dụng ra sao? *(Evidence: Adjusted Association)*
* **RQ4 (Phân tầng Rủi ro Đơn biến):** Làm thế nào để phân nhóm danh mục khách hàng thành các tầng rủi ro tương đối (Quartiles Q1 → Q4) có tính đơn điệu chặt chẽ? *(Evidence: Model Proxy / Ranking)*
* **RQ5 (Vùng Điểm nóng & Khả năng Chi trả):** Khi kết hợp đa chiều giữa điểm tín dụng và gánh nặng trả góp (`income_to_annuity`), vùng điểm nóng rủi ro (Hotspot) nào xuất hiện và quy mô phơi nhiễm tài chính là bao nhiêu? *(Evidence: Decision Threshold / Multivariate Stress)*
* **RQ6 (Bối cảnh Vĩ mô & Đóng góp Dự đoán Máy học):** Mô hình học máy phi tuyến tính có cải thiện năng lực phân định rủi ro so với hồi quy tuyến tính chuẩn mực không, và các nhân tố nào đóng góp lớn nhất vào dự đoán theo SHAP? *(Evidence: Predictive & Explainability Evidence)*

### 1.5. Phạm vi & Giới hạn Nghiên cứu (Scope & Boundaries)
- **Tập dữ liệu nền tảng:** Bộ dữ liệu tín dụng tiêu dùng Home Credit Default Risk (307,511 hồ sơ đơn vay tại thời điểm nộp đơn).
- **Phạm vi Phương pháp luận:** Dự án tập trung vào phân tích kinh doanh (Business Intelligence), phân tầng rủi ro và xếp hạng rủi ro (Risk Ranking). Dự án **không** nhằm mục đích xây dựng bảng điểm PD Scorecard tuân thủ tiêu chuẩn vốn Basel II/III hay hệ thống phê duyệt tự động thay thế con người.

---

# CHƯƠNG 2: KIẾN TRÚC NỀN TẢNG DỮ LIỆU & QUY TRÌNH ETL/DWH

### 2.1. Kiến trúc Hệ thống Tổng thể (End-to-End Pipeline)
Kiến trúc CCIP được tổ chức thành 4 tầng phân tách mạch lạc, đảm bảo tính mô-đun hóa và khả năng tái lập (Reproducibility):

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           RAW DATA LAYER                                │
│        application_train (307k) │ bureau │ previous_application         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Python ETL / Staging Load
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          STAGING SCHEMA                                 │
│  stg_application (Data Cleaning) │ stg_bureau_summary │ stg_prev_summary│
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ SQL Star Schema Transformation
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               DATA WAREHOUSE LAYER (PostgreSQL - SSOT)                  │
│       dw.dim_customer (307,511) ◄─── dw.fact_loan (307,511)             │
│       dw.dim_region   (3)       ◄─── dw.dim_time  (144)                 │
└───────────────────┬─────────────────────────────────┬───────────────────┘
                    │                                 │ Python Parquet Export
                    │ Direct SQL / Semantic Model     │ (18.65 MB)
                    ▼                                 ▼
┌──────────────────────────────────────┐ ┌────────────────────────────────┐
│      DESCRIPTIVE BI LAYER            │ │    PREDICTIVE ML LAYER         │
│     Power BI Desktop Report          │ │ Google Colab / LightGBM + SHAP │
│ (P1 Overview → P4 Profile)           │ │ (60/20/20 Holdout Evaluation)  │
└───────────────────┬──────────────────┘ └────────────────┬───────────────┘
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│          GOVERNANCE: FINDINGS & RECOMMENDATIONS MATRIX                  │
│  5 Core Insights ──► 3 Decision Levels ──► Action Plan with Owners     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Thiết kế Mô hình Dữ liệu Star Schema (Data Warehouse Layer)
Data Warehouse được chuẩn hóa theo mô hình Star Schema trên cơ sở dữ liệu PostgreSQL (`ccip_dw`) tuân thủ các nguyên lý mô hình hóa chiều dữ liệu chuẩn mực (Kimball & Ross, 2013):
- **Bảng Fact chính (`dw.fact_loan`):** Lưu trữ 307,511 bản ghi khoản vay. Khóa ngoại liên kết tới các Dimension: `customer_sk`, `region_sk`, `date_id`. Chứa các độ đo định lượng: `loan_amount`, `annuity_amount`, `goods_price`, `loan_to_value_ratio`, `income_to_annuity_ratio`, `is_default`, `ext_score_avg`.
- **Bảng Chiều khách hàng (`dw.dim_customer`):** Trong phạm vi dataset nghiên cứu, mỗi hồ sơ phân tích tương ứng với một application và một customer identifier duy nhất; do đó `dw.dim_customer` được materialize ở grain phân tích tương ứng với **307,511 hồ sơ**. Bảng hợp nhất toàn diện các thông tin nhân khẩu học, thu nhập, học vấn, điểm tín dụng bên ngoài và các chỉ số tổng hợp tiền nộp đơn từ Bureau (`num_active_credits`, `total_overdue_amt`, `pct_late_months`) và Previous Applications (`approval_rate_pct`, `avg_prev_credit_amt`).
- **Bảng Chiều khu vực (`dw.dim_region`):** 3 phân cấp xếp hạng rủi ro địa phương (Loại 1 - Thấp, Loại 2 - Trung bình, Loại 3 - Cao).
- **Bảng Chiều thời gian (`dw.dim_time`):** Hỗ trợ chuẩn hóa trục thời gian phân tích kinh tế vĩ mô.

### 2.3. Hợp đồng Hạt nhân Dữ liệu & Tính Toàn vẹn (Data Grain Contract & SSOT)
- **Quy tắc Hạt nhân (Grain Rule):** Bắt buộc duy trì nghiêm ngặt **1 dòng = 1 hồ sơ nộp đơn vay = 1 khách hàng = 1 nhãn mục tiêu (307,511 dòng)**. Mọi phép tổng hợp (Aggregation) từ các bảng lịch sử đa quan hệ (1-to-N như Bureau, Previous Applications) đều được tính toán gom cụm tại tầng Staging trước khi JOIN vào Dimension, triệt tiêu hoàn toàn rủi ro nhân bản dòng (Cartesian Explosion).
- **Khóa Số liệu Nền tảng (Integrity Lock):**
  - Số dòng toàn vẹn: `307,511` dòng (0 bản ghi trùng lặp `customer_id`).
  - Phân bổ nhãn mục tiêu: `282,686` khoản trả đúng hạn (Class 0 - 91.93%) và `24,825` khoản vỡ nợ (Class 1 - 8.07%).
  - Tỷ lệ vỡ nợ chuẩn toàn danh mục: **`8.07%`**.

### 2.4. Xử lý Chất lượng Dữ liệu & Kỹ thuật Tính toán Thuộc tính (Data Quality & Feature Engineering)
1. **Xử lý Mã lỗi Sentinel `DAYS_EMPLOYED = 365243`:**
   - Giá trị `365243` biểu thị mã quy ước cho nhóm người không tham gia thị trường lao động chính thức / hưu trí.
   - Chuyển đổi thành `years_employed = NULL` và tạo cờ nhị phân `has_employment = 0` (ngược lại = 1). Kỹ thuật này giúp giữ nguyên thông tin mà không làm sai lệch phân phối thống kê.
2. **Chuẩn hóa Tỷ lệ Đòn bẩy & Khả năng Chi trả (Affordability Metrics):**
   - Tỷ lệ Vay trên Giá trị Tài sản: $\text{Loan-to-Value (LTV)} = \frac{\text{AMT\_CREDIT}}{\text{AMT\_GOODS\_PRICE}}$.
   - Tỷ lệ Thu nhập trên Trả góp: $\text{Income-to-Annuity} = \frac{\text{AMT\_INCOME\_TOTAL}}{\text{AMT\_ANNUITY}}$ (thể hiện số lần thu nhập hàng năm bao phủ khoản trả góp).
3. **Điểm Tín dụng Ngoài Tổng hợp (`ext_score_avg`):**
   - Trung bình cộng linh hoạt của 3 nguồn điểm ngoại vi `ext_source_1`, `ext_source_2`, `ext_source_3` (loại trừ các giá trị NULL khi tính trung bình).
4. **Xuất bản Dataset ML-Ready (`ccip_ml_dataset.parquet`):**
   - Tệp Parquet dung lượng tối ưu **18.65 MB**, chứa 44 thuộc tính kỹ thuật và nhãn `target`, cho phép nạp trực tiếp vào Google Drive để huấn luyện mô hình trên Colab mà không phụ thuộc vào raw Kaggle CSV hay kết nối mạng cơ sở dữ liệu.

---

# CHƯƠNG 3: PHÂN TÍCH THỐNG KÊ MÔ TẢ & KHÁM PHÁ RỦI RO

### 3.1. Phân tầng Rủi ro Đơn biến theo Điểm tín dụng (Monotonic Risk Gradient Q1 → Q4)
Phân tích phân tầng rủi ro trên điểm tín dụng trung bình ngoài (`ext_score_avg`) chỉ ra **mối quan hệ đơn điệu rõ ràng trong dữ liệu quan sát** với tỷ lệ vỡ nợ:

| Phân khúc Rủi ro | Ngưỡng Điểm Tín dụng | Số lượng Hồ sơ | Tỷ lệ trong Danh mục | Tỷ lệ Vỡ nợ (Default Rate) | Đóng góp vào Tổng Vỡ nợ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Q1 (Lowest Risk)** | $\ge 0.6276$ | 73,352 | 23.9% | **2.69%** | 7.9% |
| **Q2 (Low-Moderate)** | $[0.5144, 0.6276)$ | 88,345 | 28.7% | **4.63%** | 16.5% |
| **Q3 (Moderate-High)** | $[0.3868, 0.5144)$ | 82,994 | 27.0% | **8.55%** | 28.6% |
| **Q4 (Highest Risk)** | $< 0.3868$ | 62,648 | 20.4% | **18.60%** | **46.9%** |

* **Nhận xét chuyên môn:** Tỷ lệ vỡ nợ ở nhóm Q4 (18.60%) cao gấp **2.30 lần** baseline danh mục (`8.07%`) và cao gấp **6.91 lần (xấp xỉ 6.93x)** nhóm Q1 (`2.69%`). Mặc dù chỉ chiếm 20.4% số lượng hồ sơ, **nhóm Q4 đóng góp tới 46.9% tổng số ca vỡ nợ toàn danh mục**. Hệ số tương quan Pearson giữa điểm tín dụng và vỡ nợ đạt $r = -0.2229$ (mối liên kết tuyến tính âm mạnh nhất trong các biến số).
*(Lưu ý về phương pháp luận: Trong giai đoạn SQL EDA ban đầu, hàm `NTILE(4)` phân chia danh mục thành 4 nhóm kích thước bằng nhau ~76.8k hồ sơ với default rate 2.71% $\rightarrow$ 17.28%; khi chuyển sang tầng triển khai nghiệp vụ trên Power BI và ML pipeline, hệ thống chuẩn hóa sang phân tầng quy tắc cố định (Fixed Operational Score Cut-offs) với ngưỡng Q1 $\ge 0.6276$ và Q4 $< 0.3868$, mang lại default rate tương ứng 2.69% $\rightarrow$ 18.60%).*

### 3.2. Phân tích Rủi ro Đa chiều & Vùng Điểm nóng (Hotspot Q4 × T1)
Khi kết hợp chéo giữa Điểm tín dụng và Tỷ lệ Chi trả Thu nhập (`income_to_annuity`), bức tranh rủi ro bộc lộ tính chất tập trung phi tuyến tính:

```
                  MA TRẬN RỦI RO ĐA CHIỀU (DEFAULT RATE %)
┌─────────────────────────┬────────────┬────────────┬────────────┬────────────┐
│ Affordability Tier      │ Q1 (Thấp)  │ Q2 (TB-Thấp│ Q3 (TB-Cao)│ Q4 (Cao)   │
├─────────────────────────┼────────────┼────────────┼────────────┼────────────┤
│ T1 (< 4.5x - Gánh nặng) │   3.07%    │   5.25%    │   9.46%    │  19.90% 🔥 │
│ T2 [4.5x - 6.25x)       │   2.79%    │   4.88%    │   8.96%    │  19.65%    │
│ T3 [6.25x - 9.0x)       │   2.53%    │   4.30%    │   8.34%    │  18.20%    │
│ T4 (≥ 9.0x - Dồi dào)   │   2.23%    │   4.01%    │   7.40%    │  16.59%    │
└─────────────────────────┴────────────┴────────────┴────────────┴────────────┘
```

* **Quy mô Vùng Điểm nóng (Hotspot Q4 × T1):**
  - Tỷ lệ vỡ nợ: **`19.90%`** (3,216 ca vỡ nợ / 16,158 hồ sơ, cao gấp 2.47 lần baseline danh mục).
  - Số lượng hồ sơ: **`16,158`** hồ sơ (chiếm 5.25% danh mục).
  - Dư nợ chịu rủi ro (Amount at Risk): **`2.10 tỷ CU`** (chính xác `2,096,007,278 CU` dư nợ vỡ nợ trên tổng `11.11 tỷ CU` giải ngân phân khúc).
  - **Ý nghĩa:** Đây là phân khúc có rủi ro cộng hưởng nghiêm trọng nhất — nơi khách hàng vừa có uy tín tín dụng kém trong quá khứ, vừa gánh chịu áp lực trả nợ lớn.

### 3.3. Đặc trưng Nhân khẩu học: Độ tuổi, Thu nhập và Nghề nghiệp
- **Phân hóa theo Độ tuổi:**
  - Nhóm trẻ tuổi (**< 25 tuổi**): Tỷ lệ vỡ nợ đạt **`12.31%`** (`1,496 / 12,150` hồ sơ, cao gấp 1.53 lần baseline).
  - Tỷ lệ vỡ nợ giảm đều đặn theo độ tuổi: `25–34 (10.67%)` → `35–44 (8.40%)` → `45–54 (7.06%)` → `55+ (5.21%)`.
- **Phân hóa theo Nghề nghiệp & Học vấn:**
  - Nhóm Học vấn Đại học trở lên (`Higher education`): Tỷ lệ vỡ nợ **`5.36%`** (`4,009 / 74,863` hồ sơ, thấp hơn baseline 2.71 pp).
  - Nhóm Học vấn Phổ thông cơ sở (`Lower secondary`): Tỷ lệ vỡ nợ **`10.93%`** (`417 / 3,816` hồ sơ).
  - Phân hóa theo Loại hình thu nhập: Nhóm Công chức nhà nước (`State servant`): **`5.75%`** (`1,249 / 21,703`); Nhóm Hưu trí (`Pensioner`): **`5.39%`** (`2,982 / 55,362`); Nhóm Lao động tự do/công nhân (`Working`): **`9.59%`** (`15,224 / 158,774`).

### 3.4. Bối cảnh Kinh tế Vĩ mô Tham chiếu (Macroeconomic Reference Context)
Dữ liệu từ `dw.fact_economy` cung cấp bối cảnh kinh tế độc lập giai đoạn 2010–2018:
- Thị trường hoạt động chính ghi nhận giai đoạn phục hồi kinh tế năm 2017 với tăng trưởng GDP đạt `+1.57%` và lạm phát CPI về mức `3.68%` (so với đỉnh điểm lạm phát `15.53%` năm 2015).
- **Lưu ý Phương pháp luận:** Bối cảnh vĩ mô được sử dụng nhằm cung cấp thông tin tham chiếu cho thời điểm quan sát. Do dữ liệu khoản vay hiện chỉ được gắn với một mốc thời gian (snapshot 2017), nghiên cứu chưa đủ cơ sở để định lượng mức độ ảnh hưởng của các biến kinh tế vĩ mô đến xác suất vỡ nợ hoặc loại trừ tác động của các cú sốc kinh tế.

---

# CHƯƠNG 4: KIẾN TRÚC DASHBOARD ĐIỀU HÀNH & TRỰC QUAN HÓA THÔNG TIN

### 4.1. Triết lý Thiết kế & Storyboard 4 Trang (Executive Storyboard)
Dashboard CCIP trên Power BI được thiết kế bám sát các nguyên lý thiết kế bảng điều khiển thông tin điều hành (Few, 2006) — ưu tiên tối đa tính rõ ràng, loại bỏ phiền nhiễu thị giác (data-to-ink ratio) và tối ưu hóa khả năng quét nhanh thông tin hỗ trợ ra quyết định:
- **Cấu trúc luồng thông tin (Storyboard):** Đi từ bức tranh vĩ mô danh mục (P1) → Phân tầng rủi ro đơn biến (P2) → Đào sâu điểm nóng tập trung đa chiều (P3) → Chi tiết hồ sơ nhân khẩu học người vay (P4).
- **Bảng màu trực quan (Color Semantics):** Sử dụng bảng màu chuyên nghiệp tuân thủ chuẩn tương phản WCAG: Xanh Navy `#1E3A8A` cho baseline và thành phần an toàn; Đỏ Coral/Crimson `#DC2626` / `#991B1B` làm nổi bật rủi ro và các điểm nóng cảnh báo.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     CCIP EXECUTIVE STORYBOARD                           │
│                                                                         │
│   ┌───────────────────────────┐       ┌───────────────────────────┐     │
│   │ PAGE 1: OVERVIEW          │ ────► │ PAGE 2: RISK SEGMENTS     │     │
│   │ - Portfolio KPIs (184.2B) │       │ - Quartiles Q1 → Q4       │     │
│   │ - Baseline DR (8.07%)     │       │ - Monotonicity Gradient   │     │
│   └─────────────┬─────────────┘       └─────────────┬─────────────┘     │
│                 │                                   │                   │
│                 ▼                                   ▼                   │
│   ┌───────────────────────────┐       ┌───────────────────────────┐     │
│   │ PAGE 3: RISK HOTSPOTS     │ ◄──── │ PAGE 4: BORROWER PROFILE  │     │
│   │ - Heatmap Q4 × T1 (19.91%)│       │ - Demographics (<25 Age)  │     │
│   │ - 2.10B Exposure at Risk  │       │ - Income & Education      │     │
│   └───────────────────────────┘       └───────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2. Chi tiết Cấu trúc Từng Trang Báo cáo (P1 → P4)
1. **Trang 1: Portfolio Overview (Tổng quan Danh mục Tín dụng):**
   - KPI Cards trung tâm: Tổng dư nợ (`184.2B CU`), Tổng đơn vay (`307.5K`), Tỷ lệ vỡ nợ nền tảng (`8.07%`), Tổng giá trị chịu rủi ro (`~13.8B CU`).
   - Visual cơ cấu sản phẩm vay và phân bổ địa lý, thiết lập điểm neo tham chiếu cho toàn bộ báo cáo.
2. **Trang 2: Risk Segments (Phân tầng Rủi ro Tín dụng Q1–Q4):**
   - Biểu đồ phân bổ hồ sơ và tỷ lệ vỡ nợ theo 4 nhóm phân vị điểm tín dụng ngoài.
   - Thể hiện trực quan khoảng cách rủi ro gấp 6.38 lần giữa Q4 (17.28%) và Q1 (2.71%).
3. **Trang 3: Risk Hotspots Drill-down (Đào sâu Vùng Điểm nóng Rủi ro):**
   - Trọng tâm là Ma trận nhiệt (Matrix Heatmap) kết hợp `Risk Quartiles` và `Affordability Tiers`.
   - Ba KPI Cards cảnh báo độc quyền vùng nguy hiểm Q4 × T1: Tỷ lệ vỡ nợ (`19.91%`), Quy mô hồ sơ (`16,158 apps`), Dư nợ phơi nhiễm (`2.10B CU`).
4. **Trang 4: Borrower Risk Profile (Hồ sơ Khách hàng & Nhân khẩu học):**
   - Ma trận phân tích đa chiều giữa Trình độ học vấn và Nhóm thu nhập.
   - Biểu đồ phân hóa theo độ tuổi làm nổi bật nguy cơ tại nhóm trẻ tuổi (< 25 tuổi: 12.31%).

### 4.3. Thiết kế Hệ thống Đo lường Tập trung (Centralized DAX Architecture)
Toàn bộ logic nghiệp vụ và định dạng màu sắc động được đóng gói tập trung trong bảng `_Measures`:
- `Default Rate % = DIVIDE(CALCULATE(COUNTROWS(fact_loan), fact_loan[is_default] = 1), COUNTROWS(fact_loan), 0)`
- `Total Loan Exposure = SUM(fact_loan[loan_amount])`
- `Heatmap Cell Color`: Hàm DAX nội suy mã màu HEX động dựa trên ngưỡng vỡ nợ thực tế để tự động cảnh báo thị giác trên bảng ma trận nhiệt.

### 4.4. Đánh giá Trải nghiệm Người dùng Điều hành (Executive UX Validation)
Hệ thống dashboard đã vượt qua bài kiểm tra chấp nhận người dùng điều hành (T9 Acceptance Protocol) với kết quả đạt chuẩn tuyệt đối (PASS) trên cả 5 tiêu chí: Nhận diện quy mô baseline (P1), Nắm bắt tính đơn điệu rủi ro (P2), Đọc chính xác điểm nóng Q4 × T1 (P3), Nhận diện nhóm khách hàng trẻ tuổi (P4), và Khả năng tự giải thích mà không cần hỗ trợ kỹ thuật.

---

# CHƯƠNG 5: PHÂN TÍCH DỰ ĐOÁN & KHẢ NĂNG GIẢI THÍCH MÔ HÌNH MÁY HỌC

### 5.1. Thiết kế Thực nghiệm & Cơ chế Chia Dữ liệu Không Rò rỉ (60/20/20 Stratified Split)
Để ngăn chặn hiện tượng rò rỉ dữ liệu (Data Leakage), quy trình phân chia dữ liệu 3 tập phân tầng (Stratified Split) được áp dụng:

```
                     307,511 HỒ SƠ TOÀN DANH MỤC
                                 │
     ┌───────────────────────────┴───────────────────────────┐
     ▼ (80% Train-Val: 246,008)                              ▼ (20% Holdout)
┌─────────────────────────┐                             ┌─────────────────────────┐
│ TRAIN SET: 184,506 (60%)│                             │ TEST SET: 61,503 (20%)  │
│ Huấn luyện mô hình      │                             │ Đánh giá độc lập FINAL  │
└────────────┬────────────┘                             │ (Chỉ dùng 1 lần duy nhất│
             │                                          └─────────────────────────┘
             ▼ (20% Total)                                           ▲
┌─────────────────────────┐                                          │
│ VALIDATION SET: 61,502  │                                          │
│ - Early Stopping        │                                          │
│ - Threshold Trade-off   │ ─────────────────────────────────────────┘
└─────────────────────────┘
```

* **Train Set (60.0% - 184,506 dòng):** Dùng để huấn luyện trọng số mô hình; tỷ lệ vỡ nợ duy trì đúng `8.07%`.
* **Validation Set (20.0% - 61,502 dòng):** Dùng làm tập dữ liệu giám sát điểm dừng sớm (Early Stopping) của LightGBM và thực hiện phân tích đánh đổi ngưỡng; tỷ lệ vỡ nợ `8.07%`.
* **Test Set (20.0% - 61,503 dòng):** Tập kiểm thử holdout được cô lập hoàn toàn, không tham gia vào quá trình huấn luyện hay tinh chỉnh siêu tham số, chỉ được gọi đúng một lần duy nhất ở khâu đánh giá cuối cùng.

### 5.2. Mô hình Hồi quy Logistic Chuẩn mực (Logistic Regression Baseline)
- Nhằm tạo điểm đối chiếu phương pháp luận, mô hình hồi quy Logistic được huấn luyện trên cùng không gian 44 thuộc tính sau khi tiền xử lý tương ứng (Numeric chuẩn hóa qua `StandardScaler` + Categorical mã hóa qua `OneHotEncoder`).
- Thiết lập trọng số cân bằng lớp (`class_weight='balanced'`).
- **Kết quả Baseline trên Test Set:** $\text{ROC-AUC} = \mathbf{0.7526}$, $\text{Average Precision (AP)} = \mathbf{0.2373}$.

### 5.3. Mô hình Cây Quyết định Nâng cao (LightGBM Main Model)
- Mô hình chính được xây dựng dựa trên thuật toán LightGBM (Ke et al., 2017), một kiến trúc Gradient Boosting Decision Tree (GBDT) tối ưu hóa tốc độ và khả năng xử lý dữ liệu quy mô lớn thông qua cơ chế phân nhánh theo lá (leaf-wise tree growth).
- Cấu hình thuật toán: `boosting_type='gbdt'`, `learning_rate=0.05`, `num_leaves=63`, `feature_fraction=0.8`, `bagging_fraction=0.8`, `scale_pos_weight=11.39` (xử lý mất cân bằng nhãn $282,686 / 24,825$).
- Cơ chế giám sát: Early stopping 50 vòng lặp trên `Validation Set`.
- **Tiến trình huấn luyện:** Mô hình hội tụ tối ưu tại vòng lặp thứ **115 (Best Iteration = 115)** trong thời gian thực thi chỉ **22.0 giây**.

### 5.4. Đánh giá Hiệu năng Phân biệt trên Tập Kiểm thử Độc lập (Test Set Holdout)

| Mô hình Phân tích | ROC-AUC | Average Precision (AP) | Tăng trưởng so với Baseline |
| :--- | :---: | :---: | :---: |
| **Logistic Regression (Baseline)** | `0.7526` | `0.2373` | Benchmark |
| **LightGBM (Main Model)** | **`0.7636`** | **`0.2535`** | **$+1.10\text{ pp}$ ROC-AUC / $+1.62\text{ pp}$ AP** |

* **Đánh giá Chuyên môn:**
  - LightGBM đạt **ROC-AUC = 0.7636**, cho thấy mô hình có khả năng khai thác các quan hệ phi tuyến và tương tác giữa nhiều đặc trưng tốt hơn trong tập kiểm thử so với baseline Logistic Regression.
  - Chỉ số **Average Precision (AP) đạt `0.2535`** (được sử dụng làm metric chính theo khuyến nghị của Saito & Rehmsmeier, 2015 cho precision-recall evaluation trong bối cảnh class imbalance), cao gấp **3.14 lần** tỷ lệ phổ biến ngẫu nhiên của danh mục (`8.07%`), khẳng định khả năng phát hiện rủi ro vượt trội trong điều kiện dữ liệu lệch lớp nặng.
  - Báo cáo phân loại tại ngưỡng tham chiếu 0.50 đạt **Recall default = 67%** (nhận diện được 2/3 tổng số ca vỡ nợ thực tế trên tập kiểm thử).

### 5.5. Phân tích Đánh đổi Ngưỡng Vận hành trên Tập Kiểm định (Validation Threshold Trade-off)
Thực nghiệm phân tích ngưỡng trên **Validation Set** minh chứng bức tranh đánh đổi vận hành thực tế:

| Ngưỡng (Threshold) | Recall (Bao phủ vỡ nợ) | Precision (Chính xác cảnh báo) | F1-Score | Tỷ lệ Hồ sơ bị Cảnh báo (Flagged %) | Ý nghĩa Ứng dụng Nghiệp vụ |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **0.15** | 97.7% | 9.1% | 0.167 | 86.3% | Sàng lọc diện rộng (Max Coverage) |
| **0.25** | **91.8%** | 10.8% | 0.194 | 68.3% | **Cảnh báo sớm rộng (Early Warning)** |
| **0.40** | **78.1%** | 14.1% | 0.239 | 44.6% | **Cân bằng Vận hành (Operational Balance)** |
| **0.50** | **66.2%** | 17.0% | 0.271 | 31.3% | **Tập trung Rủi ro cao (High-Risk Focus)** |

* **Kết luận Phương pháp luận:** Không tồn tại một ngưỡng cắt "tối ưu tuyệt đối" duy nhất về mặt toán học; việc lựa chọn ngưỡng phụ thuộc vào **Ma trận Chi phí Doanh nghiệp (Cost Matrix)** giữa chi phí tổn thất do bỏ lọt nợ xấu (False Negative) và chi phí xử lý / cơ hội mất khách hàng tốt (False Positive).

### 5.6. Ước lượng Mức độ Đóng góp Thuộc tính bằng SHAP (Global Explainability Estimation)
Để giải thích đóng góp của các thuộc tính trong mô hình hộp đen, nghiên cứu áp dụng khung lý thuyết Shapley Additive Explanations (SHAP) từ lý thuyết trò chơi hợp tác (Lundberg & Lee, 2017). Giá trị SHAP được tính toán trên mẫu ngẫu nhiên **5,000 hồ sơ từ Test Set** nhằm ước lượng mức độ đóng góp dự đoán toàn cục:

```
TOP 10 BIẾN QUAN TRỌNG NHẤT THEO MEAN |SHAP|
────────────────────────────────────────────────────────────────────────
 1. ext_score_avg           ██████████████████████████████  0.4320
 2. ext_score_3             ███████████                     0.1532
 3. loan_to_value           █████████                       0.1308
 4. years_employed          ████████                        0.1140
 5. ext_score_1             ████████                        0.1130
 6. ext_score_2             ███████                         0.1004
 7. occupation_type         ██████                          0.0926
 8. code_gender             ██████                          0.0891
 9. name_education_type     █████                           0.0827
10. flag_own_car            █████                           0.0798
────────────────────────────────────────────────────────────────────────
```

* **Phát hiện Trọng tâm:**
  - `ext_score_avg` (`Mean |SHAP| = 0.4320`) có mức đóng góp dự đoán trung bình cao nhất trong LightGBM, lớn gấp **2.82 lần** thuộc tính xếp thứ hai (`ext_score_3`). Kết quả này nhất quán với phát hiện mô tả trước đó về sự phân tầng rủi ro đơn biến theo Q1–Q4.
  - `loan_to_value` xếp thứ 3 (`0.1308`), cho thấy đòn bẩy tài chính là tín hiệu dự đoán quan trọng bổ sung cho điểm tín dụng.
  - `years_employed` xếp thứ 4 (`0.1140`), khẳng định giá trị thực tế của công tác tiền xử lý chất lượng dữ liệu (`DAYS_EMPLOYED = 365243`).

### 5.7. Kiểm định Đối chiếu Tính Nhất quán (SQL DWH vs ML Consistency Analysis)
Kiểm tra chéo giữa tầng Thống kê Mô tả DWH và tầng Dự đoán Máy học mang lại sự trùng khớp:

1. **Đối chiếu Vùng Điểm nóng Q4 × T1:**
   - **Tỷ lệ vỡ nợ SSOT SQL DWH:** **`19.91%`**
   - **Tỷ lệ vỡ nợ thực tế trên Test Set:** **`19.90%`** (Độ lệch chỉ **`0.01 pp`** — Khớp).
   - **Điểm số mô hình trung bình (Mean Model Risk Score):** **`67.48`** (Mô hình xếp nhóm này vào thang điểm rủi ro cao nhất).
2. **Đối chiếu Phân tầng Rủi ro Q1 → Q4:**

| Phân khúc Rủi ro | Tỷ lệ Vỡ nợ SQL DWH | Tỷ lệ Vỡ nợ Thực tế Test Set | Độ lệch (Gap) | Điểm số Rủi ro Mô hình (Mean Risk Score) |
| :--- | :---: | :---: | :---: | :---: |
| **Q1 - Lowest Risk** | 2.71% | 2.73% | $+0.02\text{ pp}$ | **19.32** |
| **Q2 - Low-Moderate** | 4.58% | 4.60% | $+0.02\text{ pp}$ | **30.23** |
| **Q3 - Moderate-High** | 7.71% | 8.44% | $+0.73\text{ pp}$ | **45.35** |
| **Q4 - Highest Risk** | 17.28% | 18.82% | $+1.54\text{ pp}$ | **66.30** |

* **Đánh giá Phương pháp luận:** Độ lệch nhỏ ($+0.02\text{ pp}$ tại Q1/Q2) nằm trong phạm vi dao động chọn mẫu ngẫu nhiên (sampling variance). Tính chất đơn điệu được bảo toàn nguyên vẹn trên cả dữ liệu thực tế và thang điểm xếp hạng rủi ro của máy học.

---

# CHƯƠNG 6: MA TRẬN PHÁT HIỆN & KHUYẾN NGHỊ KINH DOANH

### 6.1. Khung Cấu trúc Phân cấp Quyết định 3 Tầng (Decision Framework)
Tuân thủ quy chuẩn `dashboard-insight-workflow`, mọi đề xuất hành động được phân định rành mạch theo 3 cấp độ:
- **Level 1 — Descriptive Action (Hành động Mô tả / Giám sát):** Tiếp tục điều tra, drill-down dữ liệu bổ sung, chưa thay đổi quy trình vận hành.
- **Level 2 — Operational Action (Hành động Vận hành):** Điều chỉnh quy trình linh hoạt, có thể đảo ngược dễ dàng: phân luồng thẩm định, tăng cường xác minh chứng từ, thử nghiệm pilot.
- **Level 3 — Policy Action (Hành động Chính sách Tín dụng):** Thay đổi quy chế phê duyệt chính thức, điều chỉnh trần hạn mức, tái định giá lãi suất. Đòi hỏi bằng chứng thống kê vững chắc và được phê duyệt bởi Hội đồng Quản trị Rủi ro.

### 6.2. Ma trận 5 Phát hiện Trọng yếu & Khuyến nghị Hành động

#### INS-001: Phân tầng Rủi ro Đơn biến theo Điểm Tín dụng Ngoài
* **Bằng chứng (Evidence):** Tỷ lệ vỡ nợ nhóm Q4 (`17.28%`) cao gấp 6.38 lần nhóm Q1 (`2.71%`); khoảng 43.5% số ca default quan sát được trong danh mục thuộc nhóm Q4.
* **Đề xuất Hành động:**
  - `[Operational Action - Level 2]`: Phân luồng thẩm định: Triển khai luồng phê duyệt nhanh tự động (Fast-track STP) cho nhóm Q1; ưu tiên chuyển nhóm Q4 sang luồng thẩm định nâng cao (enhanced/manual review) thay vì tự động từ chối. Việc áp dụng hard decline chỉ được xem xét sau khi có cost matrix, validation bổ sung và governance review.
  - `[Policy Action - Level 3]`: Xem xét áp dụng cơ chế Định giá Lãi suất theo Rủi ro (Risk-Based Pricing) với biên độ bù rủi ro cho nhóm Q3–Q4.
* **Owner:** *Underwriting Operations Lead & Credit Risk Committee*.

#### INS-002: Hotspot Rủi ro Tập trung Đa biến Q4 × T1
* **Bằng chứng (Evidence):** Điểm nóng Q4 × T1 có default rate **`19.91%`** (thực nghiệm ML Test Set: `19.90%`), gắn liền với **2.10 tỷ CU** dư nợ trên 16,158 hồ sơ.
* **Đề xuất Hành động:**
  - `[Operational Action - Level 2]`: Tăng cường thẩm định xác minh dòng tiền thực tế qua sao kê tài khoản ngân hàng hoặc yêu cầu người đồng bảo lãnh đối với hồ sơ thuộc giao điểm Q4 × T1.
  - `[Policy Action - Level 3]`: Xem xét điều chỉnh cấu trúc khoản vay nhằm cải thiện affordability (ví dụ: giảm hạn mức vay hoặc giãn kỳ hạn vay); ngưỡng 4.5x hiện chỉ là empirical/statistical threshold của nghiên cứu và chưa được xem là ngưỡng chính sách tín dụng chính thức.
* **Owner:** *Chief Risk Officer (CRO) & Verification Lead*.

#### INS-003: Phân khúc Nhân khẩu học Trẻ tuổi (< 25 tuổi)
* **Bằng chứng (Evidence):** Tỷ lệ vỡ nợ nhóm < 25 tuổi đạt **`12.31%`** (+4.24 pp so với baseline). SHAP xác nhận độ tuổi xếp thứ 8 trong các biến số định lượng.
* **Đề xuất Hành động:**
  - `[Descriptive Action - Level 1]`: Phân tích chuyên sâu ma trận Tuổi × Thâm niên làm việc để bóc tách yếu tố gây nhiễu trước khi can thiệp chính sách.
  - `[Operational Action - Level 2]`: Không từ chối cực đoan; nghiên cứu triển khai chương trình tín dụng khởi điểm (Starter Credit Program) với hạn mức nhỏ và cơ chế nâng hạn mức theo hành vi trả nợ tích cực.
  - `[Policy Action - Level 3]`: *Chưa khuyến nghị thay đổi Policy loại trừ nhóm tuổi này* nhằm đảm bảo chuẩn mực đạo đức tín dụng (Fair Lending).
* **Owner:** *Customer Segment Manager & Retail Lending Team*.

#### INS-004: Phân hóa theo Loại hình Thu nhập & Học vấn
* **Bằng chứng (Evidence):** Nhóm học vấn đại học (`5.36%`) và công chức nhà nước (`5.77%`) có rủi ro thấp hơn đáng kể so với lao động tự do (`9.59%`) và học vấn phổ thông cơ sở (`10.93%`).
* **Đề xuất Hành động:**
  - `[Operational Action - Level 2]`: Thiết kế gói sản phẩm ưu đãi thủ tục và lãi suất dành riêng cho nhóm Prime (State Servant / Higher Education) để mở rộng danh mục an toàn.
  - `[Operational Action - Level 2]`: Đánh giá tính ổn định và thời gian duy trì nguồn thu trong quy trình underwriting đối với nhóm Working; ngưỡng thâm niên cụ thể cần được xác định qua phân tích bổ sung và thử nghiệm pilot trước khi đưa vào policy chính thức.
* **Owner:** *Product Development Lead & Retail Underwriting Lead*.

#### INS-005: Xếp hạng Rủi ro Dự đoán bằng Mô hình Máy học (Predictive Risk Ranking)
* **Bằng chứng (Evidence):** LightGBM đạt ROC-AUC `0.7636` và PR-AUC `0.2535` trên tập Test độc lập, cho thấy mô hình có khả năng phân biệt tương đối giữa hồ sơ có và không có default; SHAP chỉ ra vai trò chi phối của `ext_score_avg`, `ext_score_3` và `loan_to_value`.
* **Bối cảnh & Định vị:** Kết quả mô hình được sử dụng để hỗ trợ **phân loại rủi ro (Risk Triage) và ưu tiên review**, không thay thế quyết định tín dụng tự động.
* **Đề xuất Hành động:**
  - `[Operational Action - Level 2]`: Tích hợp điểm số rủi ro của LightGBM làm Hệ thống Cảnh báo Sớm (Early Warning Score), ưu tiên hồ sơ cần kiểm tra chuyên sâu cho đội ngũ thẩm định.
  - `[Descriptive Action - Level 1]`: Phối hợp với bộ phận Tài chính xây dựng Ma trận Chi phí Tổn thất để xác định điểm cắt (Cut-off Threshold) tối ưu tài chính.
* **Owner:** *Head of Data Science & Credit Risk Modeling Manager*.

### 6.3. Bảng Phân công Trách nhiệm & Thực thi (Action Plan & Owner Assignment)

| Insight ID | Trọng tâm Rủi ro | Cấp độ Quyết định | Hành động Đề xuất Cụ thể | Người chịu trách nhiệm (Owner) | Thời hạn / Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INS-001** | External Score (Q1 vs Q4) | **Level 2 (Operational)** | Fast-track STP cho Q1; Chuyển Q4 sang enhanced review | Underwriting Lead | Triển khai ngay |
| **INS-001** | External Score (Q1 vs Q4) | **Level 3 (Policy)** | Xem xét Ma trận Lãi suất theo Rủi ro (Risk-Based Pricing) | Credit Risk Committee | Q1 Tiếp theo |
| **INS-002** | Hotspot Q4 × T1 | **Level 2 (Operational)** | Tăng cường sao kê ngân hàng / người bảo lãnh với nhóm Q4 × T1 | Verification Lead | Khẩn cấp |
| **INS-002** | Hotspot Q4 × T1 | **Level 3 (Policy)** | Nghiên cứu điều chỉnh hạn mức/kỳ hạn nhằm cải thiện affordability | CRO & Risk Committee | Q1 Tiếp theo |
| **INS-003** | Khách hàng Trẻ (<25) | **Level 1 (Descriptive)** | Phân tích sâu ma trận Độ tuổi × Thâm niên làm việc | Risk Analytics Team | 1 Tháng |
| **INS-003** | Khách hàng Trẻ (<25) | **Level 2 (Operational)** | Nghiên cứu gói Starter Credit Program (Hạn mức nhỏ, tăng dần) | Product & Lending Lead | Nghiên cứu Pilot |
| **INS-004** | Nghề nghiệp & Học vấn | **Level 2 (Operational)** | Gói vay ưu đãi cho Prime; Đánh giá độ ổn định nguồn thu nhóm Working | Retail Product Lead | 2 Tháng |
| **INS-005** | ML Risk Ranking | **Level 2 (Operational)** | Tích hợp Risk Score làm Hệ thống Cảnh báo Sớm (Early Warning Triage) | Risk Modeling Team | Pilot thẩm định |
| **INS-005** | ML Threshold Cut-off | **Level 1 (Descriptive)** | Xây dựng Business Cost Matrix để tính điểm cut-off tối ưu | Risk & Finance Team | 1 Tháng |

---

# CHƯƠNG 7: GIỚI HẠN ĐỀ TÀI & HƯỚNG PHÁT TRIỂN MỞ RỘNG

### 7.1. Giới hạn Dữ liệu Cắt ngang & Kiểm định Thời gian (Temporal & Point-in-Time Limitations)
1. **Bản chất Dữ liệu Chụp Cắt ngang (Point-in-Time Snapshot):**
   - Tập dữ liệu phản ánh thông tin tại thời điểm nộp hồ sơ vay. Đề tài chưa tiếp cận được dữ liệu chuỗi thời gian nhiều kỳ (Longitudinal Tracking) để theo dõi hành vi trả nợ phát sinh theo từng tháng sau giải ngân.
2. **Giới hạn Kiểm định Thời gian (Temporal Validation Limitation):**
   - Dữ liệu hiện tại chủ yếu là application-level và chưa cho phép đánh giá đầy đủ model stability theo thời gian. Do thiếu dữ liệu các đợt phát hành khoản vay theo các năm khác nhau (Out-of-Time Validation), mô hình chưa thể đánh giá chỉ số ổn định dân số (Population Stability Index - PSI) hay sự dịch chuyển của các thuộc tính rủi ro qua các chu kỳ suy thoái kinh tế.

### 7.2. Giới hạn Mô hình & Vấn đề Hiệu chỉnh Xác suất (Probability Calibration & Scoring Limits)
1. **Tính chất Điểm số Xếp hạng Rủi ro (Uncalibrated Risk Score):**
   - Do áp dụng kỹ thuật cân bằng mẫu `scale_pos_weight = 11.39`, điểm số đầu ra của LightGBM mang bản chất là **Thang đo Xếp hạng Rủi ro Tương đối (Monotonic Risk Ranking)**, chưa phải là Xác suất Vỡ nợ Tuyệt đối (Calibrated Probability of Default - PD).
   - Con số dự đoán trung bình tại nhóm Q4 × T1 (`67.48`) phản ánh mức độ báo động rủi ro của thuật toán, không đồng nhất với tỷ lệ vỡ nợ danh mục thực tế (`19.90%`).
2. **Tương quan và Nhân quả (Correlation vs Causality):**
   - Các thuộc tính có Mean |SHAP| cao như `ext_score_avg` hay `loan_to_value` chỉ phản ánh mối liên kết thống kê dự đoán mạnh mẽ, không khẳng định mối quan hệ nhân quả trực tiếp.

### 7.3. Lộ trình Nâng cấp Hệ thống Quản trị Rủi ro Sản xuất (Future Roadmap)
Từ nền tảng CCIP hiện tại, lộ trình nâng cấp thành một hệ thống quản trị rủi ro sản xuất toàn diện bao gồm:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       CURRENT CCIP ACHIEVEMENTS                         │
│  - Star Schema SSOT Data Warehouse (307,511 rows)                       │
│  - Executive Power BI Storyboard (P1 → P4)                              │
│  - Predictive Risk Ranking (ROC-AUC 0.7636, AP 0.2535)                  │
│  - SHAP Explainability & Consistent Hotspot Validation                  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 FUTURE PRODUCTION RISK SYSTEM ROADMAP                   │
│                                                                         │
│  1. TEMPORAL VALIDATION & OUT-OF-TIME TESTING (OOT)                     │
│     - Kiểm thử mô hình trên các vintage giải ngân khác nhau             │
│     - Giám sát độ ổn định thuộc tính (PSI / Characteristic Drift)       │
│                                                                         │
│  2. PROBABILITY CALIBRATION & SCORECARD DEVELOPMENT                     │
│     - Hiệu chỉnh xác suất qua Isotonic Regression / Platt Scaling       │
│     - Chuyển đổi xác suất thành thang điểm tín dụng chuẩn (Credit Score)│
│                                                                         │
│  3. COST-SENSITIVE OPTIMIZATION & AUTOMATED DECISIONING                 │
│     - Tích hợp Ma trận Chi phí Tổn thất Tài chính thực tế               │
│     - Tự động hóa điểm cắt tối ưu cho hệ thống Decision Engine sản xuất │
└─────────────────────────────────────────────────────────────────────────┘
```

---

# TỔNG KẾT BÁO CÁO

Công trình nghiên cứu và xây dựng **Consumer Credit Intelligence Platform (CCIP)** đã hoàn thành trọn vẹn chuỗi giá trị phân tích kinh doanh hiện đại:
$$\text{Data Engineering (SSOT)} \longrightarrow \text{Descriptive BI (Dashboard)} \longrightarrow \text{Predictive ML (Ranking \& SHAP)} \longrightarrow \text{Actionable Governance}$$

Hệ thống cung cấp một cơ sở khoa học vững chắc, vừa trực quan hóa sâu sắc bức tranh rủi ro danh mục tín dụng phục vụ ban điều hành, vừa mở ra công cụ xếp hạng dự đoán thông minh hỗ trợ đội ngũ thẩm định, đồng thời xác lập ma trận khuyến nghị kinh doanh có trách nhiệm và phân cấp rõ ràng.

---

# TÀI LIỆU THAM KHẢO (REFERENCES)

1. **Basel Committee on Banking Supervision (BCBS).** (2006). *International Convergence of Capital Measurement and Capital Standards: A Revised Framework (Basel II)*. Bank for International Settlements.
2. **Breiman, L.** (2001). *Statistical Modeling: The Two Cultures*. Statistical Science, 16(3), 199-231.
3. **Few, S.** (2006). *Information Dashboard Design: The Effective Visual Communication of Data*. O'Reilly Media.
4. **Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y.** (2017). *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*. Advances in Neural Information Processing Systems (NeurIPS), 30, 3146-3154.
5. **Kimball, R., & Ross, M.** (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling* (3rd ed.). John Wiley & Sons.
6. **Lundberg, S. M., & Lee, S. I.** (2017). *A Unified Approach to Interpreting Model Predictions*. Advances in Neural Information Processing Systems (NeurIPS), 30, 4765-4774.
7. **Saito, T., & Rehmsmeier, M.** (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*. PLOS ONE, 10(3), e0118432.
8. **Thomas, L. C., Crook, J. N., & Edelman, D. B.** (2017). *Credit Scoring and Its Applications* (2nd ed.). SIAM - Society for Industrial and Applied Mathematics.
