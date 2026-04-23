# Meeting Minutes — 2026-04-22 Lark Base: Thống Nhất Kiến Trúc Hệ Thống

> Tạo bởi AI Agent từ transcript. Chờ xác nhận bởi: **Huyên** trước **2026-04-23**

---

## THÔNG TIN

| | |
|---|---|
| **Ngày** | 2026-04-22 |
| **Thành phần ideaLAB** | Anh Trung (technical lead), Huyên, Vân |
| **Thành phần Thanh Yến** | Chị Yến |
| **Mục đích** | Anh Trung align lại kiến trúc tổng thể của Lark Base — phân định rõ cái gì dùng Lark Base, cái gì dùng Excel, cái gì là Flow — trước khi team tiếp tục build |

---

## 📋 TÓM TẮT NỘI DUNG *(high-level)*

- **Kiến trúc cốt lõi được làm rõ**: Lark Base = nơi nhập liệu & chạy quy trình (flow). Dashboard = nơi hiển thị & tính toán. Hai thứ này tách biệt hoàn toàn.
- **Tồn quỹ & Dự báo dòng tiền bị loại khỏi Lark Base**: Dữ liệu tần suất cao / phức tạp → dùng auto-sync hoặc Excel template, không nhập tay vào Lark Base.
- **Giải ngân & Trả nợ chuyển thành Flow**: Các nghiệp vụ cần nhiều bước phê duyệt sẽ được thiết kế thành workflow thay vì form nhập liệu đơn thuần.
- **Vốn góp nội bộ bị loại**: Tần suất thay đổi quá thấp, không cần bảng riêng trong Lark Base.
- **Công nợ nội bộ → Phase 2**: Chưa xây trong phase hiện tại.
- **Focus hiện tại**: Build hoàn chỉnh cho một công ty pilot trước, sau đó mới mở rộng lên holding.

---

## ✅ QUYẾT ĐỊNH ĐÃ CONFIRM

| # | Quyết định | Người confirm |
|---|---|---|
| 1 | **Tồn quỹ KHÔNG nhập tay vào Lark Base** → dùng auto bank-sync tool; nếu chưa có tool thì dùng Excel import | Anh Trung + Chị Yến |
| 2 | **Vốn góp nội bộ: XÓA khỏi Lark Base** — master data thay đổi rất ít, không cần bảng riêng; dữ liệu hiển thị trên dashboard | Anh Trung |
| 3 | **Dự báo dòng tiền / Cân đối thu chi KHÔNG dùng Lark Base** → dùng Excel template + shared folder; auto-sync lên dashboard | Anh Trung + Chị Yến |
| 4 | **Giải ngân → Flow** (workflow có bước phê duyệt nhiều người) | Anh Trung |
| 5 | **Trả nợ & Đóng khoản vay → Flow** | Anh Trung |
| 6 | **Khoản vay gốc & Tài sản thế chấp → Flow** (form phức tạp, có đính kèm hình ảnh) | Anh Trung |
| 7 | **Master data đơn giản** (Danh mục công ty, Tài khoản ngân hàng) → giữ dạng form thông thường | Anh Trung |
| 8 | **Công nợ nội bộ → Phase 2**, chưa build trong phase này | Anh Trung |
| 9 | **Phase hiện tại chỉ build cho một công ty pilot** — chưa build dashboard tổng holding | Anh Trung |
| 10 | Họp tiếp theo **chiều 23/04** (~1–2 tiếng) để clarify chi tiết approval flow của Giải ngân và các quy trình khác | Anh Trung + Chị Yến |

<img width="563" height="843" alt="image" src="https://github.com/user-attachments/assets/d59169d2-9b01-4219-8162-66fbcb79fed8" />

---

## 🔴 CONFLICT & ĐIỂM CHƯA THỐNG NHẤT

| # | Vấn đề | Quan điểm ideaLAB | Quan điểm Thanh Yến | Người quyết định | Deadline | Status |
|---|---|---|---|---|---|---|
| C-001 | Cân đối thu chi cần tập trung ở đâu — Lark Base không phù hợp cho dữ liệu phức tạp này | Dùng Excel template + shared folder → auto-sync dashboard; Phase 2 mới automate toàn bộ | Đồng ý dùng Excel, nhưng cần rõ: công ty con gửi vào folder nào, theo template nào, bao giờ | Anh Trung + Huyên (ideaLAB) | 23/04 | 🟡 Đang giải quyết |

---

## ⚡ ACTION ITEMS

| # | Mô tả | Kết quả kỳ vọng | Owner | Deadline | Priority | Status |
|---|---|---|---|---|---|---|
| A-001 | Xóa/ẩn bảng Tồn quỹ khỏi Lark Base; nghiên cứu auto bank-sync tool hoặc thiết kế luồng import Excel | Số dư tồn quỹ cập nhật tự động lên dashboard, không nhập tay hàng ngày | Anh Trung / Vân | 25/04 | P0 🔴 | ⬜ Todo |
| A-002 | Xóa bảng Vốn góp nội bộ khỏi Lark Base | Lark Base gọn hơn; dữ liệu vốn góp vẫn hiển thị trên dashboard từ nguồn khác | ideaLAB | 24/04 | P1 🟡 | ⬜ Todo |
| A-003 | Thiết kế lại 4 bảng thành Lark Base Flow: (1) Khoản vay gốc, (2) Tài sản thế chấp, (3) Giải ngân, (4) Trả nợ & đóng khoản vay — xác định initiator, bước phê duyệt, auto-fill | Flow dẫn dắt từng bước; người dùng không phải tự điền form trắng | Anh Trung (thiết kế) + ideaLAB (build) | Sau họp 23/04 | P0 🔴 | ⬜ Chờ họp |
| A-004 | Thiết kế Excel template chuẩn cho báo cáo cân đối thu chi; set up shared folder để công ty con upload; hệ thống tự sync lên dashboard | Chị Yến xem tổng hợp thu chi trên dashboard, không nhận từng file qua email | Vân + Huyên | 28/04 | P1 🟡 | ⬜ Todo |
| A-005 | Confirm lịch họp chiều 23/04 (~1–2 tiếng) với chị Yến để clarify approval flow | Lịch gửi lên group trước tối 22/04 | Huyên | 22/04 | P0 🔴 | ⬜ Todo |

---

## 📝 TODO — CẦN LÀM RÕ TRONG HỌP 23/04

| # | Câu hỏi cụ thể | Hỏi ai | Cần để làm gì | Deadline | Status |
|---|---|---|---|---|---|
| T-001 | Quy trình giải ngân gồm mấy bước? Ai tạo yêu cầu? Ai duyệt từng bước? Điều kiện chuyển bước? Cần chữ ký số/giấy tờ không? | Chị Yến | ideaLAB thiết kế Flow giải ngân trong Lark Base | Họp 23/04 | ⬜ Chờ họp |
| T-002 | Khi trả nợ: ai xác nhận đã trả? Ai duyệt đóng khoản vay? Cần upload chứng từ không? | Chị Yến | ideaLAB thiết kế Flow trả nợ | Họp 23/04 | ⬜ Chờ họp |
| T-003 | Template cân đối thu chi có cấu trúc cố định không? Các công ty con đang dùng cùng một template không? Tần suất gửi là hàng ngày hay hàng tháng? | Chị Yến / Huyên (đã có file mẫu trong Zoom chat) | Thiết kế shared folder + data pipeline lên dashboard | 23/04 | ⬜ Chờ xác nhận |

---

## 🔄 REQUIREMENT PHÁT SINH

### 📈 BI / Dashboard
| REQ | Tab | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| BI-NEW-004 | Vị thế thanh khoản / Biến động dòng tiền | Bổ sung dữ liệu từ Excel cân đối thu chi (tiền vào/ra vận hành) vào chart biến động dòng tiền — hiện chỉ có dòng trả gốc & lãi | 🟡 Partial | ⬜ Chờ template |

### 🔄 Workflow / Lark Base Flow
| REQ | Loại | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| LRK-FLOW-001 | Flow | Giải ngân khoản vay → thiết kế thành Lark Base Flow với các bước phê duyệt | 🟡 Partial | ⬜ Chờ clarify 23/04 |
| LRK-FLOW-002 | Flow | Trả nợ & đóng khoản vay → Lark Base Flow | 🟡 Partial | ⬜ Chờ clarify 23/04 |
| LRK-FLOW-003 | Flow | Khoản vay gốc → Lark Base Flow (thay vì form đơn) | 🟢 Clear | ⬜ Chờ build |
| LRK-FLOW-004 | Flow | Tài sản thế chấp → Lark Base Flow (có đính kèm hình ảnh) | 🟢 Clear | ⬜ Chờ build |
| LRK-DEL-001 | Xóa | Xóa bảng Vốn góp nội bộ khỏi Lark Base | 🟢 Clear | ✅ Confirmed |
| LRK-DEL-002 | Xóa/Thay thế | Xóa bảng Tồn quỹ nhập tay; thay bằng auto-sync hoặc Excel import | 🟢 Clear | ✅ Confirmed |
| LRK-DEL-003 | Xóa/Thay thế | Xóa bảng Dự báo dòng tiền khỏi Lark Base; thay bằng Excel template + shared folder | 🟢 Clear | ✅ Confirmed |

---

## 📅 MEETING SAU

| | |
|---|---|
| **Ngày dự kiến** | Chiều 23/04/2026 (~1–2 tiếng) |
| **Mục đích** | Clarify chi tiết approval flow cho Giải ngân, Trả nợ, Khoản vay gốc; thống nhất template cân đối thu chi |
| **Cần chuẩn bị** | ideaLAB: draft sơ bộ các flow steps để discuss; Thanh Yến: mô tả quy trình hiện tại (ai làm gì, bao nhiêu bước) |
| **TODO cần có kết quả** | TODO-001, TODO-002, TODO-003 |

---

*Tạo bởi AI Agent — 2026-04-22 | Chưa được xác nhận*
