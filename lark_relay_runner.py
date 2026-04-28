#!/usr/bin/env python3
"""lark_relay_runner.py — Lark API runner executed by GitHub Actions relay."""
import os
import json
import requests
from datetime import datetime, timezone

LARK_APP_ID = os.environ["LARK_APP_ID"]
LARK_APP_SECRET = os.environ["LARK_APP_SECRET"]
LARK_BASE_ID = os.environ["LARK_BASE_ID"]
OPERATION = os.environ["OPERATION"]
PARAMS = json.loads(os.environ.get("PARAMS", "{}"))
OUTPUT_FILE = os.environ["OUTPUT_FILE"]
API_BASE = "https://open.larksuite.com/open-apis"


def get_token() -> str:
    r = requests.post(
        f"{API_BASE}/auth/v3/tenant_access_token/internal",
        json={"app_id": LARK_APP_ID, "app_secret": LARK_APP_SECRET},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["tenant_access_token"]


def lark_get(path: str, headers: dict, params: dict = None) -> dict:
    r = requests.get(f"{API_BASE}{path}", headers=headers, params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


def lark_post(path: str, headers: dict, body: dict) -> dict:
    r = requests.post(f"{API_BASE}{path}", headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def lark_put(path: str, headers: dict, body: dict) -> dict:
    r = requests.put(f"{API_BASE}{path}", headers=headers, json=body, timeout=30)
    r.raise_for_status()
    return r.json()


def lark_delete(path: str, headers: dict) -> dict:
    r = requests.delete(f"{API_BASE}{path}", headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def get_all_records(table_id: str, headers: dict, active_base_id: str = None) -> list:
    if active_base_id is None:
        active_base_id = LARK_BASE_ID
    records = []
    page_token = None
    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        data = lark_get(
            f"/bitable/v1/apps/{active_base_id}/tables/{table_id}/records",
            headers,
            params,
        )
        items = data.get("data", {}).get("items", [])
        records.extend(items)
        if not data.get("data", {}).get("has_more"):
            break
        page_token = data.get("data", {}).get("page_token")
    return records


def write_output(data: dict):
    output_dir = os.path.dirname(OUTPUT_FILE)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ {OPERATION} → {OUTPUT_FILE}")


def run():
    ts = datetime.now(timezone.utc).isoformat()
    # Allow per-request base_id override (dùng cho base test)
    ACTIVE_BASE_ID = PARAMS.get("base_id") or LARK_BASE_ID

    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # ── Read operations ────────────────────────────────────────────

        if OPERATION == "get_base_info":
            data = lark_get(f"/bitable/v1/apps/{ACTIVE_BASE_ID}", headers)
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "list_tables":
            data = lark_get(f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables", headers)
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "get_fields":
            table_id = PARAMS["table_id"]
            data = lark_get(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/fields",
                headers,
                {"page_size": 100},
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "get_records":
            table_id = PARAMS["table_id"]
            params = {"page_size": PARAMS.get("page_size", 20)}
            if PARAMS.get("filter"):
                params["filter"] = PARAMS["filter"]
            if PARAMS.get("page_token"):
                params["page_token"] = PARAMS["page_token"]
            data = lark_get(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/records",
                headers,
                params,
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "search_records":
            table_id = PARAMS["table_id"]
            params = {"page_size": 100}
            if PARAMS.get("filter_formula"):
                params["filter"] = PARAMS["filter_formula"]
            data = lark_get(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/records",
                headers,
                params,
            )
            write_output({"success": True, "data": data, "ts": ts})

        # ── Record write operations ────────────────────────────────────

        elif OPERATION == "create_record":
            table_id = PARAMS["table_id"]
            data = lark_post(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/records",
                headers,
                {"fields": PARAMS["fields"]},
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "update_record":
            table_id = PARAMS["table_id"]
            record_id = PARAMS["record_id"]
            data = lark_put(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/records/{record_id}",
                headers,
                {"fields": PARAMS["fields"]},
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "batch_create_records":
            table_id = PARAMS["table_id"]
            payload = {"records": [{"fields": r} for r in PARAMS["records"]]}
            data = lark_post(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/records/batch_create",
                headers,
                payload,
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "validate_business_rules":
            table_id = PARAMS["table_id"]
            records = get_all_records(table_id, headers, ACTIVE_BASE_ID)
            issues = []
            for rec in records:
                fields = rec.get("fields", {})
                rid = rec.get("record_id", "?")
                if not fields.get("Tên công ty") and not fields.get("Cong_Ty") and not fields.get("company"):
                    issues.append({"record_id": rid, "rule": "BR-001", "msg": "Thiếu liên kết công ty"})
                for amt_field in ["Số tiền", "So_Tien", "amount", "Dư nợ"]:
                    val = fields.get(amt_field)
                    if val is not None and isinstance(val, (int, float)) and val <= 0:
                        issues.append({"record_id": rid, "rule": "BR-002", "msg": f"{amt_field} phải > 0"})
            write_output({
                "success": True,
                "data": {
                    "table_id": table_id,
                    "total_records": len(records),
                    "issues_found": len(issues),
                    "issues": issues,
                    "status": "PASS" if not issues else "FAIL",
                },
                "ts": ts,
            })

        # ── Schema management (table & field) ─────────────────────────

        elif OPERATION == "create_table":
            body = {"table": {"name": PARAMS["table_name"]}}
            if PARAMS.get("fields"):
                body["table"]["fields"] = PARAMS["fields"]
            data = lark_post(f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables", headers, body)
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "create_field":
            table_id = PARAMS["table_id"]
            body = {
                "field_name": PARAMS["field_name"],
                "type": PARAMS["field_type"],
            }
            if PARAMS.get("property"):
                body["property"] = PARAMS["property"]
            data = lark_post(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/fields",
                headers,
                body,
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "update_field":
            table_id = PARAMS["table_id"]
            field_id = PARAMS["field_id"]
            body = {}
            if PARAMS.get("field_name"):
                body["field_name"] = PARAMS["field_name"]
            if PARAMS.get("field_type"):
                body["type"] = PARAMS["field_type"]
            if PARAMS.get("property"):
                body["property"] = PARAMS["property"]
            data = lark_put(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/fields/{field_id}",
                headers,
                body,
            )
            write_output({"success": True, "data": data, "ts": ts})

        elif OPERATION == "delete_field":
            table_id = PARAMS["table_id"]
            field_id = PARAMS["field_id"]
            data = lark_delete(
                f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/fields/{field_id}",
                headers,
            )
            write_output({"success": True, "data": data, "ts": ts})

        # ── Sync ──────────────────────────────────────────────────────

        elif OPERATION == "sync_all":
            base_data = lark_get(f"/bitable/v1/apps/{ACTIVE_BASE_ID}", headers)
            tables_data = lark_get(f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables", headers)
            tables = tables_data.get("data", {}).get("items", [])

            os.makedirs("lark-data", exist_ok=True)
            with open("lark-data/base-info.json", "w", encoding="utf-8") as f:
                json.dump({"success": True, "data": base_data, "ts": ts}, f, ensure_ascii=False, indent=2)
            with open("lark-data/tables.json", "w", encoding="utf-8") as f:
                json.dump({"success": True, "data": tables_data, "ts": ts}, f, ensure_ascii=False, indent=2)

            synced = {}
            for table in tables:
                table_id = table["table_id"]
                name = table.get("name", table_id)
                safe_name = name.replace("/", "_").replace(" ", "_")

                fields_data = lark_get(
                    f"/bitable/v1/apps/{ACTIVE_BASE_ID}/tables/{table_id}/fields",
                    headers,
                    {"page_size": 100},
                )
                records = get_all_records(table_id, headers, ACTIVE_BASE_ID)

                dir_path = f"lark-data/{safe_name}"
                os.makedirs(dir_path, exist_ok=True)
                with open(f"{dir_path}/fields.json", "w", encoding="utf-8") as f:
                    json.dump({"success": True, "data": fields_data, "ts": ts}, f, ensure_ascii=False, indent=2)
                with open(f"{dir_path}/records.json", "w", encoding="utf-8") as f:
                    json.dump(
                        {"success": True, "data": {"items": records, "total": len(records)}, "ts": ts},
                        f,
                        ensure_ascii=False,
                        indent=2,
                    )
                synced[name] = {"records": len(records), "table_id": table_id}
                print(f"  synced {name}: {len(records)} records")

            summary = {"synced_at": ts, "tables": synced, "total_tables": len(tables)}
            write_output({"success": True, "data": summary, "ts": ts})

        else:
            write_output({"success": False, "error": f"Unknown operation: {OPERATION}", "ts": ts})
            exit(1)

    except Exception as e:
        write_output({"success": False, "error": str(e), "ts": ts})
        print(f"✗ ERROR: {e}")
        exit(1)


if __name__ == "__main__":
    run()
