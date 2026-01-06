from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re


class UCIError(RuntimeError):
    pass


@dataclass
class UCIGo:
    movetime_ms: int | None = None
    depth: int | None = None
    nodes: int | None = None

    def to_cmd(self) -> str:
        parts: list[str] = ["go"]
        if self.movetime_ms is not None:
            parts += ["movetime", str(self.movetime_ms)]
        if self.depth is not None:
            parts += ["depth", str(self.depth)]
        if self.nodes is not None:
            parts += ["nodes", str(self.nodes)]
        if len(parts) == 1:
            parts += ["movetime", "250"]
        return " ".join(parts)


class UCIEngine:
    def __init__(self, path: str, uci_options: dict[str, Any] | None = None):
        self.path = path
        self.uci_options = uci_options or {}
        self._p: subprocess.Popen[str] | None = None

    def __enter__(self) -> "UCIEngine":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

    def start(self) -> None:
        if self._p is not None:
            return
        self._p = subprocess.Popen(
            [self.path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        self._send("uci")
        self._wait_for("uciok", timeout_s=5.0)

        for name, value in self.uci_options.items():
            self._send(f"setoption name {name} value {value}")

        self._send("isready")
        self._wait_for("readyok", timeout_s=5.0)

    def stop(self) -> None:
        if self._p is None:
            return
        try:
            self._send("quit")
        finally:
            try:
                self._p.kill()
            except Exception:
                pass
            self._p = None

    def bestmove_from_fen(self, fen: str, go: UCIGo) -> str:
        self._send(f"position fen {fen}")
        self._send(go.to_cmd())
        line = self._wait_for_prefix("bestmove ", timeout_s=30.0)
        # bestmove e2e4 [ponder e7e5]
        parts = line.split()
        if len(parts) < 2:
            raise UCIError(f"Malformed bestmove line: {line!r}")
        return parts[1].strip()

    def analyze_from_fen(self, fen: str, go: UCIGo) -> dict[str, Any]:
        """
        Returns a dict with:
          - bestmove (uci)
          - score (e.g. "cp 34" or "mate 3") if seen
          - pv (string) if seen
        """
        self._send(f"position fen {fen}")
        self._send(go.to_cmd())

        last_score: str | None = None
        last_pv: str | None = None

        # Examples:
        #  "info depth 10 score cp 34 pv ..."
        #  "info depth 12 score mate 3 pv ..."
        #  "info ... score cp -120 upperbound pv ..."
        score_re = re.compile(r"\bscore\s+(cp\s+-?\d+|mate\s+-?\d+)(?:\s+(?:lowerbound|upperbound))?")
        pv_re = re.compile(r"\bpv\s+(.+)$")

        deadline = time.time() + 30.0
        while time.time() < deadline:
            line = self._readline()
            if line.startswith("info "):
                m = score_re.search(line)
                if m:
                    last_score = m.group(1)
                m = pv_re.search(line)
                if m:
                    last_pv = m.group(1).strip()
                continue
            if line.startswith("bestmove "):
                parts = line.split()
                if len(parts) < 2:
                    raise UCIError(f"Malformed bestmove line: {line!r}")
                return {"bestmove": parts[1].strip(), "score": last_score, "pv": last_pv}

        raise UCIError("Timed out waiting for bestmove during analysis")

    def _send(self, cmd: str) -> None:
        if self._p is None or self._p.stdin is None:
            raise UCIError("Engine process not started")
        self._p.stdin.write(cmd + "\n")
        self._p.stdin.flush()

    def _readline(self) -> str:
        if self._p is None or self._p.stdout is None:
            raise UCIError("Engine process not started")
        line = self._p.stdout.readline()
        if line == "":
            raise UCIError("Engine stdout closed unexpectedly")
        return line.strip()

    def _wait_for(self, token: str, timeout_s: float) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            line = self._readline()
            if line == token:
                return
        raise UCIError(f"Timed out waiting for {token!r}")

    def _wait_for_prefix(self, prefix: str, timeout_s: float) -> str:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            line = self._readline()
            if line.startswith(prefix):
                return line
        raise UCIError(f"Timed out waiting for prefix {prefix!r}")


def load_engine_config(config_path: str) -> tuple[str, dict[str, Any], UCIGo]:
    p = Path(config_path)
    if not p.exists():
        raise FileNotFoundError(
            f"Missing engine config at {config_path!r}. "
            "Create it by copying config/engine.example.json to config/engine.json."
        )
    data = json.loads(p.read_text())
    eng = data.get("engine", {})
    path = eng.get("path")
    if not path:
        raise UCIError("engine.path missing in config")
    uci_options = eng.get("uci_options", {}) or {}
    go_cfg = eng.get("go", {}) or {}
    go = UCIGo(
        movetime_ms=go_cfg.get("movetime_ms"),
        depth=go_cfg.get("depth"),
        nodes=go_cfg.get("nodes"),
    )
    return path, uci_options, go


