# Meeting Minutes — 2026-04-22 Weekly Progress Update: Menu Engineering & PNL

> Tạo bởi AI Agent từ transcript. Chờ xác nhận bởi: **Huyên** trước **2026-04-23**

---

## THÔNG TIN

| | |
|---|---|
| **Ngày** | 2026-04-22 |
| **Thành phần ideaLAB** | Team lead (chị), Hạnh, Vân, Huyên |
| **Thành phần Thanh Yến** | Mẫn (FA/kế toán), Dương (FA/kế toán) |
| **Mục đích** | Cập nhật tiến độ tuần Menu Engineering & PNL Dashboard |

---

## 📋 TÓM TẮT NỘI DUNG *(high-level)*

> Phần này chỉ ghi ngắn gọn — chi tiết xem các section bên dưới

- **Menu Engineering**: Phần Ala Carte đã hoàn thành theo comment; Buffet đã thêm cost nguyên vật liệu và auto-refresh T-mix/AOV Mix. Phần chi phí thực tế vs. định mức đang bị pending do logic phức tạp và cần làm rõ hệ số quy đổi.
- **PNL Dashboard**: Data model đã build xong, đang viết metrics trên Power BI. Phát hiện dữ liệu từ Fast API khớp với Fast UI, nhưng file Excel từ FA có chênh lệch — cần làm rõ với kế toán.
- **Conflict về ưu tiên**: Chị Hà muốn pending PNL để tập trung Menu Engineering; ideaLAB muốn chạy song song vì PNL gần xong và team có đủ người — cần chị Hà xác nhận lại.

---

## ✅ QUYẾT ĐỊNH ĐÃ CONFIRM

| # | Quyết định | Người confirm |
|---|---|---|
| 1 | Phần visual PNL và chỉnh data ở database sẽ chạy **song song** (không block nhau) | Team lead ideaLAB |
| 2 | Huyên sẽ bẻ nhỏ các đầu việc Menu Engineering thành sub-task 1–2 ngày và cập nhật lên task board **ngay hôm nay** | Huyên |
| 3 | Họp với Dương + FA vào **thứ Ba 28/04** để review logic tính cost và giải thích ý nghĩa từng bảng/cột | Team lead ideaLAB |
| 4 | ideaLAB sẽ nhắn chị Hà để xác nhận lại việc **tiếp tục PNL song song** với Menu Engineering | Team lead ideaLAB |
| 5 | Khi bảng cost xong thì Mẫn/Dương sẽ **so khớp số liệu** với báo cáo kế toán hiện tại | Mẫn + Dương |

---

## 🔴 CONFLICT & ĐIỂM CHƯA THỐNG NHẤT *(chi tiết)*

### CONFLICT-001: PNL — Pending vs. Chạy Song Song

| | |
|---|---|
| **Vấn đề** | Chị Hà đã thông báo pending PNL để hoàn thiện Menu Engineering trước. ideaLAB không đồng ý vì PNL gần xong và khác team làm |
| **Quan điểm ideaLAB** | PNL đã có data model, đã kéo được dữ liệu từ Fast, chỉ còn phần bottom-line. Có người riêng làm PNL, không ảnh hưởng đến Menu Engineering. Pending PNL kéo dài toàn dự án |
| **Quan điểm Thanh Yến (chị Hà)** | Muốn xong Menu Engineering trước rồi mới làm PNL. Timeline PNL gửi cho chị Hà đang bị "dài" |
| **Tác động** | Customer dashboard cũng đang pending → nguy cơ nhiều dashboard bị đóng băng cùng lúc |
| **Người quyết định** | Chị Hà |
| **Deadline** | Cần xác nhận trước **23/04/2026** để team ideaLAB biết phân bổ nguồn lực |
| **Status** | 🔴 Chưa giải quyết |

---

### CONFLICT-002: Hệ Số Quy Đổi Buffet — Nhiều Nguồn Mâu Thuẫn

| | |
|---|---|
| **Vấn đề** | Hệ số quy đổi buffet trẻ em trong buổi họp user requirement là 0.33, nhưng một file mới tìm thấy có nhiều hệ số quy đổi khác nhau. Combo cũng có hệ số 2.5. |
| **Quan điểm ideaLAB** | Chưa chắc chắn dùng hệ số nào là đúng — cần kế toán xác nhận trước khi code logic |
| **Quan điểm Thanh Yến** | Chưa có phản hồi chính thức |
| **Tác động** | Block việc hoàn thiện bảng tính cost thực tế/định mức cho Buffet |
| **Người quyết định** | Kế toán / FA |
| **Deadline** | Cần xác nhận trước **thứ Ba 28/04** để họp review logic |
| **Status** | 🔴 Chưa giải quyết |

---

### CONFLICT-003: File Excel FA Chênh Lệch Với Fast UI

| | |
|---|---|
| **Vấn đề** | File Excel do chị Hà gửi (dùng làm nguồn đầu vào PNL) có số liệu khác so với Fast API/Fast UI. Cụ thể: cùng một metric (ví dụ: tính lương trong PNL by store) nhưng cách tính khác nhau giữa các tháng |
| **Quan điểm ideaLAB** | Dữ liệu từ Fast API đã khớp Fast UI → Fast là nguồn đúng. File Excel của FA đang có inconsistency trong logic tính |
| **Quan điểm Thanh Yến** | Chưa có phản hồi — cần list chi tiết các điểm sai |
| **Tác động** | Block việc xác nhận metric PNL; không biết dùng nguồn số liệu nào |
| **Người quyết định** | FA / kế toán (chị Hà hoặc người gửi file Excel) |
| **Deadline** | Cần phản hồi trước **25/04/2026** |
| **Status** | 🔴 Chưa giải quyết |

---

## ⚡ ACTION ITEMS *(chi tiết)*

### ACTION-001: Bẻ Nhỏ Task Menu Engineering Thành Sub-task 1–2 Ngày

| | |
|---|---|
| **Mô tả** | Chia nhỏ các đầu việc còn lại trong Menu Engineering (đặc biệt phần cost thực tế/định mức) thành sub-task cụ thể, mỗi task có timeline 1–2 ngày |
| **Vị trí** | Task board / công cụ quản lý dự án hiện tại |
| **Thay đổi cụ thể** | Thêm sub-task kèm deadline cụ thể thay vì để một task lớn đến 24/04 |
| **Kết quả kỳ vọng** | Team Thanh Yến có thể theo dõi từng đầu việc và biết sớm khi bị chậm |
| **Owner** | Huyên (ideaLAB) |
| **Deadline** | 22/04/2026 (hôm nay) |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Menu Engineering |

---

### ACTION-002: Tổ Chức Họp Thứ Ba 28/04 — Review Logic Cost + Giải Thích Bảng/Cột

| | |
|---|---|
| **Mô tả** | Tổ chức buổi họp với Dương + FA để ideaLAB trình bày: (1) luồng logic tính cost thực tế/định mức, (2) ý nghĩa từng bảng và cột trong database |
| **Vị trí** | Nhóm FA trên Zalo/Teams |
| **Thay đổi cụ thể** | Gửi lịch họp thứ Ba 28/04 lên nhóm FA |
| **Kết quả kỳ vọng** | Dương hiểu cấu trúc dữ liệu, bắt đầu check số song song với ideaLAB |
| **Owner** | Huyên (ideaLAB) — tổ chức lịch |
| **Deadline** | Gửi lịch trước 23/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Menu Engineering — Cost thực tế/định mức |

---

### ACTION-003: Vân List Các Metric Bất Đồng Nhất Trong File Excel FA

| | |
|---|---|
| **Mô tả** | Liệt kê cụ thể các metric có cách tính khác nhau giữa các tháng trong file Excel FA, sau đó nhắn lên nhóm kế toán để làm rõ |
| **Vị trí** | File Excel chị Hà gửi; so sánh với Fast UI / database |
| **Thay đổi cụ thể** | Tạo danh sách: tên metric, tháng A tính thế nào, tháng B tính thế nào, chênh lệch bao nhiêu |
| **Kết quả kỳ vọng** | Kế toán xác nhận cách tính đúng để ideaLAB replicate vào dashboard PNL |
| **Owner** | Vân (ideaLAB) |
| **Deadline** | 23/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | PNL Dashboard |

---

### ACTION-004: ideaLAB Nhắn Chị Hà Xác Nhận Lại Việc Tiếp Tục PNL Song Song

| | |
|---|---|
| **Mô tả** | Team lead ideaLAB nhắn chị Hà trình bày lý do tiếp tục PNL song song: PNL gần xong, khác người làm, pending làm chậm cả dự án |
| **Vị trí** | Nhóm chat với chị Hà |
| **Thay đổi cụ thể** | Xác nhận: PNL tiếp tục trong tuần tới và dự kiến xong cuối tuần 25/04 |
| **Kết quả kỳ vọng** | Chị Hà đồng ý → team PNL tiếp tục, không bị block |
| **Owner** | Team lead ideaLAB |
| **Deadline** | 22/04/2026 (hôm nay) |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | PNL Dashboard |

---

### ACTION-005: Vân Tham Gia Họp FA Để Làm Rõ Cách Tính TIC File

| | |
|---|---|
| **Mô tả** | Vân join buổi họp giữa ideaLAB và FA (kế toán) để hỏi trực tiếp cách tính từ TIC file ra số cuối cùng đưa vào PNL |
| **Vị trí** | TIC files từ chị Hằng (2025 đến nay) |
| **Thay đổi cụ thể** | Xác nhận công thức/logic tính từng cột TIC → số PNL |
| **Kết quả kỳ vọng** | Vân nắm được logic, tự replicate được vào Power BI |
| **Owner** | Vân (ideaLAB) + FA |
| **Deadline** | Buổi họp thứ Ba 28/04 hoặc trước đó nếu có buổi FA riêng |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | PNL Dashboard |

---

## 📝 TODO — CẦN LÀM RÕ TRƯỚC MEETING SAU *(chi tiết)*

### TODO-001: Xác Nhận Hệ Số Quy Đổi Buffet Chính Thức

| | |
|---|---|
| **Câu hỏi cụ thể** | Hệ số quy đổi chính thức cho: (1) Buffet trẻ em là 0.33 hay số khác? (2) Combo là 2.5 hay số khác? (3) Có bảng mapping đầy đủ tất cả hệ số quy đổi theo từng loại không? |
| **Người trả lời** | Kế toán / FA (qua chị Mẫn hoặc trực tiếp trong buổi họp 28/04) |
| **Cần để làm gì** | Nếu không có → block toàn bộ việc tính cost buffet thực tế/định mức trong Menu Engineering |
| **Deadline trả lời** | 28/04/2026 (trước buổi họp) |
| **Status** | ⬜ Chờ trả lời |

---

### TODO-002: Logic Tính TIC File Để Ra Số PNL

| | |
|---|---|
| **Câu hỏi cụ thể** | Từ file TIC (chị Hằng gửi, 2025 đến nay): công thức tính từng cột như thế nào để ra được con số cuối cùng bỏ vào PNL? Có template hoặc tài liệu hướng dẫn không? |
| **Người trả lời** | Chị Hằng hoặc FA |
| **Cần để làm gì** | Nếu không có → Vân không thể replicate logic TIC vào Power BI → block metric PNL |
| **Deadline trả lời** | 28/04/2026 |
| **Status** | ⬜ Chờ trả lời |

---

### TODO-003: Xác Nhận File Excel FA — Metric Nào Dùng Logic Nào Là Đúng

| | |
|---|---|
| **Câu hỏi cụ thể** | Trong file Excel FA: tại sao cùng một metric (ví dụ: lương trong PNL by store) lại có cách tính khác nhau giữa tháng này và tháng trước? Cách tính nào là chuẩn? |
| **Người trả lời** | Kế toán FA (người tạo file Excel) |
| **Cần để làm gì** | Nếu không rõ → không biết replicate logic nào vào dashboard PNL → số liệu sai |
| **Deadline trả lời** | 25/04/2026 |
| **Status** | ⬜ Chờ trả lời |

---

## 🔄 REQUIREMENT PHÁT SINH *(cần confirm trước khi vào scope_register)*

### 📊 Lark Base
| REQ | Bảng | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| — | — | Không phát sinh requirement mới cho Lark Base trong buổi này | — | — |

### 📈 BI / Dashboard
| REQ | Tab | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| BI-NEW-001 | Menu Engineering — Buffet | Thêm bảng so sánh chi phí thực tế vs. chi phí định mức theo tuần/tháng (phát sinh từ buổi review dashboard ~2 tuần trước, không có trong plan gốc) | 🟡 Partial | ⬜ Chờ confirm chị Hà |
| BI-NEW-002 | Menu Engineering — Ala Carte | Thêm cột/bảng cost thực tế và định mức cho AC card theo tuần và tháng | 🟡 Partial | ⬜ Chờ confirm chị Hà |

### 🔄 Workflow / UI / Mockup
| REQ | Loại | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| MK-NEW-001 | Mockup | Có thành viên trong buổi video review đề xuất yêu cầu mới cho dashboard — chưa rõ nội dung cụ thể, cần chị Hà xác nhận có đưa vào scope không | 🔴 Unclear | ⬜ Chờ chị Hà |

---

## 📅 MEETING SAU

| | |
|---|---|
| **Ngày dự kiến** | Thứ Ba, 28/04/2026 |
| **Mục đích** | Review logic tính cost thực tế/định mức; giải thích ý nghĩa từng bảng/cột database với Dương; làm rõ TIC file |
| **Cần chuẩn bị** | ideaLAB: slide/doc giải thích luồng tính toán và cấu trúc bảng; FA/Kế toán: xác nhận hệ số quy đổi buffet và logic TIC file |
| **Conflict cần giải quyết** | CONFLICT-002 (hệ số quy đổi), CONFLICT-003 (Excel FA vs. Fast) |
| **TODO cần có kết quả** | TODO-001 (hệ số quy đổi), TODO-002 (TIC file logic), TODO-003 (Excel FA inconsistency) |

---

*Tạo bởi AI Agent — 2026-04-22 | Chưa được xác nhận*
