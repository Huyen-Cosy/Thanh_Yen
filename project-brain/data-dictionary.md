# Data Dictionary — Dự án Thanh Yến

> Nguồn tham chiếu duy nhất cho tất cả field trong hệ thống.  
> Dõng + Tài cập nhật khi có thay đổi trên Lark. Vân đọc trước khi build measure.

---

## BẢNG: Company

| Field | Lark Name | Type | Required | Mô tả |
|---|---|---|---|---|
| Mã công ty | company_id | Text | ✅ | Mã định danh duy nhất |
| Tên công ty | company_name | Text | ✅ | Tên đầy đủ |
| Tên viết tắt | company_short | Text | ✅ | Dùng trên dashboard |
| Nhóm | company_group | Dropdown | — | Phân nhóm kinh doanh |
| Trạng thái | status | Dropdown | ✅ | Active / Inactive |

---

## BẢNG: Loan Master

| Field | Lark Name | Type | Required | Mô tả |
|---|---|---|---|---|
| Mã khoản vay | loan_id | Text | ✅ | Auto-generate |
| Công ty | company_id | Relation → Company | ✅ | Công ty vay |
| Ngân hàng | bank_name | Dropdown | ✅ | Tên ngân hàng |
| Số hợp đồng | contract_no | Text | ✅ | Số HĐ tín dụng |
| Loại vay | loan_type | Dropdown | ✅ | Ngắn hạn / Dài hạn / Tuần hoàn |
| Hạn mức | credit_limit | Number (VND) | — | Hạn mức theo HĐ tín dụng |
| Mã HĐ tín dụng | parent_loan_id | Relation → Loan Master | — | ⚠️ CLR-001: pending |
| Ngày vay | loan_date | Date | ✅ | Ngày giải ngân đầu tiên |
| Ngày đáo hạn | due_date | Date | ✅ | Ngày phải trả hết |
| Lãi suất | interest_rate | Number (%) | ✅ | Theo năm p.a. — 365 ngày |
| Dư nợ | outstanding_balance | Number (VND) | Auto-calc | Từ Loan Activity |
| Trạng thái | loan_status | Dropdown | ✅ | Active / Closed / Overdue |

---

## BẢNG: Loan Activity

| Field | Lark Name | Type | Required | Mô tả |
|---|---|---|---|---|
| Mã giao dịch | activity_id | Text | ✅ | Auto-generate |
| Khoản vay | loan_id | Relation → Loan Master | ✅ | Thuộc KV nào |
| Ngày GD | transaction_date | Date | ✅ | Ngày thực hiện |
| Loại GD | transaction_type | Dropdown | ✅ | Rút vốn / Trả gốc / Trả lãi / Gia hạn |
| Số tiền gốc | principal_amount | Number (VND) | — | |
| Số tiền lãi | interest_amount | Number (VND) | — | |
| Người nhập | created_by | Text | ✅ | |
| Ghi chú | notes | Text | — | |

---

## BẢNG: Collateral Assets

| Field | Lark Name | Type | Required | Mô tả |
|---|---|---|---|---|
| Mã TSDB | asset_id | Text | ✅ | |
| Khoản vay | loan_id | Relation → Loan Master | ✅ | |
| Mô tả | asset_description | Text | ✅ | |
| Loại TS | asset_type | Dropdown | ✅ | BĐS / Xe / Máy móc / Khác |
| Chủ sở hữu | asset_owner | Relation → Company | ✅ | |
| Giá trị thẩm định | appraised_value | Number (VND) | ✅ | |
| Ngày thẩm định | appraisal_date | Date | ✅ | |
| Ngày thẩm định tiếp | next_appraisal | Date | — | |
| Tỷ lệ NH | bank_ltv_ratio | Number (%) | — | LTV ratio NH cho phép |
| Giá trị cho vay | lending_value | Number (VND) | Auto-calc | appraised_value × bank_ltv_ratio |
| Ngân hàng nhận TC | collateral_bank | Dropdown | ✅ | |
| Trạng thái | asset_status | Dropdown | ✅ | Active / Released / Expired |

---

## BUSINESS RULES ĐÃ CONFIRM

| # | Rule | Xác nhận bởi | Ngày |
|---|---|---|---|
| BR-001 | Lãi suất tính theo năm (p.a.), 365 ngày | Nhàn | — |
| BR-002 | Dư nợ = Tổng rút vốn - Tổng trả gốc | Nhàn | — |
| BR-003 | 1 HĐ tín dụng có thể có nhiều khoản vay con | Nhàn | — |
| BR-004 | TSDB có thể dùng cho nhiều khoản vay (bảo lãnh chéo) | Nhàn | — |

---

*Cập nhật lần cuối: 23/04/2026*
