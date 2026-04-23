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

---

## 🔴 CONFLICT & ĐIỂM CHƯA THỐNG NHẤT

### CONFLICT-001: Dự Báo Dòng Tiền — Cần Tập Trung Dữ Liệu Ở Đâu?

| | |
|---|---|
| **Vấn đề** | Chị Yến cần một nơi tập trung để xem dự báo dòng tiền / cân đối thu chi của tất cả công ty con (hiện đang nhận qua email/Zalo riêng lẻ). Lark Base không phù hợp để chứa dữ liệu phức tạp này |
| **Quan điểm ideaLAB** | Dùng Excel template chuẩn + shared folder → tự động đẩy lên dashboard. Phase 2 mới automate toàn bộ |
| **Quan điểm Thanh Yến** | Đồng ý dùng Excel, nhưng cần rõ quy trình: các công ty con gửi vào folder nào, theo template nào, bao giờ |
| **Tác động** | Nếu không có quy trình rõ → tiếp tục nhận báo cáo rải rác, không tập trung được |
| **Người quyết định** | Anh Trung + Huyên (ideaLAB) — thiết kế template & folder |
| **Deadline** | Clarify trong buổi họp 23/04 |
| **Status** | 🟡 Đang giải quyết |

---

## ⚡ ACTION ITEMS

### ACTION-001: ideaLAB Redesign Tồn Quỹ — Bỏ Nhập Tay Lark Base

| | |
|---|---|
| **Mô tả** | Xóa/ẩn bảng Tồn quỹ khỏi Lark Base. Nghiên cứu auto bank-sync tool; nếu chưa có thì thiết kế luồng import Excel |
| **Kết quả kỳ vọng** | Số dư tồn quỹ cập nhật tự động lên dashboard, không cần nhập tay hàng ngày |
| **Owner** | Anh Trung / Vân (ideaLAB) |
| **Deadline** | 25/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |

---

### ACTION-002: ideaLAB Xóa Bảng Vốn Góp Nội Bộ

| | |
|---|---|
| **Mô tả** | Remove bảng Vốn góp nội bộ khỏi Lark Base. Đảm bảo dữ liệu vốn góp vẫn hiển thị được trên dashboard từ nguồn khác |
| **Kết quả kỳ vọng** | Lark Base gọn hơn, không có bảng thừa |
| **Owner** | ideaLAB |
| **Deadline** | 24/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |

---

### ACTION-003: ideaLAB Convert Giải Ngân + Trả Nợ + Khoản Vay Gốc + Tài Sản Thế Chấp → Flow

| | |
|---|---|
| **Mô tả** | Thiết kế lại 4 bảng thành Lark Base Flow (workflow): (1) Khoản vay gốc, (2) Tài sản thế chấp, (3) Hoạt động giải ngân, (4) Trả nợ & đóng khoản vay |
| **Thay đổi cụ thể** | Mỗi flow cần xác định: người khởi tạo (initiator), các bước phê duyệt, người duyệt, điều kiện auto-fill |
| **Kết quả kỳ vọng** | Người dùng không phải tự điền form trắng — flow dẫn dắt từng bước, auto-fill những gì có thể |
| **Owner** | Anh Trung (thiết kế) + ideaLAB team (build) |
| **Deadline** | Clarify approval logic trong họp 23/04; build sau đó |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Chờ họp 23/04 để clarify |

---

### ACTION-004: ideaLAB Tạo Excel Template + Shared Folder Cho Cân Đối Thu Chi

| | |
|---|---|
| **Mô tả** | Thiết kế Excel template chuẩn cho báo cáo cân đối thu chi hàng tháng. Set up shared folder để các công ty con upload vào; hệ thống tự sync lên dashboard |
| **Kết quả kỳ vọng** | Chị Yến xem được cân đối thu chi tổng hợp trên dashboard mà không cần nhận từng file Excel qua email |
| **Owner** | Vân + Huyên (ideaLAB) |
| **Deadline** | 28/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |

---

### ACTION-005: Huyên Confirm Lịch Họp Chiều 23/04

| | |
|---|---|
| **Mô tả** | Check lịch nội bộ và confirm với chị Yến lịch họp chiều 23/04 (~1–2 tiếng) để clarify approval flow chi tiết cho các quy trình Giải ngân, Trả nợ |
| **Kết quả kỳ vọng** | Lịch họp được gửi lên group trước tối 22/04 |
| **Owner** | Huyên (ideaLAB) |
| **Deadline** | 22/04/2026 (hôm nay) |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |

---

## 📝 TODO — CẦN LÀM RÕ TRONG HỌP 23/04

### TODO-001: Approval Flow Chi Tiết Cho Giải Ngân

| | |
|---|---|
| **Câu hỏi cụ thể** | Quy trình giải ngân một khoản vay gồm mấy bước? Ai là người tạo yêu cầu? Ai duyệt bước 1, bước 2? Điều kiện để chuyển bước là gì? Có bước nào cần chữ ký số/giấy tờ không? |
| **Người trả lời** | Chị Yến (Thanh Yến) |
| **Cần để làm gì** | ideaLAB thiết kế Flow trong Lark Base |
| **Deadline trả lời** | Trong buổi họp 23/04 |
| **Status** | ⬜ Chờ họp |

---

### TODO-002: Approval Flow Chi Tiết Cho Trả Nợ & Đóng Khoản Vay

| | |
|---|---|
| **Câu hỏi cụ thể** | Khi trả nợ một khoản: ai xác nhận đã trả? Ai duyệt đóng khoản vay? Có cần upload chứng từ không? |
| **Người trả lời** | Chị Yến (Thanh Yến) |
| **Cần để làm gì** | ideaLAB thiết kế Flow trả nợ |
| **Deadline trả lời** | Trong buổi họp 23/04 |
| **Status** | ⬜ Chờ họp |

---

### TODO-003: Template & Folder Cân Đối Thu Chi

| | |
|---|---|
| **Câu hỏi cụ thể** | Template cân đối thu chi hiện tại của Thanh Yến có cấu trúc cố định không? Các công ty con có đang dùng cùng một template không? Tần suất gửi là hàng ngày hay hàng tháng? |
| **Người trả lời** | Chị Yến / Huyên (đã có file mẫu trong Zoom chat) |
| **Cần để làm gì** | Thiết kế shared folder + data pipeline lên dashboard |
| **Deadline trả lời** | 23/04/2026 |
| **Status** | ⬜ Chờ xác nhận |

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
