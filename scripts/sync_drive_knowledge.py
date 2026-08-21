#!/usr/bin/env python3
"""Sync official tax knowledge from Google Drive into knowledge/drive_mirror.

Modes:
  1) Service account (preferred): set GOOGLE_SERVICE_ACCOUNT_JSON to a credentials JSON path.
  2) Manifest file IDs: knowledge/drive_manifest.json → files[] with {id, name}
  3) Manual: copy PDFs into knowledge/official/ and skip this script.

Usage (repo root):
  export GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/sa.json
  python scripts/sync_drive_knowledge.py
  python scripts/seed_knowledge.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "knowledge" / "drive_mirror"
OFFICIAL = ROOT / "knowledge" / "official"
MANIFEST = ROOT / "knowledge" / "drive_manifest.json"

PRIMARY = os.getenv("GOOGLE_DRIVE_PRIMARY_FOLDER", "1Jx0cipUqQyGnJk4hFCURzWIg1Abo1Del")
FALLBACK = os.getenv("GOOGLE_DRIVE_FALLBACK_FOLDER", "1NcBkZOTemmVfnNKY7FgxuqbIXj6f4Dtl")

ALLOWED_EXT = {".pdf", ".docx", ".doc", ".md", ".txt"}


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def sync_with_service_account(folder_ids: list[str]) -> int:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseDownload
    except ImportError:
        print(
            "google-api-python-client / google-auth not installed.\n"
            "  pip install google-api-python-client google-auth",
            file=sys.stderr,
        )
        return 0

    cred_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not cred_path or not Path(cred_path).exists():
        print("GOOGLE_SERVICE_ACCOUNT_JSON not set or file missing.", file=sys.stderr)
        return 0

    scopes = ["https://www.googleapis.com/auth/drive.readonly"]
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
    service = build("drive", "v3", credentials=creds, cache_discovery=False)

    MIRROR.mkdir(parents=True, exist_ok=True)
    count = 0

    def list_files(folder_id: str, prefix: str = "") -> None:
        nonlocal count
        q = f"'{folder_id}' in parents and trashed=false"
        page_token = None
        while True:
            resp = (
                service.files()
                .list(
                    q=q,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType)",
                    pageToken=page_token,
                    pageSize=100,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )
            for f in resp.get("files", []):
                name = f["name"]
                mime = f.get("mimeType", "")
                fid = f["id"]
                if mime == "application/vnd.google-apps.folder":
                    list_files(fid, prefix=f"{prefix}{name}/")
                    continue
                ext = Path(name).suffix.lower()
                # Google Docs export not handled here; only binary uploads
                if ext not in ALLOWED_EXT and mime.startswith("application/vnd.google-apps"):
                    print(f"skip google-native: {prefix}{name}")
                    continue
                if ext not in ALLOWED_EXT and mime != "application/pdf":
                    print(f"skip: {prefix}{name} ({mime})")
                    continue
                safe = (prefix + name).replace("/", "__")
                out = MIRROR / safe
                if out.exists() and out.stat().st_size > 0:
                    print(f"exists: {out.name}")
                    continue
                request = service.files().get_media(fileId=fid)
                import io

                buf = io.BytesIO()
                downloader = MediaIoBaseDownload(buf, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                out.write_bytes(buf.getvalue())
                count += 1
                print(f"downloaded: {out.name} ({out.stat().st_size} bytes)")
            page_token = resp.get("nextPageToken")
            if not page_token:
                break

    for fid in folder_ids:
        print(f"=== folder {fid} ===")
        try:
            list_files(fid)
        except Exception as e:
            print(f"ERROR folder {fid}: {e}", file=sys.stderr)
    return count


def sync_manifest_files(manifest: dict) -> int:
    """Optional: download explicit file IDs via gdown if available."""
    files = manifest.get("files") or []
    if not files:
        return 0
    try:
        import gdown  # type: ignore
    except ImportError:
        print("gdown not installed (pip install gdown) — skip manifest files", file=sys.stderr)
        return 0
    MIRROR.mkdir(parents=True, exist_ok=True)
    n = 0
    for item in files:
        fid = item.get("id")
        name = item.get("name") or f"{fid}.pdf"
        if not fid:
            continue
        out = MIRROR / name
        url = f"https://drive.google.com/uc?id={fid}"
        try:
            gdown.download(url, str(out), quiet=False)
            n += 1
        except Exception as e:
            print(f"gdown fail {name}: {e}", file=sys.stderr)
    return n


def main() -> None:
    manifest = load_manifest()
    folder_ids = []
    env_ids = os.getenv("GOOGLE_DRIVE_FOLDER_IDS", "").strip()
    if env_ids:
        folder_ids.extend([x.strip() for x in env_ids.split(",") if x.strip()])
    else:
        folder_ids.append(manifest.get("primary_folder_id") or PRIMARY)
        folder_ids.append(manifest.get("fallback_folder_id") or FALLBACK)

    print("Target folders:", folder_ids)
    n = sync_with_service_account(folder_ids)
    n += sync_manifest_files(manifest)

    if n == 0:
        print(
            "\nNo files synced automatically.\n"
            "Options:\n"
            "  1) Set GOOGLE_SERVICE_ACCOUNT_JSON and share Drive folders with the SA email\n"
            "  2) Manually copy official PDFs into knowledge/official/\n"
            "  3) Add file ids to knowledge/drive_manifest.json under files[]\n"
            "Then run: python scripts/seed_knowledge.py\n"
        )
    else:
        print(f"\nSynced {n} file(s) → {MIRROR}")
        print("Next: python scripts/seed_knowledge.py")

    OFFICIAL.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    main()
