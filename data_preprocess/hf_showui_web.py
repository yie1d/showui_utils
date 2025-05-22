import sys

sys.path.append('/root/autodl-tmp/ShowUI')

from showui_utils.data_preprocess.config import get_path_from_name
from showui_utils.tools import read_data, write_data

DATABASE_NAME = 'ShowUI-web'


def main():
    images_path, metadata_path = get_path_from_name(DATABASE_NAME)

    json_path = metadata_path / 'hf_train.json'

    metadata = read_data(json_path)

    new_data = []
    for data in metadata:
        data['img_url'] = data['img_url'].replace('/blob/v-lqinghong/data/GUI_database/GUI_Exp_Web//images', images_path.as_posix())
        new_data.append(data)

    write_data(json_path, new_data)


if __name__ == '__main__':
    main()
