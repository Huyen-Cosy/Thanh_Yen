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
| Lark Base — Khoản vay | 7 | 3 | 0 | 0 | 4 |
| BI — Dashboard Khoản vay | 1 | 0 | 1 | 0 | 0 |
| Business Workflow | 4 | 2 | 2 | 0 | 0 |
| UI/UX Mockup | 0 | 0 | 0 | 0 | 0 |
| **Tổng** | **12** | **5** | **3** | **0** | **4** |

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

### Thay đổi cấu trúc Lark Base (Architecture changes)
| ID | Tên requirement | Thay đổi | Mô tả | Nguồn | Rõ ràng | Status | Ngày |
|---|---|---|---|---|---|---|---|
| LRK-DEL-001 | Xóa bảng Vốn góp nội bộ | Xóa bảng | Master data thay đổi rất ít, không cần bảng riêng; hiển thị trên dashboard từ nguồn khác | Meeting 22/04 | 🟢 Clear | ✅ Confirmed | 22/04/2026 |
| LRK-DEL-002 | Xóa bảng Tồn quỹ nhập tay | Xóa/thay thế | Thay bằng auto bank-sync tool hoặc Excel import; không nhập tay | Meeting 22/04 | 🟢 Clear | ✅ Confirmed | 22/04/2026 |
| LRK-DEL-003 | Xóa bảng Dự báo dòng tiền | Xóa/thay thế | Thay bằng Excel template + shared folder; auto-sync lên dashboard | Meeting 22/04 | 🟢 Clear | ✅ Confirmed | 22/04/2026 |
| LRK-FLOW-001 | Giải ngân → Lark Base Flow | Chuyển thành Flow | Workflow có các bước phê duyệt; cần clarify approval steps trong họp 23/04 | Meeting 22/04 | 🟡 Partial | ⬜ Chờ clarify | 22/04/2026 |
| LRK-FLOW-002 | Trả nợ & đóng khoản vay → Flow | Chuyển thành Flow | Workflow nhiều bước; cần clarify ai duyệt, điều kiện đóng khoản vay | Meeting 22/04 | 🟡 Partial | ⬜ Chờ clarify | 22/04/2026 |
| LRK-FLOW-003 | Khoản vay gốc → Lark Base Flow | Chuyển thành Flow | Form phức tạp, có đính kèm hình ảnh; biến thành Flow cho dễ nhập | Meeting 22/04 | 🟢 Clear | ⬜ Todo | 22/04/2026 |
| LRK-FLOW-004 | Tài sản thế chấp → Lark Base Flow | Chuyển thành Flow | Form có đính kèm hình ảnh/giấy tờ; biến thành Flow | Meeting 22/04 | 🟢 Clear | ⬜ Todo | 22/04/2026 |

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
| BI-NEW-004 | Thêm dữ liệu cân đối thu chi vào biến động dòng tiền | Chart | Bổ sung tiền vào/ra vận hành từ Excel cân đối thu chi; hiện chỉ có dòng trả gốc & lãi | Meeting 22/04 | 🟡 Partial | ⬜ Chờ template | 22/04/2026 |

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
| BW-001 | Tạo mới khoản vay | Quy trình nhập Loan Master mới | Kế toán / CFO | 14 cty | Meeting 22/04 | 🟢 Clear | ⬜ Todo (Flow) | 22/04/2026 |
| BW-002 | Ghi nhận giao dịch / Giải ngân | Workflow giải ngân có bước phê duyệt nhiều người | Kế toán / CFO | 14 cty | Meeting 22/04 | 🟡 Partial | ⬜ Chờ clarify 23/04 | 22/04/2026 |
| BW-003 | Trả nợ & đóng khoản vay | Workflow trả nợ, xác nhận và đóng khoản vay | Kế toán / CFO | 14 cty | Meeting 22/04 | 🟡 Partial | ⬜ Chờ clarify 23/04 | 22/04/2026 |
| BW-004 | Cập nhật Tài sản thế chấp | Quy trình thêm/sửa tài sản đảm bảo kèm giấy tờ | Kế toán | 14 cty | Meeting 22/04 | 🟢 Clear | ⬜ Todo (Flow) | 22/04/2026 |

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
| 22/04/2026 | LRK-DEL-001,002,003 | Xóa | Xóa 3 bảng: Vốn góp nội bộ, Tồn quỹ nhập tay, Dự báo dòng tiền khỏi Lark Base | Anh Trung | ✅ Confirmed |
| 22/04/2026 | LRK-FLOW-001,002,003,004 | Thêm mới | 4 bảng chuyển thành Lark Base Flow (Khoản vay gốc, Tài sản thế chấp, Giải ngân, Trả nợ) | Anh Trung | ⬜ Chờ clarify 23/04 |
| 22/04/2026 | BI-NEW-004 | Thêm mới | Thêm dữ liệu cân đối thu chi vào chart biến động dòng tiền | Chị Yến | ⬜ Chờ template |

---
*Cập nhật lần cuối: —*
