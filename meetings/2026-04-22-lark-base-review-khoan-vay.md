# Meeting Minutes — 2026-04-22 Lark Base Review: Hệ Thống Quản Lý Khoản Vay

> Tạo bởi AI Agent từ transcript. Chờ xác nhận bởi: **Huyên** trước **2026-04-23**

---

## THÔNG TIN

| | |
|---|---|
| **Ngày** | 2026-04-22 |
| **Thành phần ideaLAB** | Người trình bày (em), Huyên |
| **Thành phần Thanh Yến** | Chị Yến, Chị Nhàn, Trang (Na Trang) |
| **Mục đích** | Walk-through toàn bộ các bảng (table) trên Lark Base — review cấu trúc, logic, dữ liệu hiện có và thống nhất các điểm còn chưa rõ |

---

## 📋 TÓM TẮT NỘI DUNG *(high-level)*

- **Master data**: Danh mục công ty (27 bản ghi), tài khoản ngân hàng (16 bản ghi) đã nhập khá đủ. Khoản vay gốc còn thiếu một số trường. Quyết định giữ toàn bộ khoản vay (NH/NB/CN) trong một bảng, dùng filter view để tách.
- **Tồn quỹ**: Phát sinh yêu cầu mới — chị Yến muốn nhập chi tiết thu chi hàng ngày (sổ 111/112) thay vì chỉ ghi số dư tổng. ideaLAB sẽ đánh giá khả năng import template; tạm thời chưa thay đổi cấu trúc.
- **Công nợ nội bộ (Bảng 8)**: Đổi tên từ "Khoản vay nội bộ", bổ sung trường mã hợp đồng, xác nhận mã tài khoản kế toán (131/138/331/338) và công thức nợ/có cuối kỳ.
- **Trả nợ (Bảng 9)**: Thống nhất công thức tính lãi và dư nợ. Trạng thái (status) sẽ chạy bằng công thức tự động thay vì nhập tay.
- **Dự báo dòng tiền**: Chị Yến muốn có vị thế thanh khoản và forecast cash flow. ideaLAB xác nhận đây là scope Phase 2 — sẽ trao đổi với anh Trung.
- **Automation**: Thống nhất 3 nhóm nhắc nhở tự động. Chị Yến sẽ gửi rule chi tiết lên group.
- **Data completeness**: Chị Yến xác nhận dữ liệu **chưa đủ** — mục tiêu hoàn thành trong 1–2 ngày tới.

---

## ✅ QUYẾT ĐỊNH ĐÃ CONFIRM

| # | Quyết định | Người confirm |
|---|---|---|
| 1 | **Mục đích khoản vay** phải ghi cụ thể: "Vay bổ sung vốn lưu động" / "Vay đầu tư tài sản cố định" — không ghi chung chung "vay ngắn hạn" / "mượn nội bộ" | Chị Yến |
| 2 | Toàn bộ khoản vay (NH/NB/CN) **ở chung một bảng** khoản vay gốc, dùng filter view để tách theo loại | Chị Yến |
| 3 | **Bảng 8** đổi tên thành "Công nợ nội bộ"; bổ sung trường **mã hợp đồng** bên cạnh mã khoản vay | Chị Yến |
| 4 | Mã tài khoản kế toán trong Bảng 8: Bán hàng **131**, Cho vay **138**, Mua hàng **331**, Vay **338** | Chị Yến |
| 5 | Công thức cuối kỳ Bảng 8: Nợ cuối kỳ = Nợ đầu kỳ + PS Nợ − PS Có (nếu > 0); Có cuối kỳ = \|(Nợ đầu kỳ + PS Nợ − PS Có)\| (nếu < 0) | Chị Yến |
| 6 | **Trạng thái Bảng 9** chạy bằng công thức tự động, không nhập tay. Logic: Số ngày quá hạn = Ngày trả dự kiến − Ngày hiện tại; dương → chưa đến hạn; âm → quá hạn; = 0 → đến hạn; dư nợ = 0 → tất toán | Chị Yến |
| 7 | Công thức tính lãi: **Dư nợ đầu kỳ × Lãi suất × Số ngày / 365** | Chị Yến |
| 8 | Tổng phải trả kỳ này = Số tiền gốc phải trả + Số tiền lãi phải trả | Chị Yến |
| 9 | Dư nợ cuối kỳ = Dư nợ đầu kỳ − Số tiền gốc đã trả thực tế | Chị Yến |
| 10 | Tất cả tính toán phức tạp (trạng thái, dư nợ đầu/cuối kỳ) **đẩy lên dashboard BI**, bảng Lark Base chỉ là nơi nhập liệu | Đồng thuận |
| 11 | **Dự báo dòng tiền / vị thế thanh khoản** → Phase 2, chưa làm trong giai đoạn này | ideaLAB (trao đổi lại với anh Trung) |
| 12 | Thanh Yến hoàn thành nhập liệu trong **1–2 ngày tới** để ideaLAB bê dữ liệu sang data warehouse | Chị Yến |

---

## 🔴 CONFLICT & ĐIỂM CHƯA THỐNG NHẤT *(chi tiết)*

### CONFLICT-001: Tồn Quỹ — Chi Tiết Thu Chi vs. Số Dư Tổng

| | |
|---|---|
| **Vấn đề** | Bảng Tồn quỹ hiện chỉ ghi số dư đầu ngày / cuối ngày (tổng). Chị Yến muốn nhập chi tiết từng khoản thu chi hàng ngày (như sổ 111/112) để kiểm soát dòng tiền và xác minh mục đích sử dụng vốn của các công ty con |
| **Quan điểm ideaLAB** | Bảng Tồn quỹ được thiết kế chỉ để tính KPI (tỷ lệ dư nợ/tồn quỹ), không phải sổ theo dõi tiền mặt. Nhập chi tiết sẽ double-work và không link được với dashboard hiện tại |
| **Quan điểm Thanh Yến** | Cần một nơi tập trung để xem chi tiết thu chi của tất cả công ty con thay vì nhận từng file Excel/email riêng lẻ |
| **Hướng giải quyết tạm thời** | ideaLAB xin template sổ 112 từ Thanh Yến → nghiên cứu hỗ trợ import file thay vì nhập tay từng dòng |
| **Tác động** | Nếu thêm chức năng này → scope mới, cần đánh giá effort và timeline |
| **Người quyết định** | Chị Yến + anh Trung (ideaLAB) |
| **Deadline** | Sau khi ideaLAB đánh giá — dự kiến phản hồi trước **25/04/2026** |
| **Status** | 🔴 Chưa giải quyết |

---

### CONFLICT-002: Dự Báo Dòng Tiền — Trong Scope Hiện Tại hay Phase 2?

| | |
|---|---|
| **Vấn đề** | Mockup dashboard có phần "Vị thế thanh khoản" và "Dòng tiền vào/ra" (ghi chú "minh họa"). Chị Yến muốn có forecast cash flow đầy đủ ngay trong phase này |
| **Quan điểm ideaLAB** | Forecast cash flow đòi hỏi dữ liệu từ 3 hoạt động (kinh doanh, đầu tư, tài chính) + balance sheet + báo cáo KQKD → phạm vi rất lớn, cần Phase 2 riêng |
| **Quan điểm Thanh Yến** | Trong mockup có phần này; cần để kiểm soát thanh khoản tập đoàn |
| **Tác động** | Nếu đưa vào Phase 1 → delay toàn bộ go-live |
| **Người quyết định** | Anh Trung + Chị Yến |
| **Deadline** | Cần xác nhận trước **25/04/2026** |
| **Status** | 🔴 Chưa giải quyết |

---

## ⚡ ACTION ITEMS *(chi tiết)*

### ACTION-001: Chị Yến Gửi Template Báo Cáo Tồn Quỹ / Sổ Thu Chi

| | |
|---|---|
| **Mô tả** | Gửi cho ideaLAB file mẫu (Excel hoặc format hiện tại) mà các công ty con đang dùng để báo cáo thu chi hàng ngày (sổ 111/112) |
| **Vị trí** | File Excel / báo cáo hiện tại của các công ty con |
| **Kết quả kỳ vọng** | ideaLAB đánh giá được cấu trúc dữ liệu và xác định hỗ trợ import được không |
| **Owner** | Chị Yến (Thanh Yến) |
| **Deadline** | 23/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | CONFLICT-001 |

---

### ACTION-002: Chị Yến/Trang Gửi Rule Automation Lên Group

| | |
|---|---|
| **Mô tả** | Gửi chi tiết các rule nhắc nhở tự động lên group chat: (1) Gửi đến ai, (2) Ngày/giờ gửi, (3) Nội dung thông báo |
| **Vị trí** | Group chat dự án |
| **Thay đổi cụ thể** | Đã thống nhất 3 rule: báo cáo tồn quỹ (9:00 T2–T7 hàng ngày), nhắc trả nợ ngân hàng/lãi (ngày 5 và ngày 25 hàng tháng), nhắc báo cáo công nợ nội bộ (cuối tháng) |
| **Kết quả kỳ vọng** | ideaLAB setup được automation notifications chính xác |
| **Owner** | Chị Yến / Trang (Thanh Yến) |
| **Deadline** | 23/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Automation |

---

### ACTION-003: ideaLAB Tạo Filter Views Cho Bảng Khoản Vay Gốc

| | |
|---|---|
| **Mô tả** | Tạo 2 view riêng trên bảng Khoản vay gốc: View 1 chỉ hiện khoản vay Ngân hàng (NH), View 2 chỉ hiện khoản vay Nội bộ (NB) |
| **Vị trí** | Lark Base → Bảng Khoản vay gốc |
| **Thay đổi cụ thể** | Thêm filter theo cột "Loại khoản vay" = NH / NB / CN |
| **Kết quả kỳ vọng** | Chị Yến nhìn được từng nhóm khoản vay riêng biệt mà không cần tách 2 bảng master |
| **Owner** | ideaLAB |
| **Deadline** | 25/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Khoản vay gốc |

---

### ACTION-004: ideaLAB Cập Nhật Bảng 8 — Công Nợ Nội Bộ

| | |
|---|---|
| **Mô tả** | (1) Đổi tên bảng từ "Khoản vay nội bộ" → "Công nợ nội bộ"; (2) Cập nhật mã tài khoản: 131/138/331/338; (3) Thêm trường "Mã hợp đồng"; (4) Implement công thức nợ/có cuối kỳ |
| **Vị trí** | Lark Base → Bảng 8 |
| **Thay đổi cụ thể** | Xem Quyết định #3, #4, #5 ở trên |
| **Kết quả kỳ vọng** | Bảng theo dõi được toàn bộ giao dịch nội bộ (mua bán, vay mượn) với công thức tự động |
| **Owner** | ideaLAB |
| **Deadline** | 25/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Công nợ nội bộ |

---

### ACTION-005: ideaLAB Implement Công Thức Tự Động Bảng 9 — Trả Nợ

| | |
|---|---|
| **Mô tả** | Implement 4 công thức trong Bảng Trả nợ: (1) Số tiền lãi phải trả, (2) Tổng phải trả kỳ này, (3) Dư nợ cuối kỳ, (4) Trạng thái tự động theo số ngày quá hạn |
| **Vị trí** | Lark Base → Bảng 9 (Trả nợ) |
| **Thay đổi cụ thể** | Xem Quyết định #6, #7, #8, #9 ở trên |
| **Kết quả kỳ vọng** | Người nhập chỉ cần điền số tiền thực tế đã trả; hệ thống tự tính lãi, trạng thái, dư nợ còn lại |
| **Owner** | ideaLAB |
| **Deadline** | 25/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Bảng Trả nợ |

---

### ACTION-006: ideaLAB Trao Đổi Với Anh Trung Về Scope Dự Báo Dòng Tiền

| | |
|---|---|
| **Mô tả** | Huyên trao đổi với anh Trung để xác nhận: phần "Dòng tiền vào/ra" và "Vị thế thanh khoản" (hiện ghi "minh họa" trên mockup) có được đưa vào Phase 1 không, hay để Phase 2 |
| **Vị trí** | Mockup dashboard — khu vực Vị thế thanh khoản |
| **Kết quả kỳ vọng** | Thông báo lại cho chị Yến quyết định cuối cùng |
| **Owner** | Huyên (ideaLAB) |
| **Deadline** | 24/04/2026 |
| **Priority** | P1 🟡 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | CONFLICT-002 |

---

### ACTION-007: Thanh Yến Hoàn Thành Nhập Liệu Toàn Bộ

| | |
|---|---|
| **Mô tả** | Hoàn thành nhập đủ dữ liệu vào tất cả các bảng master (danh mục công ty, tài khoản ngân hàng, khoản vay gốc, tài sản thế chấp) và các bảng giao dịch |
| **Vị trí** | Toàn bộ Lark Base |
| **Kết quả kỳ vọng** | ideaLAB có đủ dữ liệu thật để migrate sang data warehouse và build dashboard |
| **Owner** | Chị Yến + team kế toán (Thanh Yến) |
| **Deadline** | 24/04/2026 |
| **Priority** | P0 🔴 |
| **Status** | ⬜ Todo |
| **Liên quan REQ** | Go-live milestone |

---

## 📝 TODO — CẦN LÀM RÕ TRƯỚC MEETING SAU *(chi tiết)*

### TODO-001: Template Sổ Thu Chi Hàng Ngày (Sổ 111/112)

| | |
|---|---|
| **Câu hỏi cụ thể** | File Excel / format mà các công ty con đang dùng để báo cáo thu chi hàng ngày có cấu trúc như thế nào? Có cột nào, bao nhiêu dòng/ngày? Hiện đang gửi qua email hay Zalo? |
| **Người trả lời** | Chị Yến (Thanh Yến) |
| **Cần để làm gì** | Nếu không có → không thể đánh giá khả năng import; CONFLICT-001 tiếp tục blocked |
| **Deadline trả lời** | 23/04/2026 |
| **Status** | ⬜ Chờ trả lời |

---

### TODO-002: Rule Chi Tiết Automation Notifications

| | |
|---|---|
| **Câu hỏi cụ thể** | (1) Báo cáo tồn quỹ 9:00 sáng T2–T7: gửi đến những ai (tên/chức danh)? Nội dung thông báo cụ thể là gì? (2) Nhắc trả nợ ngân 5 & 25: gửi đến ai? (3) Nhắc công nợ nội bộ cuối tháng: ngày mấy chính xác? Gửi đến ai? |
| **Người trả lời** | Chị Yến / Trang (Thanh Yến) |
| **Cần để làm gì** | Nếu không có → ideaLAB không setup được automation đúng người đúng nội dung |
| **Deadline trả lời** | 23/04/2026 |
| **Status** | ⬜ Chờ trả lời |

---

### TODO-003: Xác Nhận Scope Dự Báo Dòng Tiền Với Anh Trung

| | |
|---|---|
| **Câu hỏi cụ thể** | Phần "Dòng tiền vào/ra" và "Vị thế thanh khoản" trên mockup — anh Trung xác nhận đây là Phase 1 hay Phase 2? Nếu Phase 1 thì cần bổ sung bảng dữ liệu nào? |
| **Người trả lời** | Anh Trung (ideaLAB) |
| **Cần để làm gì** | Nếu không rõ → chị Yến không biết kỳ vọng go-live có bao gồm forecast cash flow không; CONFLICT-002 tiếp tục blocked |
| **Deadline trả lời** | 24/04/2026 |
| **Status** | ⬜ Chờ trả lời |

---

## 🔄 REQUIREMENT PHÁT SINH *(cần confirm trước khi vào scope_register)*

### 📊 Lark Base
| REQ | Bảng | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| LRK-NEW-001 | Tồn quỹ | Hỗ trợ import chi tiết thu chi hàng ngày (sổ 111/112) từ file Excel của từng công ty con | 🟡 Partial | ⬜ Chờ template từ Thanh Yến |
| LRK-NEW-002 | Khoản vay gốc | Thêm 2 filter view: View NH (ngân hàng) và View NB (nội bộ) | 🟢 Clear | ⬜ Chờ confirm anh Trung |

### 📈 BI / Dashboard
| REQ | Tab | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| BI-NEW-003 | Vị thế thanh khoản | Bổ sung dòng tiền vào/ra và forecast cash flow (hiện đang là "minh họa" trên mockup) | 🔴 Unclear | ⬜ Chờ anh Trung xác nhận scope |

### 🔄 Workflow / UI / Mockup
| REQ | Loại | Thay đổi cụ thể | Rõ ràng | Confirm? |
|---|---|---|---|---|
| — | — | Không phát sinh requirement mới về workflow trong buổi này | — | — |

---

## 📅 MEETING SAU

| | |
|---|---|
| **Ngày dự kiến** | Sau khi Thanh Yến hoàn thành nhập liệu (~24–25/04/2026) |
| **Mục đích** | Xác nhận data đã đủ; ideaLAB demo dashboard sau khi migrate dữ liệu; chốt scope dự báo dòng tiền |
| **Cần chuẩn bị** | Thanh Yến: hoàn thành nhập liệu + gửi template sổ thu chi + gửi rule automation; ideaLAB: cập nhật Bảng 8 & 9, trao đổi với anh Trung |
| **Conflict cần giải quyết** | CONFLICT-001 (tồn quỹ chi tiết), CONFLICT-002 (dự báo dòng tiền) |
| **TODO cần có kết quả** | TODO-001 (template sổ thu chi), TODO-002 (automation rules), TODO-003 (scope dự báo) |

---

*Tạo bởi AI Agent — 2026-04-22 | Chưa được xác nhận*
