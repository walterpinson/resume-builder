import sys
import tomllib
from pathlib import Path

_ROOT = Path(__file__).parent.parent.parent  # repo root (src/resume_builder/config.py -> src/ -> repo root)


def _find_config() -> Path:
    return _ROOT / "config.toml"


def load() -> dict:
    path = _find_config()
    if not path.exists():
        print(
            f"[error] config.toml not found at {path}\n"
            "Copy config.toml.example to config.toml and fill in your details.",
            file=sys.stderr,
        )
        sys.exit(1)
    with open(path, "rb") as f:
        return tomllib.load(f)


def db_path() -> Path:
    cfg = load()
    p = Path(cfg.get("database", {}).get("path", "db/resume.db"))
    if not p.is_absolute():
        p = _ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def output_dir() -> Path:
    cfg = load()
    p = Path(cfg.get("output", {}).get("directory", "output"))
    if not p.is_absolute():
        p = _ROOT / p
    p.mkdir(parents=True, exist_ok=True)
    return p
