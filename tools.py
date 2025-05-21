import json
from pathlib import Path
from typing import Any


def read_data(json_path: Path) -> list[dict[str, Any]]:
    with json_path.open('r', encoding='utf-8') as f:
        content = f.read()

    return json.loads(content)


def write_data(json_path: Path, data: list[dict[str, Any]]) -> None:
    with json_path.open('w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
