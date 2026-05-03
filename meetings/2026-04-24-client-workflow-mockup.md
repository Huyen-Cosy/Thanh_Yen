# Meeting Minutes — 2026-04-24: Workflow Discussion (with Mockup)

> ⏳ Chờ xác nhận bởi: Huyên

---

## THÔNG TIN

| | |
|---|---|
| **Ngày** | 2026-04-24 |
| **Loại** | Client Meeting |
| **Thành phần** | ideaLAB (Huyên + team) · Thanh Yến (Chị Yến, Chị Loan) |
| **Mục đích** | Review mockup approval flow 4 quy trình; thống nhất cấu trúc phê duyệt và phân quyền pilot |
| **Recording** | 24/4/2026 - Weekly & Workflow discussion (with mockup).mp4 |

---

## 📋 TÓM TẮT NỘI DUNG

- 4 quy trình (Tạo khoản vay, TSDB, Giải ngân, Trả nợ) cần bổ sung thêm bước **Kiểm soát** trước khi lên Lãnh đạo → approval thành **3 bước**
- Quy trình Giải ngân cần thêm bước **cập nhật trạng thái thực tế** sau khi được duyệt (kèm bank statement)
- Xác nhận mapping nhân sự cho **công ty pilot**
- Chị Yến + kế toán cần **review lại mockup forms** để confirm đủ field

---

## ✅ QUYẾT ĐỊNH ĐÃ CONFIRM

| # | Quyết định | Người confirm |
|---|---|---|
| 1 | **3-bước phê duyệt** cho cả 4 flow: Staff → Reviewer (Trưởng BP/Kế toán trưởng) → Approver (CEO/CFO) | Chị Yến + ideaLAB |
| 2 | **Reviewer là Open** — Staff tự chọn người kiểm soát tùy cơ cấu từng đơn vị | Chị Yến |
| 3 | **Pilot company mapping**: Lý (Staff) → Open (Reviewer) → Chị Loan hoặc GĐ tài chính (Approver) | Chị Loan + Chị Yến |
| 4 | Giải ngân: sau khi duyệt nội bộ, Staff **cập nhật trạng thái thực tế** (kèm Bank Statement) trước khi đổ vào Master Data | Chị Yến |
| 5 | Giải ngân: **Auto-notification** cho Approver khi Staff update "Đã giải ngân" — không cần phê duyệt lại lần 2 | Chị Yến + ideaLAB |

---

## 🔴 ĐIỂM CHƯA THỐNG NHẤT / CẦN THEO DÕI

| # | Vấn đề | Cần làm rõ | Owner | Status |
|---|---|---|---|---|
| C-002 | Field đầy đủ trong từng form chưa được confirm | Chị Yến + kế toán review mockup từng form | Chị Yến / Nhàn | ⬜ Chờ review |
| C-003 | Auto-integration form phê duyệt → Master Data chưa verify | Kiểm tra không có lệch dữ liệu giữa nội dung đã duyệt và dữ liệu quản trị | Tài + Dõng | ⬜ Chờ test |

---

## ⚡ ACTION ITEMS

| # | Mô tả | Owner | Deadline | Status |
|---|---|---|---|---|
| A-006 | Cập nhật mockup 4 flow → thêm bước Reviewer (bước 2 mới) | Hiếu | TBD | ⬜ Todo |
| A-007 | Cập nhật mockup Giải ngân → thêm bước cập nhật trạng thái thực tế + attach Bank Statement | Hiếu | TBD | ⬜ Todo |
| A-008 | Thiết kế auto-notification trigger khi Giải ngân = "Đã giải ngân" | Dõng | TBD | ⬜ Todo |
| A-009 | Chị Yến + kế toán review mockup forms — confirm field đầy đủ | Chị Yến / Nhàn | TBD | ⬜ Chờ Thanh Yến |
| A-010 | Setup approval routing Lark cho pilot: Lý → Open → Chị Loan | Dõng | TBD | ⬜ Todo |

---

## 🔄 REQUIREMENT PHÁT SINH

### 🔄 Workflow / Lark Base Flow

| REQ | Loại | Nội dung | Rõ ràng | Confirm? |
|---|---|---|---|---|
| LRK-FLOW-005 | Flow update | Bổ sung bước Reviewer (bước 2) vào cả 4 quy trình | 🟢 Clear | ✅ Confirmed |
| LRK-FLOW-006 | Flow update | Giải ngân: thêm bước cập nhật trạng thái thực tế + đính kèm Bank Statement | 🟢 Clear | ✅ Confirmed |
| LRK-FLOW-007 | Automation | Auto-notification cho Approver khi status Giải ngân = "Đã giải ngân" | 🟢 Clear | ✅ Confirmed |

---

> ⚠️ **Lưu ý:** Section "1.4 Tóm tắt cấu trúc phê duyệt đã thống nhất" (dạng bảng/diagram trong Lark Docs) không extract được — cần Huyên bổ sung thủ công nếu có chi tiết quan trọng hơn phần đã capture ở trên.

---

*Tạo bởi AI Agent — 2026-05-03 | Chờ xác nhận*
