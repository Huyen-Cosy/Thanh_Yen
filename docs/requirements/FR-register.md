# FR Register — Functional Requirements
# Dự án Thanh Yến | Ngôn ngữ: Technical (team implement)

> Mỗi FR phải link về 1 BR cha. Không có BR cha → không được implement.  
> Không chỉnh sửa thủ công — qua AI Agent sau khi confirm.

---

## PREFIX

| Prefix | Loại | Owner |
|---|---|---|
| FR-L-XXX | Lark Base setup | Dõng |
| FR-D-XXX | Dashboard Power BI | Vân |
| FR-M-XXX | Mockup | Hiếu |
| FR-DM-XXX | Data model / transformation | Tài |
| FR-WF-XXX | Business workflow / automation | Dõng + Tài |

---

## FLAT TABLE — TẤT CẢ FR

| FR ID | BR | Loại | Tên | Mô tả chi tiết | Owner | Priority | Phase | Status | CLR | Ngày |
|---|---|---|---|---|---|---|---|---|---|---|
| FR-L-001 | BR-001 | Lark | Tạo bảng Loan Master | Tạo bảng với đầy đủ field theo data-dictionary | Dõng | P0 | Current | 🔄 In Progress | — | — |
| FR-L-002 | BR-001 | Lark | Tạo bảng Loan Activity | Tạo bảng giao dịch, link relation với Loan Master | Dõng | P0 | Current | 🔄 In Progress | — | — |
| FR-L-003 | BR-003 | Lark | Tạo bảng Collateral Assets | Tạo bảng TSDB, link với Loan Master và Company | Dõng | P0 | Current | 🔄 In Progress | — | — |
| FR-L-004 | BR-001 | Lark | Field parent_loan_id | Link nhiều khoản vay về 1 HĐ tín dụng | Dõng | P1 | Current | 🔴 Blocked | CLR-001 | — |
| FR-DM-001 | BR-001 | Data Model | Schema Loan Master | Thiết kế field, type, relation, index | Tài | P0 | Current | ✅ Done | — | — |
| FR-DM-002 | BR-001 | Data Model | Transformation rule dư nợ | Công thức: Dư nợ = Tổng rút - Tổng trả gốc | Tài | P0 | Current | ✅ Done | — | — |
| FR-M-001 | BR-001 | Mockup | Mockup Tab 1 — Dư nợ | HTML mockup v6, đã confirm | Hiếu | P0 | Current | ✅ Done | — | — |
| FR-M-002 | BR-002 | Mockup | Mockup Tab 2 — Lịch trả nợ | HTML mockup v6, đã confirm | Hiếu | P0 | Current | ✅ Done | — | — |
| FR-M-003 | BR-003 | Mockup | Mockup Tab 4 — Thế chấp | HTML mockup v6, đã confirm | Hiếu | P0 | Current | ✅ Done | — | — |
| FR-M-004 | BR-004 | Mockup | Mockup Tab 3 — Thanh khoản Basic | HTML mockup v6, đang xem xét | Hiếu | P1 | Basic | 🔄 Review | — | — |
| FR-M-005 | BR-005 | Mockup | Mockup Tab 5 — KH/TT Basic | HTML mockup v6, đang xem xét | Hiếu | P1 | Basic | 🔄 Review | — | — |
| FR-D-001 | BR-001 | Dashboard | Tab 1 — KPI & Table Dư nợ | KPI strip + bảng chi tiết khoản vay | Vân | P0 | Current | ⬜ Todo | — | — |
| FR-D-002 | BR-002 | Dashboard | Tab 2 — Lịch trả nợ | Bảng lịch trả nợ sort theo đáo hạn | Vân | P0 | Current | ⬜ Todo | — | — |
| FR-D-004 | BR-003 | Dashboard | Tab 4 — Thế chấp | Bảng TSDB + chuỗi bảo lãnh chéo | Vân | P0 | Current | ⬜ Todo | — | — |
| FR-D-003 | BR-004 | Dashboard | Tab 3 — Thanh khoản Basic | Hiển thị KPI nhập thủ công | Vân | P1 | Basic | ⬜ Todo | CLR-002 | — |
| FR-D-005 | BR-005 | Dashboard | Tab 5 — KH/TT Basic | Bảng so sánh KH vs TH, tính chênh lệch | Vân | P1 | Basic | ⬜ Todo | CLR-003 | — |
| FR-WF-001 | BR-002 | Workflow | Alert đáo hạn | Cảnh báo khoản vay ≤ 30 ngày đến hạn | Dõng | P1 | Current | ⬜ Todo | — | — |
| FR-WF-002 | BR-001, BR-002, BR-003 | Workflow | 3-bước phê duyệt cho 4 flow | Bổ sung bước Reviewer (Trưởng BP/KT trưởng, open) vào giữa Staff và Approver trong cả 4 quy trình | Dõng | P0 | Current | ⬜ Todo | — | 24/04/2026 |
| FR-WF-003 | BR-001 | Workflow | Cập nhật trạng thái giải ngân thực tế | Sau khi duyệt nội bộ, Staff cập nhật trạng thái + đính kèm Bank Statement trước khi đổ vào Master Data | Dõng | P0 | Current | ⬜ Todo | — | 24/04/2026 |
| FR-WF-004 | BR-001 | Workflow | Auto-notification giải ngân | Hệ thống tự gửi thông báo cho Approver khi Staff update status = "Đã giải ngân" — không cần phê duyệt lại | Dõng | P1 | Current | ⬜ Todo | — | 24/04/2026 |

---

*Cập nhật lần cuối: 03/05/2026*
