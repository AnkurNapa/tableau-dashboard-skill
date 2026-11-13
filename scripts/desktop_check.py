#!/usr/bin/env python3
"""Open each workbook in Tableau Desktop, read the log, close Desktop. Nobody copies error dialogs by hand.

Each file goes through check_twb.py first (a .twb only); a file that fails it is never opened.
No keystrokes or clicks: open -a starts Desktop, pkill closes it, tableau_errors.py reads the log.
Desktop runs the queries of the active dashboard only, so to test every dashboard write one copy per
dashboard with that one active (the window carrying maximized='true') and pass them all.

Usage: python3 desktop_check.py book.twb [book_overview.twb ...]
Exit code 1 when any file has issues.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = Path.home() / "Documents/My Tableau Repository/Logs/log.txt"
KEEP = ("qp-process-query-error", "detailed-error", "DIALOG", "Ignoring", "serious", "error:")


def app():
    found = sorted(Path("/Applications").glob("Tableau Desktop*.app"))
    if not found:
        sys.exit("No Tableau Desktop app in /Applications")
    return str(found[-1])


def run(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def wait_quiet(cap=90, quiet=12, floor=35):
    """Wait until the log stops growing for `quiet` seconds (and at least `floor` seconds have passed)."""
    t0, last, still = time.time(), -1, 0
    while time.time() - t0 < cap:
        size = LOG.stat().st_size if LOG.exists() else 0
        still = still + 1 if size == last else 0
        last = size
        if still >= quiet and time.time() - t0 > floor:
            return
        time.sleep(1)


def check_one(path, desktop):
    if path.suffix == ".twb":
        code, msg = run(sys.executable, str(HERE / "check_twb.py"), str(path))
        if code:
            return False, f"check_twb failed, not opened\n{msg[-1500:]}"
    run(sys.executable, str(HERE / "tableau_errors.py"), "--mark")
    subprocess.run(["open", "-a", desktop, str(path)])
    time.sleep(5)
    wait_quiet()
    c1, m1 = run(sys.executable, str(HERE / "tableau_errors.py"))
    subprocess.run(["pkill", "-f", "Tableau Desktop"])
    time.sleep(4)  # query errors reach the log only after their dialog closes
    c2, m2 = run(sys.executable, str(HERE / "tableau_errors.py"))
    lines = [l[:400] for l in (m1 + "\n" + m2).splitlines() if any(k in l for k in KEEP)]
    return not (c1 or c2), "\n".join(lines)


def main():
    files = [Path(a) for a in sys.argv[1:]]
    if not files:
        sys.exit(__doc__)
    desktop, bad = app(), 0
    for f in files:
        ok, msg = check_one(f, desktop)
        bad += not ok
        print(f"## {f.name}: {'CLEAN' if ok else 'ISSUES'}\n{msg}".strip())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
