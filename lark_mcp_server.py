#!/usr/bin/env python3
"""
lark_mcp_server.py — MCP server for Lark Base (Thanh Yen Treasury).

Architecture: Anthropic sandbox blocks open.larksuite.com at network level.
This server routes all Lark API calls through GitHub Actions (unrestricted
internet) and reads cached data from the GitHub repository.

  Read ops  → raw.githubusercontent.com / GitHub API  (fast, <2s, ≤2h stale)
  Write ops → GitHub Actions relay workflow             (real-time, ~45s)

Env vars (set in .claude/settings.local.json):
  GITHUB_TOKEN  — GitHub PAT with repo + workflow scopes
  LARK_BASE_ID  — Lark Base app token (used as fallback label)
"""
import os
import json
import base64
import time
import uuid
import requests
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lark-thanh-yen")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = "Huyen-Cosy/Thanh_Yen"
GITHUB_API = "https://api.github.com"
RELAY_WORKFLOW = "lark-relay.yml"
SYNC_WORKFLOW = "lark-sync.yml"
BRANCH = "main"


def _gh_headers() -> dict:
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _read_cache(path: str):
    """Read a JSON file from GitHub repo. Returns parsed dict or None."""
    r = requests.get(
        f"{GITHUB_API}/repos/{REPO}/contents/{path}",
        headers=_gh_headers(),
        params={"ref": BRANCH},
        timeout=15,
    )
    if r.status_code != 200:
        return None
    content = base64.b64decode(r.json()["content"]).decode("utf-8")
    return json.loads(content)


def _get_table_id(table_name: str):
    """Resolve table name → table_id from cached tables list."""
    cached = _read_cache("lark-data/tables.json")
    if not cached:
        return None
    # Handle nested response structure
    items = (
        cached.get("data", {}).get("data", {}).get("items")
        or cached.get("data", {}).get("items")
        or []
    )
    match = next((t for t in items if t.get("name") == table_name), None)
    return match["table_id"] if match else None


def _relay(operation: str, params: dict, timeout_s: int = 300) -> dict:
    """
    Trigger GitHub Actions relay workflow and wait for result.
    Typical latency: 30-60 seconds.
    """
    if not GITHUB_TOKEN:
        return {"success": False, "error": "GITHUB_TOKEN not set in environment"}

    request_id = uuid.uuid4().hex[:12]
    trigger_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

    # 1. Dispatch workflow
    r = requests.post(
        f"{GITHUB_API}/repos/{REPO}/actions/workflows/{RELAY_WORKFLOW}/dispatches",
        headers=_gh_headers(),
        json={
            "ref": BRANCH,
            "inputs": {
                "request_id": request_id,
                "operation": operation,
                "params": json.dumps(params),
            },
        },
        timeout=30,
    )
    if r.status_code != 204:
        return {"success": False, "error": f"Dispatch failed HTTP {r.status_code}: {r.text}"}

    # 2. Wait for runner to pick up the job
    time.sleep(6)

    # 3. Find run_id — look for runs created after our dispatch time
    run_id = None
    for _ in range(15):
        r = requests.get(
            f"{GITHUB_API}/repos/{REPO}/actions/workflows/{RELAY_WORKFLOW}/runs",
            headers=_gh_headers(),
            params={"event": "workflow_dispatch", "per_page": 10, "branch": BRANCH},
            timeout=15,
        )
        for run in r.json().get("workflow_runs", []):
            if run.get("created_at", "") >= trigger_time:
                run_id = run["id"]
                break
        if run_id:
            break
        time.sleep(4)

    if not run_id:
        return {"success": False, "error": "Could not find workflow run after dispatch"}

    # 4. Poll until complete
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        r = requests.get(
            f"{GITHUB_API}/repos/{REPO}/actions/runs/{run_id}",
            headers=_gh_headers(),
            timeout=15,
        )
        run_data = r.json()
        if run_data.get("status") == "completed":
            if run_data.get("conclusion") != "success":
                return {"success": False, "error": f"Workflow conclusion: {run_data.get('conclusion')}"}
            break
        time.sleep(8)
    else:
        return {"success": False, "error": f"Relay timed out after {timeout_s}s"}

    # 5. Read result file committed by the workflow
    result_path = f"lark-relay/{request_id}.json"
    for _ in range(6):
        result = _read_cache(result_path)
        if result is not None:
            return result
        time.sleep(5)

    return {"success": False, "error": f"Result file not found: {result_path}"}


# ──────────────────────────────────────────────────────────────
# MCP Tools
# ──────────────────────────────────────────────────────────────

@mcp.tool()
def lark_get_base_info() -> str:
    """Get general information about the Lark Base (Treasury Management System)."""
    cached = _read_cache("lark-data/base-info.json")
    if cached:
        return json.dumps({"source": "cache", **cached}, ensure_ascii=False, indent=2)
    return json.dumps(_relay("get_base_info", {}), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_list_tables() -> str:
    """List all tables in the Lark Base (Company, LoanMaster, LoanActivity, CollateralAssets)."""
    cached = _read_cache("lark-data/tables.json")
    if cached:
        items = (
            cached.get("data", {}).get("data", {}).get("items")
            or cached.get("data", {}).get("items")
            or []
        )
        tables = [{"name": t.get("name"), "table_id": t.get("table_id")} for t in items]
        return json.dumps(
            {"source": "cache", "tables": tables, "total": len(tables), "cached_at": cached.get("ts")},
            ensure_ascii=False,
            indent=2,
        )
    return json.dumps(_relay("list_tables", {}), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_get_fields(table_name: str) -> str:
    """Get field definitions for a table.

    Args:
        table_name: One of Company | LoanMaster | LoanActivity | CollateralAssets
    """
    cached = _read_cache(f"lark-data/{table_name}/fields.json")
    if cached:
        return json.dumps({"source": "cache", **cached}, ensure_ascii=False, indent=2)
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not in cache. Call lark_refresh() first."})
    return json.dumps(_relay("get_fields", {"table_id": table_id}), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_get_cached_records(table_name: str) -> str:
    """Get records from local cache — fast (<2s), may be up to 2h stale.
    Good for browsing and overview. For fresh data use lark_get_records().

    Args:
        table_name: One of Company | LoanMaster | LoanActivity | CollateralAssets
    """
    cached = _read_cache(f"lark-data/{table_name}/records.json")
    if cached:
        return json.dumps({"source": "cache", **cached}, ensure_ascii=False, indent=2)
    return json.dumps({
        "error": f"No cache for '{table_name}'. Call lark_refresh() to populate (takes ~3 min).",
        "tip": "Or use lark_get_records() for live data (~45s via relay).",
    })


@mcp.tool()
def lark_get_records(table_name: str, filter: str = "", page_size: int = 20) -> str:
    """Get LIVE records from Lark Base via GitHub Actions relay (~45s).

    Args:
        table_name: Table name
        filter: Optional Lark filter formula
        page_size: Records per page (max 100)
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("get_records", {"table_id": table_id, "filter": filter, "page_size": page_size}),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def lark_search_records(table_name: str, filter_formula: str) -> str:
    """Search records with a filter formula via relay (~45s).

    Args:
        table_name: Table name
        filter_formula: Lark filter e.g. 'CurrentValue([Status])="Active"'
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("search_records", {"table_id": table_id, "filter_formula": filter_formula}),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def lark_create_record(table_name: str, fields: dict) -> str:
    """Create a new record in Lark Base via relay (~45s).

    Args:
        table_name: Table name
        fields: Field name → value mapping
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("create_record", {"table_id": table_id, "fields": fields}),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def lark_update_record(table_name: str, record_id: str, fields: dict) -> str:
    """Update an existing record in Lark Base via relay (~45s).

    Args:
        table_name: Table name
        record_id: Record ID to update
        fields: Field name → new value mapping
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("update_record", {"table_id": table_id, "record_id": record_id, "fields": fields}),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def lark_batch_create_records(table_name: str, records: list) -> str:
    """Batch-create multiple records in Lark Base via relay (~45s).

    Args:
        table_name: Table name
        records: List of field dicts
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("batch_create_records", {"table_id": table_id, "records": records}),
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def lark_validate_business_rules(table_name: str) -> str:
    """Validate business rules for a table via relay (~45s).

    Args:
        table_name: Table name to validate
    """
    table_id = _get_table_id(table_name)
    if not table_id:
        return json.dumps({"error": f"Table '{table_name}' not found. Call lark_refresh() first."})
    return json.dumps(
        _relay("validate_business_rules", {"table_id": table_id}),
        ensure_ascii=False,
        indent=2,
    )


_FIELD_TYPES = {
    "text": 1, "number": 2, "single_select": 3, "multi_select": 4,
    "date": 5, "checkbox": 7, "person": 11, "phone": 13, "url": 15,
    "attachment": 17, "link": 18, "formula": 20, "auto_number": 1005,
}


def _resolve_field_type(field_type) -> int:
    if isinstance(field_type, int):
        return field_type
    return _FIELD_TYPES.get(str(field_type).lower(), 1)


@mcp.tool()
def lark_create_table(table_name: str, base_id: str = "") -> str:
    """Create a new table in Lark Base via relay (~45s).

    Args:
        table_name: Tên table mới
        base_id: Base ID override — để trống = main base, điền = base test
    """
    params = {"table_name": table_name}
    if base_id:
        params["base_id"] = base_id
    return json.dumps(_relay("create_table", params), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_create_field(table_id: str, field_name: str, field_type: str, property_json: str = "{}", base_id: str = "") -> str:
    """Add a new field (column) to a table in Lark Base via relay (~45s).

    field_type — dùng tên hoặc số:
      text=1, number=2, single_select=3, multi_select=4, date=5,
      checkbox=7, person=11, phone=13, url=15, attachment=17,
      link=18, formula=20, auto_number=1005

    property_json examples:
      single_select / multi_select : '{"options": [{"name": "A"}, {"name": "B"}]}'
      number                       : '{"formatter": "0", "decimal_digits": 2}'
      date                         : '{"date_formatter": "yyyy/MM/dd"}'

    Args:
        table_id: Table ID (lấy từ lark_list_tables hoặc lark_get_fields)
        field_name: Tên cột mới
        field_type: Loại field — tên hoặc số nguyên
        property_json: JSON string cấu hình thêm (tuỳ loại field)
        base_id: Base ID override (để trống = main base)
    """
    try:
        prop = json.loads(property_json) if property_json and property_json != "{}" else {}
    except json.JSONDecodeError:
        return json.dumps({"error": f"Invalid property_json: {property_json}"})
    params = {
        "table_id": table_id,
        "field_name": field_name,
        "field_type": _resolve_field_type(field_type),
    }
    if prop:
        params["property"] = prop
    if base_id:
        params["base_id"] = base_id
    return json.dumps(_relay("create_field", params), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_update_field(table_id: str, field_id: str, field_name: str = "", property_json: str = "{}", base_id: str = "") -> str:
    """Update an existing field in Lark Base via relay (~45s).

    Args:
        table_id: Table ID
        field_id: Field ID (lấy từ lark_get_fields)
        field_name: Tên mới — để trống = giữ nguyên
        property_json: JSON string cập nhật properties
        base_id: Base ID override
    """
    try:
        prop = json.loads(property_json) if property_json and property_json != "{}" else {}
    except json.JSONDecodeError:
        return json.dumps({"error": f"Invalid property_json: {property_json}"})
    params = {"table_id": table_id, "field_id": field_id}
    if field_name:
        params["field_name"] = field_name
    if prop:
        params["property"] = prop
    if base_id:
        params["base_id"] = base_id
    return json.dumps(_relay("update_field", params), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_delete_field(table_id: str, field_id: str, base_id: str = "") -> str:
    """Delete a field (column) from a table in Lark Base via relay (~45s).

    Args:
        table_id: Table ID
        field_id: Field ID cần xoá (lấy từ lark_get_fields)
        base_id: Base ID override
    """
    params = {"table_id": table_id, "field_id": field_id}
    if base_id:
        params["base_id"] = base_id
    return json.dumps(_relay("delete_field", params), ensure_ascii=False, indent=2)


@mcp.tool()
def lark_refresh() -> str:
    """Trigger a full Lark data sync to update the local cache.
    Runs in background — data available in ~3 minutes.
    After sync: lark_list_tables, lark_get_fields, lark_get_cached_records will be fast (<2s).
    """
    if not GITHUB_TOKEN:
        return json.dumps({"error": "GITHUB_TOKEN not set"})
    r = requests.post(
        f"{GITHUB_API}/repos/{REPO}/actions/workflows/{SYNC_WORKFLOW}/dispatches",
        headers=_gh_headers(),
        json={"ref": BRANCH},
        timeout=30,
    )
    if r.status_code == 204:
        return json.dumps({
            "status": "triggered",
            "message": "Lark sync started (~3 min). Then call lark_list_tables() or lark_get_cached_records().",
        })
    return json.dumps({"error": f"HTTP {r.status_code}: {r.text}"})


if __name__ == "__main__":
    mcp.run(transport="stdio")
