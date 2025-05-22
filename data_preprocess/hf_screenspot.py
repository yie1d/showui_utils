import sys

sys.path.append('/root/autodl-tmp/ShowUI')

from showui_utils.data_preprocess.config import get_path_from_name
from showui_utils.tools import read_data, write_data

DATABASE_NAME = 'ScreenSpot'


def main():
    images_path, metadata_path = get_path_from_name(DATABASE_NAME)

    json_path = metadata_path / 'hf_test_full.json'

    (metadata_path / 'screenspot_mobile.json').unlink(missing_ok=True)

    metadata = read_data(json_path)

    new_data = []
    for data in metadata:
        if data['split'] != 'mobile':
            new_data.append(data)
        else:
            images_path.joinpath(data['img_url']).unlink(missing_ok=True)

    write_data(json_path, new_data)


if __name__ == '__main__':
    main()
