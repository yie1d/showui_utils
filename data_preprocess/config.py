from pathlib import Path

DATABASE_PATH = Path('/root/autodl-tmp/gui_database')


def get_path_from_name(database_name: str) -> tuple[Path, Path]:
    database_path = DATABASE_PATH / database_name
    images_path = database_path / 'images'
    metadata_path = database_path / 'metadata'

    return images_path, metadata_path
