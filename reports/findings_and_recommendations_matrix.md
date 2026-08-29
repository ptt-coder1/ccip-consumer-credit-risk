# CCIP — Giai đoạn 7: Tổng hợp Findings & Ma trận Khuyến nghị Kinh doanh
## (Findings & Business Recommendations Matrix)

> **Dự án:** Consumer Credit Intelligence Platform (CCIP)  
> **Bộ dữ liệu chuẩn hóa:** 307,511 hồ sơ vay (`dw.fact_loan` + `dw.dim_customer` + `dw.dim_region`)  
> **Portfolio Default Rate (Baseline SSOT):** **8.07%** (24,825 ca vỡ nợ) | **Total Loan Exposure:** **184.2B CU**  
> **Phương pháp luận:** Tuân thủ chuẩn 9 bước `dashboard-insight-workflow` (Data → Analysis → Context → Evidence/Materiality → Decision Level → Decision Owner → Limitations).

---

## 📑 MỤC LỤC
1. [Khung Cấu trúc Quyết định (Decision Framework)](#1-khung-cấu-trúc-quyết-định-decision-framework)
2. [Ma trận Tổng hợp Findings & Khuyến nghị (Matrix 5 Insights)](#2-ma-trận-tổng-hợp-findings--khuyến-nghị-matrix-5-insights)
   - [INS-001: Điểm Tín dụng Bên ngoài & Phân tầng Rủi ro Đơn biến](#ins-001-điểm-tín-dụng-bên-ngoài--phân-tầng-rủi-ro-đơn-biến)
   - [INS-002: Hotspot Rủi ro Tập trung Q4 × T1 (Đa biến)](#ins-002-hotspot-rủi-ro-tập-trung-q4--t1-đa-biến)
   - [INS-003: Phân khúc Nhân khẩu học Trẻ tuổi (< 25 tuổi)](#ins-003-phân-khúc-nhân-khẩu-học-trẻ-tuổi--25-tuổi)
   - [INS-004: Loại hình Thu nhập & Trình độ Học vấn](#ins-004-loại-hình-thu-nhập--trình-độ-học-vấn)
   - [INS-005: Mô hình Máy học Dự đoán & Ước lượng Đóng góp SHAP](#ins-005-mô-hình-máy-học-dự-đoán--ước-lượng-đóng-góp-shap)
3. [Bảng Tổng hợp Quyết định & Phân công Trách nhiệm (Action Plan & Owner Matrix)](#3-bảng-tổng-hợp-quyết-định--phân-công-trách-nhiệm-action-plan--owner-matrix)
4. [Giới hạn Phương pháp luận & Khuyến cáo Thực thi](#4-giới-hạn-phương-pháp-luận--khuyến-cáo-thực-thi)

---

## 1. KHUNG CẤU TRÚC QUYẾT ĐỊNH (DECISION FRAMEWORK)

Mọi khuyến nghị kinh doanh trong CCIP được phân loại nghiêm ngặt theo 3 cấp độ quyết định:

* **Level 1 — Descriptive Action (Hành động Mô tả / Giám sát):** Tiếp tục theo dõi, drill-down điều tra dữ liệu, thu thập thêm biến số phụ trợ. Không thay đổi quy trình vận hành. *(Owner: BI / Risk Analytics Team)*
* **Level 2 — Operational Action (Hành động Vận hành):** Điều chỉnh quy trình nghiệp vụ có tính linh hoạt, rủi ro thấp và có thể đảo ngược: tăng cường thẩm định thủ công, yêu cầu bổ sung chứng từ, siết luồng phê duyệt tự động. *(Owner: Underwriting Team / Operations Lead)*
* **Level 3 — Policy Action (Hành động Chính sách Tín dụng):** Điều chỉnh Credit Policy chính thức (hạn mức, trần LTV, chặn nhóm khách hàng, thay đổi lãi suất rủi ro). Đòi hỏi bằng chứng thống kê vững chắc, loại trừ yếu tố gây nhiễu (confounding factors) và qua hội đồng phê duyệt. *(Owner: Risk Committee / Head of Credit Risk)*

---

## 2. MA TRẬN TỔNG HỢP FINDINGS & KHUYẾN NGHỊ (MATRIX 5 INSIGHTS)

---

### INS-001: Điểm Tín dụng Bên ngoài & Phân tầng Rủi ro Đơn biến
* **Mã RQ liên quan:** RQ1 & RQ2 (Risk Profile & External Credit Scoring Monotonicity)
* **Bằng chứng Dữ liệu (Data & SSOT Evidence):**
  - Portfolio Baseline: **8.07%**.
  - Tỷ lệ vỡ nợ tăng đơn điệu (Monotonic) từ nhóm điểm cao xuống thấp:
    - **Q1 (Lowest Risk, ext_score_avg ≥ 0.6276):** Default rate **`2.71%`** (Tỷ lệ vỡ nợ thấp hơn baseline 5.36 pp; chiếm 23.8% danh mục).
    - **Q2 (Low-Moderate, 0.5144 ≤ score < 0.6276):** Default rate **`4.58%`**.
    - **Q3 (Moderate-High, 0.3868 ≤ score < 0.5144):** Default rate **`7.71%`**.
    - **Q4 (Highest Risk, ext_score_avg < 0.3868):** Default rate **`17.28%`** (Cao gấp **2.14 lần** baseline; cao gấp **6.38 lần** nhóm Q1).
  - Tương quan Pearson tuyến tính âm mạnh nhất trong các biến số: `r = -0.2229`.
* **Bối cảnh Phân tích (Context):** `[Evidence-backed]`
  - Điểm số tín dụng bên ngoài (tổng hợp từ các tổ chức chấm điểm tín dụng độc lập) phản ánh lịch sử trả nợ quá khứ của khách hàng trên toàn hệ thống tài chính.
* **Kiểm định Bằng chứng & Giới hạn (Evidence / Limitation Check):**
  - **Correlation vs Causation:** Correlation mạnh. Điểm thấp không trực tiếp "gây ra" vỡ nợ, mà phản ánh xác suất rủi ro cao của hành vi tài chính trong quá khứ.
  - **Selection Bias:** Nhóm khách hàng nộp đơn đã vượt qua một số bộ lọc sơ bộ, tuy nhiên `ext_score_avg` có độ bao phủ cao (chỉ 33 trường hợp thiếu điểm trên tập Test).
* **Đánh giá Trọng yếu Kinh doanh (Materiality Check):**
  - **Cực kỳ trọng yếu:** Chênh lệch rủi ro giữa Q4 (17.28%) và Q1 (2.71%) lên tới **14.57 pp**. Khoảng 43.5% số ca default quan sát được trong danh mục thuộc về nhóm Q4.
* **Đề xuất Hành động (Decisions):**
  - `[Operational Action - Level 2]`: Phân luồng luồng phê duyệt: Fast-track STP cho nhóm Q1; ưu tiên chuyển nhóm Q4 sang luồng thẩm định nâng cao (enhanced/manual review) thay vì tự động từ chối. Việc áp dụng hard decline chỉ được xem xét sau khi có cost matrix, validation bổ sung và governance review.
  - `[Policy Action - Level 3]`: Xem xét áp dụng cơ chế Định giá Lãi suất theo Rủi ro (Risk-Based Pricing) với biên độ bù rủi ro cho nhóm Q3–Q4.
* **Người chịu trách nhiệm (Decision Owner):**
  - Operational: *Underwriting Operations Lead*.
  - Policy: *Credit Risk Committee*.

---

### INS-002: Hotspot Rủi ro Tập trung Q4 × T1 (Đa biến)
* **Mã RQ liên quan:** RQ3 & RQ5 (Multivariate Risk Hotspot & Affordability Stress)
* **Bằng chứng Dữ liệu (Data & SSOT Evidence):**
  - Ma trận nhiệt kết hợp giữa **Điểm tín dụng (Q1–Q4)** và **Tỷ lệ Bao phủ Thu nhập/Trả góp (Affordability Tiers T1–T4)**:
    - **Vùng điểm nóng (Hotspot Q4 × T1):** Hồ sơ có điểm tín dụng thấp (`ext_score_avg < 0.3868`) kết hợp gánh nặng trả góp cao (`income_to_annuity < 4.5x`).
    - Tỷ lệ vỡ nợ Hotspot: **`19.91%`** (Cao gấp **2.47 lần** baseline danh mục).
    - Quy mô bị ảnh hưởng: **16,158 hồ sơ** (chiếm 5.25% toàn bộ danh mục).
    - Dư nợ chịu rủi ro (Exposure at Risk): **2.10 tỷ CU** (trên tổng 184.2B CU).
  - Đối chiếu thực nghiệm ML Test Set: Tỷ lệ vỡ nợ thực tế nhóm này là **19.90%** (Gap so với SSOT chỉ `0.01 pp`), điểm số rủi ro mô hình trung bình là **67.48**.
* **Bối cảnh Phân tích (Context):** `[Evidence-backed]`
  - Rủi ro vỡ nợ tăng phi tuyến khi khách hàng vừa có uy tín tín dụng thấp trong quá khứ, vừa có đòn bẩy trả nợ vượt quá khả năng tài chính hiện tại (hiệu ứng cộng hưởng rủi ro đa chiều).
* **Kiểm định Bằng chứng & Giới hạn (Evidence / Limitation Check):**
  - Dữ liệu thu nhập là tự khai báo tại thời điểm nộp đơn (self-reported income) nên có thể có sai số đo lường; tuy nhiên sự kết hợp chéo với điểm tín dụng bên ngoài tạo thành bộ lọc kiểm soát chéo rất vững chắc.
* **Đánh giá Trọng yếu Kinh doanh (Materiality Check):**
  - **Đặc biệt nghiêm trọng:** Gần 1/5 khách hàng trong phân khúc này không trả được nợ. 2.10 tỷ CU dư nợ đang nằm trong vùng rủi ro cực cao, đe dọa trực tiếp đến tỷ lệ nợ xấu (NPL) của tổ chức.
* **Đề xuất Hành động (Decisions):**
  - `[Operational Action - Level 2]`: Tăng cường thẩm định xác minh dòng tiền thực tế qua sao kê tài khoản ngân hàng hoặc yêu cầu người đồng bảo lãnh đối với hồ sơ thuộc giao điểm Q4 × T1.
  - `[Policy Action - Level 3]`: Xem xét điều chỉnh cấu trúc khoản vay nhằm cải thiện affordability (ví dụ: giảm hạn mức vay hoặc giãn kỳ hạn vay); ngưỡng 4.5x hiện chỉ là empirical/statistical threshold của nghiên cứu và chưa được xem là ngưỡng chính sách tín dụng chính thức.
* **Người chịu trách nhiệm (Decision Owner):**
  - Operational: *Head of Underwriting & Verification*.
  - Policy: *Chief Risk Officer (CRO) & Credit Risk Committee*.

---

### INS-003: Phân khúc Nhân khẩu học Trẻ tuổi (< 25 tuổi)
* **Mã RQ liên quan:** RQ1 & RQ4 (Borrower Demographics & Age Segment Risk)
* **Bằng chứng Dữ liệu (Data & SSOT Evidence):**
  - Tỷ lệ vỡ nợ nhóm tuổi **< 25 tuổi**: **`12.31%`** (Cao gấp **1.53 lần** baseline danh mục `8.07%`).
  - Đường cong rủi ro theo độ tuổi giảm dần theo thời gian: `<25 (12.31%)` → `25–34 (10.02%)` → `35–44 (7.98%)` → `45–54 (6.97%)` → `55+ (5.66%)`.
  - Trong SHAP Global Importance, biến độ tuổi (`age_years`) xếp thứ 8 trong nhóm numeric features (`Mean |SHAP| = 0.0722`).
* **Bối cảnh Phân tích (Context):** `[Hypothesis - cần cẩn trọng]`
  - *Giả thuyết:* Nhóm trẻ tuổi thường có thời gian làm việc ngắn (`years_employed` thấp), công việc chưa ổn định, thiếu tài sản tích lũy và kinh nghiệm quản lý ngân sách cá nhân.
* **Kiểm định Bằng chứng & Giới hạn (Evidence / Limitation Check):**
  - **Yếu tố gây nhiễu (Confounding Factors):** Độ tuổi có tương quan nghịch với số năm làm việc (`years_employed`) và điểm tín dụng (`ext_score_avg`). Tuổi trẻ tự nó không phải là nguyên nhân trực tiếp gây vỡ nợ, mà là biến đại diện (proxy) cho tính ổn định tài chính và kinh nghiệm tín dụng.
* **Đánh giá Trọng yếu Kinh doanh (Materiality Check):**
  - Mức chênh lệch `+4.24 pp` so với baseline là đáng kể về mặt thống kê và kinh doanh. Tuy nhiên, nhóm <25 tuổi là phân khúc khách hàng tiềm năng cho vòng đời sản phẩm lâu dài (Customer Lifetime Value).
* **Đề xuất Hành động (Decisions):**
  - `[Descriptive Action - Level 1]`: Phân tích chuyên sâu ma trận Độ tuổi × Năm kinh nghiệm (`age_years` × `years_employed`) để bóc tách yếu tố gây nhiễu trước khi can thiệp chính sách.
  - `[Operational Action - Level 2]`: Không từ chối hàng loạt chỉ vì độ tuổi. Thay vào đó, nghiên cứu triển khai sản phẩm tín dụng vi mô có kiểm soát (Starter Credit Program): hạn mức khởi điểm nhỏ, theo dõi hành vi trả nợ định kỳ 6 tháng đầu để xem xét nâng hạn mức dần.
  - `[Policy Action - Level 3]`: *Chưa khuyến nghị thay đổi Credit Policy loại trừ nhóm tuổi này* do rủi ro vi phạm chuẩn mực đạo đức tín dụng (Fair Lending) và tiềm ẩn yếu tố nhiễu về thu nhập/kinh nghiệm.
* **Người chịu trách nhiệm (Decision Owner):**
  - Descriptive/Operational: *Customer Segment Manager & Risk Analytics Team*.

---

### INS-004: Loại hình Thu nhập & Trình độ Học vấn
* **Mã RQ liên quan:** RQ4 (Borrower Financial & Education Profile)
* **Bằng chứng Dữ liệu (Data & SSOT Evidence):**
  - Theo Nhóm thu nhập (`income_type`):
    - **Nhóm Lao động tự do / Công nhân (Working):** Default rate **`9.59%`** (chiếm đa số hồ sơ).
    - **Nhóm Công chức nhà nước (State Servant):** Default rate **`5.77%`** (thấp hơn baseline 2.30 pp).
    - **Nhóm Hưu trí (Pensioner):** Default rate **`5.36%`**.
  - Theo Học vấn (`education_level`):
    - **Học vấn Phổ thông cơ sở (Lower Secondary):** Default rate **`10.93%`**.
    - **Học vấn Đại học trở lên (Higher Education):** Default rate **`5.36%`** (thấp hơn 2.71 pp so với baseline).
  - SHAP xác nhận `name_education_type` (`Rank #9`, `Mean |SHAP| = 0.0827`) và `occupation_type` (`Rank #7`, `Mean |SHAP| = 0.0926`) là các biến phân loại có đóng góp lớn vào mô hình.
* **Bối cảnh Phân tích (Context):** `[Evidence-backed]`
  - Trình độ học vấn cao và công tác trong khu vực nhà nước mang lại nguồn thu nhập ổn định hơn, ít bị ảnh hưởng bởi biến động chu kỳ kinh tế vĩ mô.
* **Kiểm định Bằng chứng & Giới hạn (Evidence / Limitation Check):**
  - Mối liên hệ có tính chất đồng biến với thu nhập ròng và vị thế xã hội.
* **Đánh giá Trọng yếu Kinh doanh (Materiality Check):**
  - Phân khúc khách hàng học vấn đại học và công chức nhà nước có rủi ro thấp hơn gần 50% so với nhóm lao động phổ thông, mở ra cơ hội phát triển danh mục tín dụng an toàn (Prime Portfolio).
* **Đề xuất Hành động (Decisions):**
  - `[Operational Action - Level 2]`: Xây dựng các gói sản phẩm ưu đãi lãi suất và thủ tục giản lược dành riêng cho nhóm phân khúc chất lượng cao (State Servant / Higher Education) nhằm tăng trưởng tín dụng an toàn.
  - `[Operational Action - Level 2]`: Đánh giá tính ổn định và thời gian duy trì nguồn thu trong quy trình underwriting đối với nhóm Working; ngưỡng thâm niên cụ thể cần được xác định qua phân tích bổ sung và thử nghiệm pilot trước khi đưa vào policy chính thức.
* **Người chịu trách nhiệm (Decision Owner):**
  - *Product Development Lead & Retail Lending Underwriting Manager*.

---

### INS-005: Mô hình Máy học Dự đoán & Ước lượng Đóng góp SHAP
* **Mã RQ liên quan:** RQ6 (Predictive Default Probability & Explainability Modeling)
* **Bằng chứng Dữ liệu (Data & SSOT Evidence):**
  - Hiệu năng phân định rủi ro trên Test Set Holdout (61,503 hồ sơ):
    - **LightGBM ROC-AUC: `0.7636`** (Vượt trội hơn Logistic Regression Baseline `0.7526` là `+1.10 pp`).
    - **Average Precision (AP): `0.2535`** (Cao gấp **3.14 lần** baseline ngẫu nhiên `8.07%`).
  - Phân tích Đánh đổi Ngưỡng (Validation Set):
    - Ngưỡng **`0.25`**: Recall đạt **`91.8%`**, nhận diện được hầu hết ca vỡ nợ tiềm ẩn (phù hợp cảnh báo sớm).
    - Ngưỡng **`0.40`**: Recall đạt **`78.1%`**, Precision **`14.1%`**, tỷ lệ gắn cờ **`44.6%`** danh mục.
    - Ngưỡng **`0.50`**: Recall đạt **`66.2%`**, Precision **`17.0%`**, tỷ lệ gắn cờ **`31.3%`** danh mục.
  - Ước lượng SHAP (Mẫu ngẫu nhiên 5,000 hồ sơ): Top 3 biến đóng góp lớn nhất là `ext_score_avg` (`0.4320`), `ext_score_3` (`0.1532`), và `loan_to_value` (`0.1308`).
* **Bối cảnh Phân tích (Context):** `[Evidence-backed]`
  - Mô hình học máy phi tuyến tính cho phép nắm bắt quan hệ tương tác phức tạp giữa đòn bẩy tài chính (LTV) và điểm tín dụng ngoài, tạo ra công cụ xếp hạng rủi ro đa biến chuẩn xác hơn các bảng phân tích đơn biến truyền thống.
* **Kiểm định Bằng chứng & Giới hạn (Evidence / Limitation Check):**
  - **Xác suất chưa Calibration:** Do sử dụng kỹ thuật `scale_pos_weight = 11.39x` để bù mất cân bằng mẫu, đầu ra của mô hình đóng vai trò là **Điểm xếp hạng rủi ro (Risk Ranking Score)**, không đồng nhất với xác suất vỡ nợ tuyệt đối (PD) chuẩn mực Basel.
  - **Chưa có Ma trận Chi phí:** Chưa có Business Cost Matrix (chi phí tổn thất do False Negative vs chi phí cơ hội do False Positive) nên chưa thể chốt một ngưỡng tối ưu duy nhất cho sản xuất.
* **Đánh giá Trọng yếu Kinh doanh (Materiality Check):**
  - Việc nâng cao khả năng phân loại từ AUC 0.75 lên 0.76+ và AP 0.25 cho phép tổ chức sàng lọc hiệu quả hơn 90% các khoản vay có nguy cơ vỡ nợ trong giai đoạn nộp đơn.
* **Đề xuất Hành động (Decisions):**
  - `[Operational Action - Level 2]`: Tích hợp điểm số dự đoán của LightGBM làm **Hệ thống Cảnh báo Sớm (Early Warning Score)** hỗ trợ chuyên viên thẩm định tín dụng, ưu tiên kiểm tra kỹ các hồ sơ có Risk Score ≥ 0.40.
  - `[Operational Action - Level 2]`: Chưa áp dụng mô hình để tự động từ chối hồ sơ (No Automated Hard Rejection).
  - `[Descriptive Action - Level 1]`: Phối hợp với bộ phận Tài chính/Quản trị rủi ro xây dựng **Ma trận Chi phí Tổn thất (Cost Matrix)** để xác định ngưỡng cắt (Cut-off Threshold) chính thức trước khi triển khai vào luồng phê duyệt tín dụng sản xuất.
* **Người chịu trách nhiệm (Decision Owner):**
  - *Head of Data Science & Credit Risk Modeling Manager*.

---

## 3. BẢNG TỔNG HỢP QUYẾT ĐỊNH & PHÂN CÔNG TRÁCH NHIỆM (ACTION PLAN & OWNER MATRIX)

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

## 4. GIỚI HẠN PHƯƠNG PHÁP LUẬN & KHUYẾN CÁO THỰC THI (LIMITATIONS)

1. **Bản chất Dữ liệu Point-in-Time:**
   - Toàn bộ phân tích dựa trên dữ liệu chụp tại thời điểm nộp hồ sơ vay (Snapshot at Application). Dự án chưa có dữ liệu chuỗi thời gian (Time-series / Longitudinal Tracking) để theo dõi sự dịch chuyển rủi ro qua các chu kỳ kinh tế (Economic Cycles) hoặc đo lường chỉ số ổn định dân số (Population Stability Index - PSI).
2. **Phân biệt Tương quan và Nhân quả (Correlation vs Causality):**
   - Các thuộc tính quan trọng được xác định qua thống kê hoặc SHAP (như `ext_score_avg`, `loan_to_value`, `name_education_type`) chỉ phản ánh **sự kết hợp dự đoán (predictive association)**, không khẳng định quan hệ nguyên nhân - kết quả trực tiếp.
3. **Phạm vi Ứng dụng Mô hình Máy học:**
   - Mô hình LightGBM được xây dựng nhằm mục đích **Khám phá Tri thức & Hỗ trợ Ra Quyết định (BI & Risk Analytics Tool)**, không phải là hệ thống chấm điểm PD Scorecard tuân thủ tiêu chuẩn Basel II/III (vốn đòi hỏi quy trình hiệu chỉnh xác suất, kiểm định độ bền vững và tính giải trình pháp lý chuyên biệt).
4. **Nguyên tắc Thận trọng khi Điều chỉnh Chính sách:**
   - Các khuyến nghị cấp độ **Level 3 (Policy Action)** cần được thử nghiệm có kiểm soát (A/B Testing hoặc Pilot trên quy mô nhỏ 5–10% danh mục) trong vòng 3–6 tháng trước khi ban hành áp dụng trên diện rộng.
