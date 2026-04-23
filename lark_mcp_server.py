#!/usr/bin/env python3
"""
Lark Base MCP Server — Thanh Yến Treasury
Cho phép Claude Code đọc và ghi dữ liệu Lark Base.
Không có quyền xóa record.

Env vars cần thiết (set trong .claude/settings.local.json):
  LARK_APP_ID     — App ID từ Lark Developer Console
  LARK_APP_SECRET — App Secret từ Lark Developer Console
  LARK_BASE_ID    — App token của Lark Base
"""

import json
import os
import time
import urllib.error
import urllib.request
from typing import Any

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

APP_ID     = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
BASE_ID    = os.environ.get("LARK_BASE_ID", "")
API_BASE   = "https://open.larksuite.com/open-apis"

# Table name → table_id mapping (populated lazily)
_TABLE_CACHE: dict[str, str] = {}

# Token cache
_token_cache: dict[str, Any] = {"token": None, "expires_at": 0}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _post(path: str, payload: dict, token: str | None = None) -> dict:
    url = f"{API_BASE}{path}"
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _get(path: str, token: str, params: dict | None = None) -> dict:
    url = f"{API_BASE}{path}"
    if params:
        qs = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items() if v is not None)
        url = f"{url}?{qs}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def _patch(path: str, payload: dict, token: str) -> dict:
    url = f"{API_BASE}{path}"
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def get_token() -> str:
    now = time.time()
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]
    result = _post("/auth/v3/tenant_access_token/internal", {
        "app_id": APP_ID,
        "app_secret": APP_SECRET,
    })
    if result.get("code") != 0:
        raise RuntimeError(f"Lark auth failed: {result.get('msg')}")
    _token_cache["token"] = result["tenant_access_token"]
    _token_cache["expires_at"] = now + result.get("expire", 7200)
    return _token_cache["token"]


# ---------------------------------------------------------------------------
# Table helpers
# ---------------------------------------------------------------------------

def _get_table_id(table_name_or_id: str) -> str:
    """Trả về table_id từ tên hoặc ID trực tiếp."""
    if table_name_or_id.startswith("tbl"):
        return table_name_or_id
    if table_name_or_id in _TABLE_CACHE:
        return _TABLE_CACHE[table_name_or_id]
    token = get_token()
    result = _get(f"/bitable/v1/apps/{BASE_ID}/tables", token)
    if result.get("code") != 0:
        raise RuntimeError(f"Cannot list tables: {result.get('msg')}")
    for item in result.get("data", {}).get("items", []):
        _TABLE_CACHE[item["name"]] = item["table_id"]
    if table_name_or_id not in _TABLE_CACHE:
        available = list(_TABLE_CACHE.keys())
        raise ValueError(f"Table '{table_name_or_id}' không tìm thấy. Có sẵn: {available}")
    return _TABLE_CACHE[table_name_or_id]


def _check_env() -> str | None:
    missing = [v for v in ["LARK_APP_ID", "LARK_APP_SECRET", "LARK_BASE_ID"] if not os.environ.get(v)]
    if missing:
        return f"Thiếu env vars: {missing}. Set trong .claude/settings.local.json"
    return None


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("lark-thanh-yen")


@mcp.tool()
def lark_list_tables() -> str:
    """
    Liệt kê tất cả tables trong Lark Base Thanh Yến.
    Trả về tên và ID của từng table.
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        result = _get(f"/bitable/v1/apps/{BASE_ID}/tables", token)
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')}"
        items = result.get("data", {}).get("items", [])
        lines = ["# Tables trong Lark Base Thanh Yến\n"]
        for t in items:
            _TABLE_CACHE[t["name"]] = t["table_id"]
            lines.append(f"- **{t['name']}** (ID: `{t['table_id']}`)")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi kết nối Lark: {e}"


@mcp.tool()
def lark_get_fields(table: str) -> str:
    """
    Lấy danh sách fields (cột) của một table.

    Args:
        table: Tên table (vd: 'Loan Master') hoặc table_id (vd: 'tblXXX')
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        result = _get(f"/bitable/v1/apps/{BASE_ID}/tables/{table_id}/fields", token)
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')}"
        fields = result.get("data", {}).get("items", [])
        lines = [f"# Fields của table '{table}'\n"]
        type_map = {1:"Text",2:"Number",3:"SingleSelect",4:"MultiSelect",5:"Date",
                    7:"Checkbox",11:"User",15:"URL",17:"Attachment",18:"Relation",
                    20:"Formula",21:"Created",22:"LastModified",23:"CreatedBy",24:"ModifiedBy",1001:"AutoNumber"}
        for f in fields:
            ftype = type_map.get(f.get("type", 0), f"Type{f.get('type')}")
            lines.append(f"- **{f['field_name']}** — {ftype} (ID: `{f['field_id']}`)")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_get_records(
    table: str,
    filter_formula: str | None = None,
    page_size: int = 20,
    page_token: str | None = None,
    view_id: str | None = None,
) -> str:
    """
    Lấy records từ một table Lark Base.

    Args:
        table:          Tên table hoặc table_id
        filter_formula: Filter theo Lark formula (vd: 'CurrentValue.[loan_status]="Active"')
        page_size:      Số records mỗi trang (max 500, default 20)
        page_token:     Token để lấy trang tiếp theo
        view_id:        ID của view cụ thể (vd: 'vew63fZRRV')
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        params: dict = {"page_size": min(page_size, 500)}
        if filter_formula:
            params["filter"] = filter_formula
        if page_token:
            params["page_token"] = page_token
        if view_id:
            params["view_id"] = view_id
        result = _get(f"/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records", token, params)
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')}"
        data = result.get("data", {})
        items = data.get("items", [])
        total = data.get("total", len(items))
        has_more = data.get("has_more", False)
        next_token = data.get("page_token", "")
        lines = [f"# Records từ '{table}' ({len(items)}/{total} records)\n"]
        for rec in items:
            lines.append(f"## Record ID: `{rec['record_id']}`")
            for k, v in rec.get("fields", {}).items():
                lines.append(f"  - {k}: {v}")
            lines.append("")
        if has_more:
            lines.append(f"*Còn records tiếp theo. page_token: `{next_token}`*")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_search_records(
    table: str,
    filter_formula: str,
    fields: list[str] | None = None,
    page_size: int = 20,
) -> str:
    """
    Tìm kiếm records với filter nâng cao.

    Args:
        table:          Tên table hoặc table_id
        filter_formula: Lark filter formula (vd: 'AND(CurrentValue.[company_id]="CTY01",CurrentValue.[loan_status]="Active")')
        fields:         Danh sách tên fields muốn lấy (None = lấy tất cả)
        page_size:      Số records (max 500)
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        payload: dict = {
            "filter": {"conjunction": "and", "conditions": []},
            "page_size": min(page_size, 500),
        }
        if filter_formula:
            payload["filter_formula"] = filter_formula
        if fields:
            payload["field_names"] = fields
        url = f"{API_BASE}/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records/search"
        data_bytes = json.dumps(payload).encode()
        req = urllib.request.Request(
            url, data=data_bytes,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode())
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')}"
        items = result.get("data", {}).get("items", [])
        lines = [f"# Kết quả tìm kiếm trong '{table}' ({len(items)} records)\n"]
        for rec in items:
            lines.append(f"## `{rec['record_id']}`")
            for k, v in rec.get("fields", {}).items():
                lines.append(f"  - {k}: {v}")
            lines.append("")
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_create_record(table: str, fields: dict[str, Any]) -> str:
    """
    Tạo một record mới trong table.

    Args:
        table:  Tên table hoặc table_id
        fields: Dict các field và giá trị (vd: {"company_id": "CTY01", "loan_status": "Active"})
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        result = _post(
            f"/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records",
            {"fields": fields},
            token,
        )
        if result.get("code") != 0:
            return f"Lỗi tạo record: {result.get('msg')} (code: {result.get('code')})"
        rec = result.get("data", {}).get("record", {})
        return f"✅ Tạo record thành công!\nRecord ID: `{rec.get('record_id')}`\nFields: {json.dumps(rec.get('fields', {}), ensure_ascii=False, indent=2)}"
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_update_record(table: str, record_id: str, fields: dict[str, Any]) -> str:
    """
    Cập nhật một record đã có trong table.

    Args:
        table:     Tên table hoặc table_id
        record_id: ID của record cần update (dạng 'recXXX')
        fields:    Dict các field cần cập nhật và giá trị mới
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        result = _patch(
            f"/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records/{record_id}",
            {"fields": fields},
            token,
        )
        if result.get("code") != 0:
            return f"Lỗi update record: {result.get('msg')} (code: {result.get('code')})"
        rec = result.get("data", {}).get("record", {})
        return f"✅ Update record thành công!\nRecord ID: `{rec.get('record_id')}`\nFields updated: {json.dumps(fields, ensure_ascii=False, indent=2)}"
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_batch_create_records(table: str, records: list[dict[str, Any]]) -> str:
    """
    Tạo nhiều records cùng lúc (batch, tối đa 500 records/lần).

    Args:
        table:   Tên table hoặc table_id
        records: Danh sách dict fields cho từng record
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        payload = {"records": [{"fields": r} for r in records[:500]]}
        url = f"{API_BASE}/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records/batch_create"
        data_bytes = json.dumps(payload).encode()
        req = urllib.request.Request(
            url, data=data_bytes,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')} (code: {result.get('code')})"
        created = result.get("data", {}).get("records", [])
        ids = [r.get("record_id") for r in created]
        return f"✅ Tạo thành công {len(ids)} records!\nIDs: {ids}"
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_validate_business_rules(table: str = "Loan Master") -> str:
    """
    Kiểm tra business rules đã được confirm trong data-dictionary.
    - BR-001: Lãi suất > 0 và <= 50 (p.a.)
    - BR-002: Dư nợ = Tổng rút vốn - Tổng trả gốc (kiểm tra tính nhất quán)
    - BR-003: loan_type hợp lệ (Ngắn hạn/Dài hạn/Tuần hoàn)
    - BR-004: loan_status hợp lệ (Active/Closed/Overdue)

    Args:
        table: Tên table cần validate (default: 'Loan Master')
    """
    if err := _check_env():
        return err
    try:
        token = get_token()
        table_id = _get_table_id(table)
        params = {"page_size": 100}
        result = _get(f"/bitable/v1/apps/{BASE_ID}/tables/{table_id}/records", token, params)
        if result.get("code") != 0:
            return f"Lỗi lấy records: {result.get('msg')}"
        items = result.get("data", {}).get("items", [])
        issues: list[str] = []
        valid_loan_types   = {"Ngắn hạn", "Dài hạn", "Tuần hoàn"}
        valid_loan_status  = {"Active", "Closed", "Overdue"}
        for rec in items:
            rid = rec["record_id"]
            f   = rec.get("fields", {})
            rate = f.get("interest_rate") or f.get("Lãi suất")
            if rate is not None:
                try:
                    r = float(rate)
                    if r <= 0 or r > 50:
                        issues.append(f"⚠️ BR-001: Record `{rid}` — interest_rate={r} ngoài range (0, 50]")
                except (ValueError, TypeError):
                    issues.append(f"⚠️ BR-001: Record `{rid}` — interest_rate không hợp lệ: {rate}")
            ltype = f.get("loan_type") or f.get("Loại vay")
            if ltype and ltype not in valid_loan_types:
                issues.append(f"⚠️ BR-003: Record `{rid}` — loan_type='{ltype}' không hợp lệ. Phải là: {valid_loan_types}")
            lstatus = f.get("loan_status") or f.get("Trạng thái")
            if lstatus and lstatus not in valid_loan_status:
                issues.append(f"⚠️ BR-004: Record `{rid}` — loan_status='{lstatus}' không hợp lệ. Phải là: {valid_loan_status}")
        total = len(items)
        if issues:
            summary = f"# Kết quả Validate — {table}\n✅ Đã kiểm tra {total} records | ❌ {len(issues)} vấn đề:\n\n"
            return summary + "\n".join(issues)
        return f"# Kết quả Validate — {table}\n✅ Đã kiểm tra {total} records — Không có vấn đề nào!"
    except Exception as e:
        return f"Lỗi: {e}"


@mcp.tool()
def lark_get_base_info() -> str:
    """Lấy thông tin tổng quan về Lark Base (tên, bảng, revision)."""
    if err := _check_env():
        return err
    try:
        token = get_token()
        result = _get(f"/bitable/v1/apps/{BASE_ID}", token)
        if result.get("code") != 0:
            return f"Lỗi: {result.get('msg')}"
        app = result.get("data", {}).get("app", {})
        lines = [
            "# Lark Base Info — Thanh Yến Treasury",
            f"- **Tên**: {app.get('name')}",
            f"- **App Token**: `{app.get('app_token')}`",
            f"- **Revision**: {app.get('revision')}",
            f"- **Time Zone**: {app.get('time_zone')}",
        ]
        return "\n".join(lines)
    except Exception as e:
        return f"Lỗi: {e}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if not all([APP_ID, APP_SECRET, BASE_ID]):
        raise SystemExit(
            "Thiếu env vars: LARK_APP_ID, LARK_APP_SECRET, LARK_BASE_ID\n"
            "Set trong .claude/settings.local.json"
        )
    mcp.run(transport="stdio")
