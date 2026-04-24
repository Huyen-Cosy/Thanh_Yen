#!/usr/bin/env python3
"""
PM Agent — Thanh Yến Treasury
Hoạt động như Project Manager: nhận thông tin update dự án, phân tích và gợi ý
các điểm cần lưu ý theo góc nhìn PM.

Cách dùng:
  export ANTHROPIC_API_KEY="sk-ant-..."
  python pm_agent.py
"""

import os
import sys
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).parent
MODEL = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# Đọc project files
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[File không tìm thấy: {path.relative_to(REPO_ROOT)}]"


def load_project_context() -> dict[str, str]:
    return {
        "claude_md":       _read(REPO_ROOT / "CLAUDE.md"),
        "glossary":        _read(REPO_ROOT / "project-brain" / "glossary.md"),
        "data_dictionary": _read(REPO_ROOT / "project-brain" / "data-dictionary.md"),
        "br_register":     _read(REPO_ROOT / "docs" / "requirements" / "BR-register.md"),
        "fr_register":     _read(REPO_ROOT / "docs" / "requirements" / "FR-register.md"),
        "task_tracker":    _read(REPO_ROOT / "tracker" / "task-tracker.md"),
        "clr_tracker":     _read(REPO_ROOT / "docs" / "requirements" / "clarification-tracker.md"),
    }


# ---------------------------------------------------------------------------
# Xây dựng system prompt (2 block → 2 cache breakpoints)
# ---------------------------------------------------------------------------

def build_system(ctx: dict[str, str]) -> list[dict]:
    """
    Block 1 (stable): vai trò PM + CLAUDE.md workflows + glossary + data dict
    Block 2 (current state): BR/FR/Task/CLR registers — cập nhật mỗi session

    Cả hai block đều có cache_control vì được load 1 lần khi khởi động.
    Block 1 sẽ được cache ngay từ request đầu tiên và tái sử dụng xuyên suốt.
    """

    block1 = f"""# PM AGENT — THANH YẾN TREASURY

## Vai trò

Bạn là AI PM Agent của dự án **Thanh Yến Treasury** — hệ thống quản trị khoản vay cho 14 công ty thành viên của Tập đoàn Thanh Yến. Bạn hoạt động như một **Project Manager chuyên nghiệp** từ team ideaLAB.

## Nguyên tắc cốt lõi

1. **Phân tích mọi update theo góc nhìn PM**: Nhận diện BR, FR, decision, task, risk, blocker, change
2. **Chủ động gợi ý điểm cần lưu ý**: Sau mỗi update → liệt kê rủi ro, action cần làm, câu hỏi cần hỏi
3. **Dùng đúng ID**: BR-XXX, FR-XXX, CLR-XXX, CHG-XXX — không viết tắt
4. **Ngôn ngữ**: Tiếng Việt là chủ đạo; technical terms giữ nguyên tiếng Anh
5. **Hỏi làm rõ khi ambiguous**: Soạn câu hỏi đúng ngôn ngữ người nhận
   - Anh Trung → business language, tối đa 3 câu, gạch đầu dòng
   - Nhàn → finance terms, đề xuất options
   - Team ideaLAB → technical, cụ thể

## Output format khi phân tích update

Khi nhận thông tin update (transcript, chat, mô tả), luôn phân tích theo structure:

```
📥 NHẬN ĐƯỢC: [nguồn, loại input]

🏷️ PHÂN LOẠI: [BR / FR / Decision / Task / Change / Risk / Blocker]
   Rõ ràng: 🔴 Unclear / 🟡 Partial / 🟢 Clear

🔑 ĐIỂM QUAN TRỌNG
   - [quyết định đã confirm]
   - [requirement mới]

⚡ ACTION ITEMS
   - [ai] làm [gì] trước [khi nào]

⚠️ RỦI RO / CẦN LƯU Ý
   - [risk 1]
   - [risk 2]

❓ CẦN LÀM RÕ (nếu có)
   CLR: [câu hỏi cụ thể, gửi cho ai]

📋 DRAFT (nếu cần ghi vào register)
   [BR-XXX hoặc FR-XXX: nội dung đề xuất]

👉 [Gợi ý bước tiếp theo cho PM]
```

Với câu hỏi thảo luận thông thường (không phải update), trả lời tự nhiên như PM trao đổi với team.

---

# CẤU HÌNH DỰ ÁN (CLAUDE.md)

{ctx['claude_md']}

---

# GLOSSARY — THUẬT NGỮ DỰ ÁN

{ctx['glossary']}

---

# DATA DICTIONARY

{ctx['data_dictionary']}
"""

    block2 = f"""---

# TRẠNG THÁI DỰ ÁN HIỆN TẠI

## Business Requirements (BR Register)

{ctx['br_register']}

## Functional Requirements (FR Register)

{ctx['fr_register']}

## Task Tracker

{ctx['task_tracker']}

## Clarification Tracker (CLR)

{ctx['clr_tracker']}

---

*Context được load lúc khởi động agent. Nếu có thay đổi file → restart agent.*
"""

    return [
        {
            "type": "text",
            "text": block1,
            "cache_control": {"type": "ephemeral"},
        },
        {
            "type": "text",
            "text": block2,
            "cache_control": {"type": "ephemeral"},
        },
    ]


# ---------------------------------------------------------------------------
# CLI loop
# ---------------------------------------------------------------------------

BANNER = """
╔══════════════════════════════════════════════════════╗
║       🤖 PM Agent — Thanh Yến Treasury               ║
║       Powered by Claude Sonnet 4.6                   ║
╚══════════════════════════════════════════════════════╝

Tôi là PM Agent của dự án. Bạn có thể:
  • Paste transcript / chat / meeting notes để tôi phân tích
  • Hỏi về trạng thái BR, FR, task, blocker
  • Gõ /status  → xem tổng quan dự án
  • Gõ /pending → xem CLR đang chờ
  • Gõ /help    → hướng dẫn
  • Gõ exit     → thoát

"""

HELP_TEXT = """
📖 HƯỚNG DẪN SỬ DỤNG PM AGENT

SLASH COMMANDS:
  /status   — Báo cáo tiến độ tổng quan
  /pending  — CLR đang chờ trả lời
  /blocked  — Task đang bị blocked
  /help     — Hiển thị hướng dẫn này

PASTE THÔNG TIN:
  • Transcript họp → tôi tag BR/FR/Decision/Task/Risk
  • Chat Zalo / Lark → tôi nhận diện requirement hoặc change
  • Mô tả bằng lời → "Anh Trung vừa nói muốn..."

INPUT TYPES:
  • /clarify [nội dung]  → phân tích ambiguity, soạn câu hỏi
  • /impact [change]     → phân tích impact trước khi commit
  • /breakdown [BR-ID]   → breakdown BR → FR + Tasks
"""


def print_streaming(stream) -> str:
    """Stream response ra màn hình, trả về full text."""
    full_text = ""
    for text in stream.text_stream:
        print(text, end="", flush=True)
        full_text += text
    print()  # newline sau khi stream xong
    return full_text


def show_cache_stats(usage) -> None:
    """Hiển thị cache stats nếu có."""
    created = getattr(usage, "cache_creation_input_tokens", 0) or 0
    read = getattr(usage, "cache_read_input_tokens", 0) or 0
    if created or read:
        parts = []
        if created:
            parts.append(f"cache written: {created:,} tokens")
        if read:
            parts.append(f"cache hit: {read:,} tokens")
        print(f"  [{' | '.join(parts)}]\n")


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Thiếu ANTHROPIC_API_KEY")
        print("   Hãy chạy: export ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print("⏳ Đang load project context từ repo...")
    ctx = load_project_context()
    system = build_system(ctx)
    print("✅ Đã load xong.\n")

    print(BANNER)

    conversation: list[dict] = []

    while True:
        try:
            raw = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Tạm biệt!")
            break

        if not raw:
            continue

        # ── Built-in commands ──────────────────────────────────────────────
        if raw.lower() in ("exit", "quit", "thoát", "bye"):
            print("👋 Tạm biệt!")
            break

        if raw.lower() == "/help":
            print(HELP_TEXT)
            continue

        # Slash commands → convert thành prompt cho agent
        slash_map = {
            "/status":  "Hãy báo cáo tiến độ tổng quan dự án theo format /report trong CLAUDE.md",
            "/pending": "Hãy liệt kê tất cả CLR đang chờ trả lời theo format /pending trong CLAUDE.md",
            "/blocked": "Hãy liệt kê tất cả item đang blocked theo format /blocked trong CLAUDE.md",
        }
        user_message = slash_map.get(raw.lower(), raw)

        conversation.append({"role": "user", "content": user_message})

        # ── Gọi API với streaming ──────────────────────────────────────────
        print("\nPM Agent: ", end="", flush=True)
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=4096,
                system=system,
                messages=conversation,
            ) as stream:
                assistant_text = print_streaming(stream)
                final = stream.get_final_message()

            show_cache_stats(final.usage)

            conversation.append({"role": "assistant", "content": assistant_text})

        except anthropic.AuthenticationError:
            print("❌ API key không hợp lệ. Kiểm tra lại ANTHROPIC_API_KEY.")
            conversation.pop()
        except anthropic.RateLimitError:
            print("⏳ Rate limit. Đợi một chút rồi thử lại.")
            conversation.pop()
        except anthropic.APIError as e:
            print(f"❌ Lỗi API: {e}")
            conversation.pop()

        print("-" * 54)


if __name__ == "__main__":
    main()
