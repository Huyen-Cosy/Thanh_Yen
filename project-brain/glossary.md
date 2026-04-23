# Glossary — Thuật ngữ Dự án Thanh Yến

> File này là nguồn tham chiếu duy nhất cho tất cả thuật ngữ.  
> Khi có từ mới → thêm vào đây trước khi dùng ở bất kỳ file nào khác.

---

## THUẬT NGỮ NGHIỆP VỤ

| Thuật ngữ | Viết tắt | Định nghĩa | Ghi chú |
|---|---|---|---|
| Dư nợ | — | Số tiền gốc còn lại chưa trả của một khoản vay tại một thời điểm | ≠ tổng giá trị khoản vay |
| Kế hoạch | KH | Số liệu được lập từ đầu kỳ (năm/quý/tháng) | Nhập thủ công |
| Thực hiện | TH | Số liệu thực tế phát sinh | Từ Loan Activity |
| Tài sản đảm bảo | TSDB | Tài sản thế chấp để đảm bảo cho khoản vay | Có thể là BĐS, xe, máy móc... |
| Hạn mức tín dụng | HMTD | Hạn mức vay tối đa được ngân hàng cấp theo hợp đồng tín dụng | 1 HĐ tín dụng có thể có nhiều khoản vay |
| Đáo hạn | — | Ngày khoản vay phải trả hết | |
| Lãi suất | — | Tỷ lệ % tính trên dư nợ, theo năm (p.a.) | Xác nhận bởi Nhàn: tính theo 365 ngày |
| Gốc | — | Phần tiền vay gốc, không bao gồm lãi | |
| Lãi | — | Phần tiền lãi phát sinh trên dư nợ | |
| Bảo lãnh chéo | — | Công ty A dùng tài sản đảm bảo cho khoản vay của Công ty B | Phổ biến trong tập đoàn |
| Nợ nội bộ | — | Khoản vay/cho vay giữa các công ty trong tập đoàn | |
| Tồn quỹ | — | Số dư tiền mặt/tài khoản ngân hàng tại một thời điểm | Bảng 05 — chưa trong scope |

---

## THUẬT NGỮ HỆ THỐNG

| Thuật ngữ | Định nghĩa | Nơi tồn tại |
|---|---|---|
| Loan Master | Bảng lưu thông tin hợp đồng vay (master record) | Lark Base |
| Loan Activity | Bảng lưu các giao dịch phát sinh: rút vốn, trả gốc, trả lãi | Lark Base |
| Collateral Assets | Bảng lưu tài sản đảm bảo | Lark Base |
| Company | Bảng lưu thông tin 14 công ty thành viên | Lark Base |
| Cash Balance | Bảng lưu số dư tài khoản (phase sau) | Lark Base |
| Data Warehouse | Kho dữ liệu trung gian giữa Lark và Power BI | TBD |
| Dashboard | Báo cáo trực quan trên Power BI | Power BI |

---

## THUẬT NGỮ QUẢN LÝ DỰ ÁN

| Thuật ngữ | Định nghĩa |
|---|---|
| BR | Business Requirement — nhu cầu nghiệp vụ, ngôn ngữ của anh Trung |
| FR | Functional Requirement — yêu cầu kỹ thuật cụ thể, ngôn ngữ của team |
| CLR | Clarification — câu hỏi cần làm rõ, đang chờ trả lời |
| CHG | Change — thay đổi requirement đã được confirm |
| Scope Creep | Yêu cầu mới ngoài phạm vi hợp đồng ban đầu |
| Mockup-First | Approach: tạo mockup confirm trước, build data sau |
| Basic version | Tab 3 & 5: nhập kết quả tính toán thủ công, không raw data |

---

*Cập nhật lần cuối: 23/04/2026*
