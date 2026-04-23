# BR Register — Business Requirements
# Dự án Thanh Yến | Ngôn ngữ: Business (Anh Trung confirm)

> Mỗi BR phải được Anh Trung hoặc đại diện Thanh Yến confirm trước khi team implement.  
> Không chỉnh sửa thủ công — qua AI Agent sau khi confirm.

---

## TỔNG QUAN

| | P0 | P1 | P2 |
|---|---|---|---|
| ✅ Confirmed | 0 | 0 | 0 |
| 🔄 In Progress | 0 | 0 | 0 |
| ⏳ Pending Confirm | 0 | 0 | 0 |
| 🔴 Unclear | 0 | 0 | 0 |

---

## DANH SÁCH BR

| BR ID | Tên | Mô tả (ngôn ngữ business) | Priority | Phase | Status | Confirmed by | Ngày | FR liên quan |
|---|---|---|---|---|---|---|---|---|
| BR-001 | Xem tổng dư nợ | Xem được tổng dư nợ của từng công ty và toàn tập đoàn tại bất kỳ thời điểm nào | P0 | Current | ⏳ Pending | — | — | FR-D-001, FR-L-001 |
| BR-002 | Theo dõi lịch trả nợ | Biết được khoản vay nào đến hạn, cần trả bao nhiêu gốc và lãi | P0 | Current | ⏳ Pending | — | — | FR-D-002, FR-L-002 |
| BR-003 | Kiểm tra tài sản đảm bảo | Biết được TSDB nào đang thế chấp cho khoản vay nào, giá trị còn bao nhiêu | P0 | Current | ⏳ Pending | — | — | FR-D-004, FR-L-003 |
| BR-004 | Xem vị thế thanh khoản | Nắm được tình hình tiền mặt/khả năng thanh toán của từng công ty | P1 | Basic | ⏳ Pending | — | — | FR-D-003 |
| BR-005 | So sánh kế hoạch vs thực hiện | Đối chiếu số liệu tài chính thực tế với kế hoạch đã đặt ra | P1 | Basic | ⏳ Pending | — | — | FR-D-005 |

---

## CHI TIẾT BR

### BR-001: Xem tổng dư nợ
**Mô tả đầy đủ:** Ban lãnh đạo cần nhìn thấy bức tranh tổng thể về tình hình vay nợ — công ty nào đang vay bao nhiêu, từ ngân hàng nào, lãi suất ra sao.

**Acceptance criteria:**
- [ ] Xem được tổng dư nợ toàn tập đoàn
- [ ] Xem được dư nợ theo từng công ty
- [ ] Xem được dư nợ theo từng ngân hàng
- [ ] Xem được lãi suất bình quân

**CLR liên quan:** —  
**Confirmed by:** —

---

### BR-002: Theo dõi lịch trả nợ
**Mô tả đầy đủ:** Cần biết trước khoản vay nào sắp đến hạn, cần chuẩn bị tiền trả gốc và lãi bao nhiêu, để chủ động kế hoạch dòng tiền.

**Acceptance criteria:**
- [ ] Xem được danh sách khoản vay theo thứ tự đáo hạn
- [ ] Biết số tiền gốc + lãi cần trả trong tháng hiện tại
- [ ] Cảnh báo khoản vay sắp đến hạn (≤ 30 ngày)

**CLR liên quan:** —  
**Confirmed by:** —

---

### BR-003: Kiểm tra tài sản đảm bảo
**Mô tả đầy đủ:** Cần biết tổng tài sản đang thế chấp, tài sản nào đang dùng cho khoản vay nào, giá trị còn lại có đủ đảm bảo không.

**Acceptance criteria:**
- [ ] Xem được danh sách TSDB và trạng thái
- [ ] Biết tỷ lệ dư nợ / giá trị TSDB
- [ ] Cảnh báo TSDB sắp hết hạn thẩm định

**CLR liên quan:** CLR-001 (parent_loan_id)  
**Confirmed by:** —

---

*Cập nhật lần cuối: 23/04/2026*
