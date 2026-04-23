# Thanh Yến Treasury — Project Repo

> **ideaLAB** | Kickoff: 30/03/2026  
> Hệ thống quản trị khoản vay cho 14 công ty thành viên Tập đoàn Thanh Yến

---

## 🚀 Nếu bạn vừa join — đọc phần này trước

Gõ vào Claude Code:
```
Tôi là [tên], role [role], vừa join dự án Thanh Yến
```
Agent sẽ tóm tắt tất cả những gì bạn cần biết theo đúng role của bạn.

---

## 🗺️ Cấu trúc repo

| Thư mục | Mô tả | Ai dùng |
|---|---|---|
| `project-brain/` | Kiến thức nền: glossary, data-dictionary, architecture | Tất cả |
| `docs/requirements/` | BR (business) + FR (technical) + CLR (câu hỏi chờ) | PM, BA, Team |
| `docs/design/` | Mockup specs, UX decisions | Hiếu → Vân |
| `docs/data-model/` | Lark schema, transformation rules | Tài, Dõng |
| `docs/dashboard-specs/` | Measure, filter, drill-down per tab | Vân |
| `docs/guides/` | Hướng dẫn sử dụng | Nhàn, 14 cty |
| `meetings/` | Meeting minutes | Tất cả |
| `tracker/` | Task tracker, change log | Huyên, team |
| `assets/` | File index + mockup HTML + templates | Tất cả |

---

## 👥 Team

| Tên | Role | Phụ trách |
|---|---|---|
| Huyên | PM | Toàn bộ dự án, merge PR |
| Vân | DA | Dashboard Power BI |
| Hiếu | Mockup Designer | UI/UX, mockup |
| Tài | Data Engineering | Data model, schema |
| Dõng | Lark Admin | Setup Lark Base |
| Anh Trung | Product Owner (ideaLAB) | Confirm BR |
| Nhàn | Finance Assistant (ideaLAB) | Clarify finance logic |
| Chị Yến | Business lead (Thanh Yến) | Confirm BR |
---

## ⚡ Slash Commands hay dùng

```
/clarify [nội dung]     → Phân tích ambiguity, tạo câu hỏi làm rõ
/breakdown [BR-ID]      → Breakdown BR thành FR + Tasks
/impact [change]        → Phân tích impact trước khi thay đổi
/handoff [role] [topic] → Tạo spec handoff cho role khác
/report                 → Báo cáo tiến độ tổng quan
/pending                → Xem câu hỏi đang chờ trả lời
/blocked                → Xem items đang bị blocked
/onboard                → Tóm tắt dự án cho member mới
```

---

## 📌 Phase hiện tại: Loan Management

| | Trong scope | Ngoài scope (phase sau) |
|---|---|---|
| Dashboard | Tab 1, 2, 4 (full) + Tab 3, 5 (basic) | Tab 3, 5 full version |
| Lark Base | Loan Master, Loan Activity, Collateral Assets | Cash Balance |
| Mockup | v6 — đang confirm | — |

---

*Repo được maintain bởi Huyên (PM) | ideaLAB*
