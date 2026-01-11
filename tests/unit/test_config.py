from pathlib import Path

from acbf.config import load_config, BlockchainConfig


def test_load_config_defaults(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "blockchain_config.yaml").write_text("difficulty: 2\nmining_reward: 10\n")
    (config_dir / "dapp_config.yaml").write_text("backend:\n  port: 9000\n")

    config = load_config(config_dir)
    assert config.blockchain.difficulty == 2
    assert config.blockchain.mining_reward == 10
    assert config.backend.port == 9000
