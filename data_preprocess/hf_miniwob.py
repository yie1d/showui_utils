
import sys

from PIL import Image

sys.path.append('/root/autodl-tmp/ShowUI')
from showui_utils.data_preprocess.config import get_path_from_name
from showui_utils.tools import read_data, write_data

DATABASE_NAME = 'MiniWob'


def normalize_bbox(bbox, size):
    x1, y1, x2, y2 = bbox
    width, height = size

    x1_norm = x1 / width
    y1_norm = y1 / height
    x2_norm = x2 / width
    y2_norm = y2 / height
    return [x1_norm, y1_norm, x2_norm, y2_norm]


def main():
    images_path, metadata_path = get_path_from_name(DATABASE_NAME)

    miniwob_data_train = read_data(metadata_path / 'miniwob_data_train.json')

    new_data = []
    ids = 0
    for scenario, scenario_data in miniwob_data_train.items():
        for episode in scenario_data:
            step_history = []
            step_inx = 0
            for step in episode:
                filename = step['img_filename']
                img_path = images_path / filename
                goal = step['goal']

                if img_path.exists() is False:
                    continue
                image = Image.open(img_path)

                if step['action_type'] == 'click':
                    action_meta = normalize_bbox(step['bbox'], image.size)
                elif step['action_type'] == 'type':
                    action_meta = step['typed_text']
                else:
                    continue

                tmp_step = {
                    "img_url": filename,
                    "action_type": step['action_type'],
                    "action_meta": action_meta,
                }
                new_data.append({
                    "split": scenario,
                    "id": f"miniwob_{ids}",

                    "task": goal,
                    "img_url": filename,
                    "img_size": image.size,

                    "action_type": step['action_type'],
                    "action_meta": action_meta,

                    "step_id": step_inx,
                    "step": tmp_step,
                    "step_history": step_history.copy(),
                })

                step_history.append(tmp_step)
                ids += 1
                step_inx += 1

    write_data(metadata_path / 'hf_train.json', new_data)


if __name__ == '__main__':
    main()
