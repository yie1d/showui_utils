import base64
import re
import sys
from copy import deepcopy
from io import BytesIO
from pathlib import Path

import pandas as pd
from PIL import Image
from tqdm import tqdm

sys.path.append('/root/autodl-tmp/ShowUI')

from showui_utils.data_preprocess.config import get_path_from_name
from showui_utils.tools import read_data, write_data

DATABASE_NAME = 'GUIAct'


# is instruction English
def is_english_simple(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def read_parquet_to_images(parquet_path: Path, images_path):
    df = pd.read_parquet(parquet_path, engine='pyarrow')

    for file_name, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"parse images"):
        if (images_path / f'{file_name}.png').exists():
            continue
        base64_data = row['base64']
        # 解码Base64数据
        image_data = base64.b64decode(base64_data)
        # 将二进制数据转换为图片对象
        image = Image.open(BytesIO(image_data))
        # 保存图片到指定目录
        image.save(images_path / f'{file_name}.png')


# bbox -> point (str)
def bbox_2_point(bbox, dig=2):
    # bbox: [x1, y1, x2, y2]
    point = [(bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2]
    point = [round(x, 4) for x in point]
    return point


def data_transform(
    state: str,
    split: str,
    images_path: Path,
    metadata_path: Path
):
    print(f'{state}: ')
    read_parquet_to_images(
        metadata_path.parent / f'{state}_{split}_images.parquet', images_path
    )
    guiact_data = read_data(
        metadata_path / f'{state}_{split}_data.json'
    )

    new_data = []
    idx = 0

    task_dict = {}
    for data in tqdm(guiact_data, desc=f'transform {state}'):
        task = data['question']
        img_uid = data['image_id']

        if state == 'web-multi':
            task_id = '_'.join(img_uid.split('_')[:3])

            if task_id not in task_dict:
                task_dict[task_id] = []
            task_history = task_dict[task_id]
            step_history = task_history
        else:
            step_history = []

        if not is_english_simple(task):
            continue

        data_acts = []
        for inx, data_act in enumerate(data['actions_label']):
            action_type = data_act['name'].lower()

            if action_type in ['click', 'input', 'select', 'hover']:
                bbox_str = data_act['element']['related']
                bbox = [float(x) for x in re.findall(r'\d+\.\d+', bbox_str)]
                point = bbox_2_point(bbox)
            elif action_type == 'select_text':
                bbox = None
                point = [
                    [float(x) for x in re.findall(
                        r'\d+\.\d+',
                        data_act['dual_point']['related']['from']
                    )],
                    [float(x) for x in re.findall(
                        r'\d+\.\d+',
                        data_act['dual_point']['related']['to']
                    )]
                ]
            else:
                bbox = None
                point = None

            if action_type in ['input', 'select', 'answer', 'copy']:
                action_value = data_act['text']
            elif action_type == 'scroll':
                down = float(data_act['scroll']['related']['down'])
                right = float(data_act['scroll']['related']['right'])
                if down > 0:
                    action_value = 'down'
                elif down < 0:
                    action_value = 'up'
                elif right > 0:
                    action_value = 'right'
                elif right < 0:
                    action_value = 'left'
                else:
                    action_value = None
            else:
                action_value = None

            if action_value is not None and not is_english_simple(action_value):
                continue
            data_act.update({
                'action_type': action_type,
                'action_value': action_value,
                'point': point
            })
            data_acts.append(data_act)

        task_now = {
            'id': f'guiact_websingle_{idx}',
            'step_id': inx,
            'task': task,
            'thought': data['thoughts'],
            "img_url": img_uid,
            "img_size": [data['image_size']['width'], data['image_size']['height']],

            "action_type": action_type,
            "action_value": action_value,
            "bbox": bbox,
            "point": point,
            "step": data_acts,
            "step_history": step_history,
        }
        new_data.append(deepcopy(task_now))
        idx += 1

        if state == 'web-multi':
            task_cp = deepcopy(task_now)
            task_cp.pop('step_history')
            task_dict[task_id].append(task_cp)
        else:
            step_history.append(data_act)

    write_data(metadata_path / f'hf_{split}_{state}.json', new_data)


def main():
    images_path, metadata_path = get_path_from_name(DATABASE_NAME)
    data_transform(
        'web-single',
        'train',
        images_path,
        metadata_path
    )

    data_transform(
        'web-multi',
        'train',
        images_path,
        metadata_path
    )


if __name__ == '__main__':
    main()
