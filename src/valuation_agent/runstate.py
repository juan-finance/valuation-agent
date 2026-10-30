"""Run checkpoints so a quota cut-off becomes a resume, not a restart; also records stage timings for tuning."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

STAGES = ["stage1_data", "stage2_dcf", "stage3_relative", "stage4_recommendation"]
STATUSES = {"pending", "in_progress", "done", "blocked", "provisional"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class RunState:
    """outputs/<ticker>_<date>/run_state.json. Update at every stage boundary and after each major sub-step."""

    def __init__(self, path: str | Path, company: str = "", ticker: str = "", valuation_date: str = "", mode: str = "standard"):
        self.path = Path(path)
        if self.path.exists():
            self.d = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.d = {"company": company, "ticker": ticker, "valuation_date": valuation_date, "mode": mode,
                      "created": _now(), "stages": {s: {"status": "pending", "notes": [], "outputs": [], "next_step": ""} for s in STAGES}}
            self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.d, indent=2, ensure_ascii=False), encoding="utf-8")

    def start(self, stage: str) -> None:
        s = self.d["stages"][stage]
        s["status"], s["started"], s["_t0"] = "in_progress", _now(), time.time()
        self.save()

    def checkpoint(self, stage: str, next_step: str, note: str = "", outputs: list[str] | None = None) -> None:
        s = self.d["stages"][stage]
        s["next_step"] = next_step
        if note:
            s["notes"].append(f"{_now()} {note}")
        for o in outputs or []:
            if o not in s["outputs"]:
                s["outputs"].append(o)
        self.save()

    def finish(self, stage: str, status: str = "done", note: str = "") -> None:
        if status not in STATUSES:
            raise ValueError(status)
        s = self.d["stages"][stage]
        s["status"], s["finished"] = status, _now()
        if "_t0" in s:
            s["elapsed_min"] = round((time.time() - s.pop("_t0")) / 60, 1)
        if note:
            s["notes"].append(f"{_now()} {note}")
        self.save()

    def resume_point(self) -> tuple[str, str] | None:
        """First stage that is not done: (stage, next_step). Read this FIRST in a new session."""
        for st in STAGES:
            s = self.d["stages"][st]
            if s["status"] != "done":
                return st, s.get("next_step", "") or "start of stage"
        return None

    def summary(self) -> str:
        lines = [f"{self.d['company']} ({self.d['ticker']}) valuation date {self.d['valuation_date']} mode {self.d['mode']}"]
        for st in STAGES:
            s = self.d["stages"][st]
            lines.append(f"- {st}: {s['status']}" + (f", {s['elapsed_min']} min" if "elapsed_min" in s else "") +
                         (f" -> next: {s['next_step']}" if s["status"] != "done" and s.get("next_step") else ""))
        return "\n".join(lines)

    def append_run_log(self, csv_path: str | Path) -> int:
        """Append one row per finished stage to memory/run_log.csv (run_id, company, mode, stage, status, elapsed_min,
        finished). Idempotent: a row already present for the same run_id+stage+finished is skipped. Returns rows added.
        Use it to compare a stage with its previous runs and to see where time and quota go."""
        import csv
        path = Path(csv_path)
        header = ["run_id", "company", "mode", "stage", "status", "elapsed_min", "finished"]
        existing = set()
        if path.exists():
            with open(path, newline="", encoding="utf-8") as fh:
                existing = {(r["run_id"], r["stage"], r["finished"]) for r in csv.DictReader(fh)}
        run_id = f"{self.d['ticker']}_{self.d['valuation_date']}"
        new = []
        for st in STAGES:
            s = self.d["stages"][st]
            if "finished" in s and (run_id, st, s["finished"]) not in existing:
                new.append([run_id, self.d["company"], self.d["mode"], st, s["status"], s.get("elapsed_min", ""), s["finished"]])
        if new:
            path.parent.mkdir(parents=True, exist_ok=True)
            fresh = not path.exists()
            with open(path, "a", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                if fresh:
                    w.writerow(header)
                w.writerows(new)
        return len(new)
