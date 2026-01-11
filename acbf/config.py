"""Configuration loading for ACBF."""

from __future__ import annotations

import dataclasses
import os
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG_DIR = Path(__file__).resolve().parents[1] / "config"


@dataclasses.dataclass(frozen=True)
class BlockchainConfig:
    difficulty: int = 3
    mining_reward: int = 50
    chain_id: str = "acbf-local"


@dataclasses.dataclass(frozen=True)
class BackendConfig:
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = False


@dataclasses.dataclass(frozen=True)
class FrontendConfig:
    port: int = 3000


@dataclasses.dataclass(frozen=True)
class AppConfig:
    blockchain: BlockchainConfig
    backend: BackendConfig
    frontend: FrontendConfig


def _parse_value(value: str) -> Any:
    value = value.strip().strip("\"")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        return value


def _parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Parse a minimal subset of YAML used in ACBF config files."""

    data: Dict[str, Any] = {}
    current_section: Optional[str] = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if raw_line.startswith("  ") and current_section:
            key, _, value = line.partition(":")
            data.setdefault(current_section, {})[key.strip()] = _parse_value(value)
        else:
            key, _, value = line.partition(":")
            if value.strip():
                data[key.strip()] = _parse_value(value)
                current_section = None
            else:
                current_section = key.strip()
                data[current_section] = {}
    return data


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    return _parse_simple_yaml(text)


def _env_override(value: Any, env_key: str, cast_type: Optional[type] = None) -> Any:
    env_value = os.getenv(env_key)
    if env_value is None:
        return value
    if cast_type:
        return cast_type(env_value)
    return env_value


def load_config(config_dir: Optional[Path] = None) -> AppConfig:
    """Load configuration from YAML files and environment variables."""

    config_dir = config_dir or DEFAULT_CONFIG_DIR
    blockchain_raw = _load_yaml(config_dir / "blockchain_config.yaml")
    dapp_raw = _load_yaml(config_dir / "dapp_config.yaml")

    blockchain = BlockchainConfig(
        difficulty=int(blockchain_raw.get("difficulty", 3)),
        mining_reward=int(blockchain_raw.get("mining_reward", 50)),
        chain_id=str(blockchain_raw.get("chain_id", "acbf-local")),
    )
    backend_raw = dapp_raw.get("backend", {})
    frontend_raw = dapp_raw.get("frontend", {})

    backend = BackendConfig(
        host=_env_override(backend_raw.get("host", "127.0.0.1"), "ACBF_BACKEND_HOST"),
        port=_env_override(backend_raw.get("port", 5000), "ACBF_BACKEND_PORT", int),
        debug=bool(
            str(_env_override(backend_raw.get("debug", False), "ACBF_BACKEND_DEBUG")).lower()
            in {"1", "true", "yes"}
        ),
    )
    frontend = FrontendConfig(
        port=_env_override(frontend_raw.get("port", 3000), "ACBF_FRONTEND_PORT", int)
    )

    return AppConfig(blockchain=blockchain, backend=backend, frontend=frontend)
