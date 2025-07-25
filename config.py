import json
import logging
from pathlib import Path

CONFIG_PATH = Path('config.json')
logger = logging.getLogger(__name__)


def load_config(path: Path = CONFIG_PATH) -> dict:
    if not path.exists():
        logger.info("Config file %s not found, creating default", path)
        return {"schedule_cron": "0 9 * * *", "queries": []}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(config: dict, path: Path = CONFIG_PATH) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    logger.info("Saved config to %s", path)
