"""Read new Tableau Desktop warnings and errors from its log, so nobody has to copy dialogs by hand.

Usage:
    python3 tableau_errors.py            # new real warnings and errors since the last run
    python3 tableau_errors.py --mark     # skip everything logged so far (run before opening a workbook)
    python3 tableau_errors.py --all      # every real warning and error in the current log

Exit code 1 when an error, a query failure or an open Tableau dialog is found, else 0.

Limits: a workbook that fails XML validation on load shows a dialog but may write nothing to the
log. The dialog text is drawn by Tableau and cannot be read through macOS accessibility, so the
script only reports that a dialog is open. Validate the XML before opening (see twb-xml.md).
"""
import json
import subprocess
import sys
from pathlib import Path

LOG_DIRS = [Path.home() / "Documents/My Tableau Repository/Logs",
            Path.home() / "Library/CloudStorage/OneDrive-Personal/Documents/My Tableau Repository/Logs"]
STATE = Path.home() / ".cache/tableau_errors_offset.json"
NOISE = ("InfoUtils::Lookup", "EventsConfigurator", "QObject::disconnect", "UserFilter for workbook info")
NOISE_KINDS = ("connector-plugin-error", "connector-plugin-warning", "connection-info-mismatch")
SERIOUS_KINDS = ("qp-process-query-error", "detailed-error-msg", "compute-task")


def find_log() -> Path:
    logs = [d / "log.txt" for d in LOG_DIRS if (d / "log.txt").exists()]
    if not logs:
        sys.exit("No Tableau log.txt found in My Tableau Repository/Logs")
    return max(logs, key=lambda p: p.stat().st_mtime)


def read_events(log: Path, start: int) -> tuple[list[dict], int]:
    size = log.stat().st_size
    if start > size:  # log rotated
        start = 0
    with log.open("rb") as f:
        f.seek(start)
        raw = f.read()
    events = []
    for line in raw.decode("utf-8", "ignore").splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("sev") not in ("warn", "error") or d.get("k") in NOISE_KINDS:
            continue
        text = json.dumps(d.get("v")) if not isinstance(d.get("v"), str) else d["v"]
        if any(n in text for n in NOISE):
            continue
        events.append({"ts": d.get("ts"), "sev": d["sev"], "kind": d.get("k"), "text": text})
    return events, size


def open_dialogs() -> list[str]:
    script = 'tell application "System Events" to if exists (first process whose name contains "Tableau") then tell (first process whose name contains "Tableau") to get name of every window'
    out = subprocess.run(["osascript", "-e", script], capture_output=True, text=True).stdout.strip()
    names = [n.strip() for n in out.split(",") if n.strip()]
    return [n for n in names if n.lower().startswith(("unable", "error", "warning"))]


def main() -> int:
    log = find_log()
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    start = 0 if "--all" in sys.argv else state.get(str(log), 0)
    events, end = read_events(log, start)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({**state, str(log): end}))
    if "--mark" in sys.argv:
        print(f"marked {log} at byte {end}")
        return 0
    for e in events:
        print(f"{e['ts']} {e['sev'].upper():5} {e['kind']}: {e['text'][:600]}")
    dialogs = open_dialogs()
    for d in dialogs:
        print(f"DIALOG OPEN: {d} (text not readable; check the log lines above)")
    serious = [e for e in events if e["sev"] == "error" or e["kind"] in SERIOUS_KINDS]
    print(f"{len(events)} warnings or errors, {len(serious)} serious, {len(dialogs)} dialogs open")
    return 1 if serious or dialogs else 0


if __name__ == "__main__":
    sys.exit(main())
