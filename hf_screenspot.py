from pathlib import Path

from .tools import read_data, write_data


def main():
    database_path = Path(__file__).parent.parent.parent.joinpath('gui_database').resolve()

    database_name = 'ScreenSpot'

    database_path = database_path.joinpath(database_name)
    json_path = database_path / 'metadata' / 'hf_test_full.json'

    metadata = read_data(json_path)

    after_data = []
    for data in metadata:
        if data['split'] != 'mobile':
            after_data.append(data)

    write_data(json_path, after_data)


if __name__ == '__main__':
    main()
