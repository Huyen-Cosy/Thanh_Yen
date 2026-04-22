# Scope Register — Dự án Thanh Yến
> ideaLAB thực hiện | Kickoff: 30/03/2026  
> **Không chỉnh sửa thủ công** — mọi thay đổi qua AI Agent sau khi confirm

---

## ⚠️ PHẠM VI PHASE HIỆN TẠI

> **Phase này: Quản trị Khoản vay** — KHÔNG phải toàn bộ dòng tiền  
> Dòng tiền (Cash Flow) là scope rộng hơn, sẽ triển khai ở phase sau

| | Phase hiện tại ✅ | Phase hiện tại — Basic ⚠️ | Phase sau 🔜 |
|---|---|---|---|
| **Focus** | Quản trị khoản vay (full) | Dòng tiền — basic only | Dòng tiền tổng thể (full) |
| **Dashboard** | Tab 1, 2, 4 | Tab 3, 5 — hiển thị kết quả đã tính | Tab 3, 5 — automation + raw data |
| **Lark Base** | Loan Master, Loan Activity, Collateral Assets | Bảng nhập kết quả tính toán thủ công | Cash Balance, Cash flow tự động |
| **Mockup** | v6 — đang confirm | v6 — Tab 3, 5 đang xem xét | Phase sau |

> ⚠️ **Quy ước Tab 3 & 5 — Basic version:**  
> - Kế toán **nhập kết quả đã tính sẵn** vào Lark (không phải raw data)  
> - Dashboard chỉ **hiển thị** số liệu đó, không tự tính toán  
> - **Không bao gồm:** automation, raw data integration, drill-down phức tạp  
> - Nâng cấp lên full version → thuộc **phase sau**, tính phí riêng

---

## TỔNG QUAN REQUIREMENT

| Loại | Tổng | 🟢 Clear | 🟡 Partial | 🔴 Unclear | ⛔ Out of Phase |
|---|---|---|---|---|---|
| Lark Base — Khoản vay | 0 | 0 | 0 | 0 | 0 |
| BI — Dashboard Khoản vay | 0 | 0 | 0 | 0 | 0 |
| Business Workflow | 0 | 0 | 0 | 0 | 0 |
| UI/UX Mockup | 0 | 0 | 0 | 0 | 0 |
| **Tổng** | **0** | | | | |

---

## 📊 LARK BASE — Cấu trúc dữ liệu Khoản vay

> 3 bảng core của phase này: **Loan Master, Loan Activity, Collateral Assets**  
> Bảng Company: đã có, dùng chung. Bảng Cash Balance: phase sau.

### Loan Master (Hợp đồng vay)
| ID | Tên requirement | Field / Thay đổi | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| LRK-LM-001 | — | — | — | — | — | — | — |

### Loan Activity (Giao dịch phát sinh)
| ID | Tên requirement | Field / Thay đổi | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| LRK-LA-001 | — | — | — | — | — | — | — |

### Collateral Assets (Tài sản đảm bảo)
| ID | Tên requirement | Field / Thay đổi | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| LRK-CA-001 | — | — | — | — | — | — | — |

**Checklist clarify khi có req Lark Base:**
- [ ] Field name & data type (text / number / date / dropdown / relation)
- [ ] Required hay Optional
- [ ] Relation với bảng nào
- [ ] Validation rule
- [ ] Permission: HQ nhập hay từng công ty tự nhập
- [ ] Automation nào trigger từ field này
- [ ] Ảnh hưởng đến field tính toán hiện có không

---

## 📈 BI / DASHBOARD — Khoản vay (3 tab trong scope)

### Tab 1 — Tổng quan Dư nợ
> KPIs: Tổng dư nợ, Số khoản vay, Lãi suất TB, Kỳ hạn TB  
> Table: Chi tiết khoản vay (Mã KV, Ngân hàng, Loại vay, Ngày vay, Đáo hạn, Lãi suất, Dư nợ, KH Gốc, KH Lãi)

| ID | Tên requirement | Thành phần | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| BI-T1-001 | — | KPI / Chart / Table / Filter | — | — | — | — | — |

### Tab 2 — Lịch trả nợ
> Table: Ngân hàng, Số HĐ, Loại vay, Lãi suất, Dư nợ, Gốc trả, Lãi trả, Đáo hạn, Còn lại (ngày)

| ID | Tên requirement | Thành phần | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| BI-T2-001 | — | KPI / Chart / Table / Filter | — | — | — | — | — |

### Tab 4 — Khả năng Thế chấp
> TSDB: Giá trị thẩm định, Tỷ lệ NH, Giá trị cho vay, Trạng thái  
> Note: Cần field `parent_loan_id` để link Hạn mức ↔ Khoản vay

| ID | Tên requirement | Thành phần | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| BI-T4-001 | — | KPI / Chart / Table / Filter | — | — | — | — | — |

### Tab 3 — Vị thế Thanh khoản ⚠️ BASIC VERSION
> **Approach:** Kế toán nhập kết quả tính toán thủ công vào Lark — dashboard chỉ hiển thị  
> **Không bao gồm:** tự động tính từ raw data, drill-down theo tài khoản ngân hàng  
> **Cần clarify:** Nhập theo tần suất nào (ngày / tuần / tháng)? Ai nhập? Bảng Lark nào lưu?

| ID | Tên requirement | Thành phần | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| BI-T3-001 | Xác định fields cần nhập | Lark input table | Các chỉ tiêu thanh khoản nào cần hiển thị | — | 🔴 Unclear | Cần clarify | — |

**Câu hỏi cần confirm trước khi build:**
- [ ] Các KPI cụ thể cần hiển thị là gì? (Tồn quỹ? Dư nợ ngắn hạn? Hệ số thanh khoản?)
- [ ] Tần suất nhập: hàng ngày / tuần / tháng?
- [ ] Nhập theo từng công ty hay tổng hợp HQ nhập?
- [ ] Có cần so sánh với kỳ trước không?

---

### Tab 5 — So sánh KH/TT ⚠️ BASIC VERSION
> **Approach:** Kế toán nhập số Kế hoạch + Thực hiện vào Lark — dashboard tính chênh lệch  
> **Không bao gồm:** kéo tự động từ hệ thống kế hoạch, phân tích variance tự động  
> **Cần clarify:** Kế hoạch được lập ở đâu hiện tại? Ai là người nhập TH hàng tháng?

| ID | Tên requirement | Thành phần | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| BI-T5-001 | Xác định chỉ tiêu KH/TT | Lark input table | Các chỉ tiêu nào cần so sánh KH vs TT | — | 🔴 Unclear | Cần clarify | — |

**Câu hỏi cần confirm trước khi build:**
- [ ] Các chỉ tiêu so sánh: Dư nợ? Lãi phải trả? Tỷ lệ trả nợ?
- [ ] Kỳ so sánh: tháng / quý / năm?
- [ ] Kế hoạch nhập 1 lần đầu năm hay cập nhật rolling?
- [ ] Ai phê duyệt số kế hoạch trước khi lưu?

---

**Checklist clarify khi có req Dashboard:**
- [ ] Metric / KPI cụ thể
- [ ] Filter nào (công ty / ngân hàng / loại vay / thời gian)
- [ ] Công thức tính nếu custom
- [ ] Drill-down level
- [ ] Nguồn data từ bảng Lark nào
- [ ] Người dùng cuối (Ban lãnh đạo / CFO / Kế toán)

---

## 🔄 BUSINESS WORKFLOW — Quy trình Khoản vay

> Các quy trình nghiệp vụ liên quan đến vòng đời khoản vay

| ID | Tên workflow | Mô tả | Actor | Áp dụng | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|---|
| BW-001 | Tạo mới khoản vay | Quy trình nhập Loan Master mới | Kế toán / CFO | 14 cty | — | — | — | — |
| BW-002 | Ghi nhận giao dịch | Nhập Loan Activity (trả gốc/lãi/rút vốn) | Kế toán | 14 cty | — | — | — | — |
| BW-003 | Cập nhật TSDB | Thêm / sửa tài sản đảm bảo | Kế toán | 14 cty | — | — | — | — |
| BW-004 | Alert đáo hạn | Cảnh báo khoản vay sắp đến hạn | Tự động → CFO | 14 cty | — | — | — | — |

**Checklist clarify khi có req Workflow:**
- [ ] Trigger (điều gì bắt đầu)
- [ ] Actor từng bước
- [ ] Điều kiện phê duyệt / từ chối
- [ ] Áp dụng tất cả 14 cty hay chỉ một số
- [ ] Exception case
- [ ] Notification: ai nhận, kênh nào (Lark / email)

---

## 🖼️ UI / UX & MOCKUP

> Approach: **Mockup-First** — confirm mockup trước, build sau

| ID | Tên | Liên quan tab | File/Link | Status | Người confirm | Ngày | Revision |
|---|---|---|---|---|---|---|---|
| MK-001 | Mockup v6 — Tổng quan Dư nợ | Tab 1 | TY_Treasury_v6.html | 🔄 Đang review | — | — | v6 |
| MK-002 | Mockup v6 — Lịch trả nợ | Tab 2 | TY_Treasury_v6.html | 🔄 Đang review | — | — | v6 |
| MK-003 | Mockup v6 — Thế chấp | Tab 4 | TY_Treasury_v6.html | 🔄 Đang review | — | — | v6 |
| MK-004 | Mockup v6 — Thanh khoản Basic | Tab 3 ⚠️ | TY_Treasury_v6.html | 🔄 Đang xem xét | — | — | v6 |
| MK-005 | Mockup v6 — So sánh KH/TT Basic | Tab 5 ⚠️ | TY_Treasury_v6.html | 🔄 Đang xem xét | — | — | v6 |

**Checklist confirm mockup:**
- [ ] KPI strip hiển thị đúng metric cần thiết
- [ ] Table columns đủ, không thừa
- [ ] Filter đáp ứng nhu cầu tra cứu
- [ ] Alert / badge trạng thái rõ ràng
- [ ] Layout phù hợp màn hình Ban lãnh đạo dùng

---

## 🚫 NGOÀI SCOPE — Phase này

| # | Hạng mục | Lý do | Ghi nhận ngày |
|---|---|---|---|
| 1 | Tab 3 full version — tính tự động từ raw data | Basic version đã deliver trong phase này | — |
| 2 | Tab 5 full version — automation + variance analysis | Basic version đã deliver trong phase này | — |
| 3 | Bảng Cash Balance raw data trên Lark | Phase sau — full version Tab 3 & 5 | — |
| 4 | Bảng 05 Tồn Quỹ | Thanh Yến chưa quyết định | — |
| 5 | Mobile app | Ngoài hợp đồng | — |
| 6 | Tích hợp hệ thống kế toán ngoài | Ngoài hợp đồng | — |

---

## 📝 CHANGE LOG

| Ngày | ID | Loại | Nội dung thay đổi | Người yêu cầu | Người confirm |
|---|---|---|---|---|---|
| 22/04/2026 | BI-T3, BI-T5 | Thêm mới | Tab 3 & 5 đưa vào scope — Basic version (nhập kết quả thủ công, không raw data) | Huyen-Cosy | Chờ confirm |
| — | — | Thêm / Sửa / Deprecated / Out of Phase | — | — | — |

---
*Cập nhật lần cuối: —*
