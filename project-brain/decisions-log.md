# Decisions Log — Dự án Thanh Yến

> Ghi lại tất cả quyết định quan trọng + lý do.
> Không chỉnh sửa thủ công — qua AI Agent.

---

## DANH SÁCH QUYẾT ĐỊNH

| DEC ID | Ngày | Chủ đề | Quyết định | Người confirm | Meeting ref |
|---|---|---|---|---|---|
| DEC-001 | 22/04/2026 | Kiến trúc | Lark Base = nhập liệu & flow. Dashboard = hiển thị & tính toán. Tách biệt hoàn toàn. | Anh Trung + Chị Yến | 2026-04-22-lark-base-architecture-alignment |
| DEC-002 | 22/04/2026 | Scope | Tồn quỹ KHÔNG nhập tay vào Lark Base → auto bank-sync hoặc Excel import | Anh Trung + Chị Yến | 2026-04-22-lark-base-architecture-alignment |
| DEC-003 | 22/04/2026 | Scope | Vốn góp nội bộ: xóa khỏi Lark Base | Anh Trung | 2026-04-22-lark-base-architecture-alignment |
| DEC-004 | 22/04/2026 | Scope | Dự báo dòng tiền / Cân đối thu chi: dùng Excel template + shared folder, không dùng Lark Base | Anh Trung + Chị Yến | 2026-04-22-lark-base-architecture-alignment |
| DEC-005 | 22/04/2026 | Scope | Công nợ nội bộ → Phase 2, chưa build | Anh Trung | 2026-04-22-lark-base-architecture-alignment |
| DEC-006 | 22/04/2026 | Approach | 4 bảng chính (Khoản vay, TSDB, Giải ngân, Trả nợ) → thiết kế dạng Flow (workflow nhiều bước phê duyệt) | Anh Trung | 2026-04-22-lark-base-architecture-alignment |
| DEC-007 | 22/04/2026 | Rollout | Phase hiện tại build cho **1 công ty pilot** trước, sau đó mở rộng lên holding | Anh Trung + Chị Yến | 2026-04-22-lark-base-architecture-alignment |
| DEC-008 | 24/04/2026 | Workflow | Cả 4 flow có **3 bước phê duyệt**: Staff → Reviewer (Trưởng BP/KT trưởng, open) → Approver (CEO/CFO) | Chị Yến + Chị Loan | 2026-04-24-client-workflow-mockup |
| DEC-009 | 24/04/2026 | Workflow | Reviewer là **Open**: Staff tự chọn người kiểm soát tùy cơ cấu đơn vị | Chị Yến | 2026-04-24-client-workflow-mockup |
| DEC-010 | 24/04/2026 | Workflow | Giải ngân: sau duyệt nội bộ có thêm bước Staff **cập nhật trạng thái thực tế** (kèm Bank Statement) trước khi vào Master Data | Chị Yến | 2026-04-24-client-workflow-mockup |
| DEC-011 | 24/04/2026 | Automation | Giải ngân: hệ thống **auto-notify** Approver khi status = "Đã giải ngân" — không phê duyệt lại | Chị Yến + ideaLAB | 2026-04-24-client-workflow-mockup |
| DEC-012 | 24/04/2026 | Pilot | Pilot mapping: **Lý** (Staff) → **Open** (Reviewer) → **Chị Loan / GĐ tài chính** (Approver) | Chị Loan + Chị Yến | 2026-04-24-client-workflow-mockup |

---

*Cập nhật lần cuối: 03/05/2026 — AI Agent*
