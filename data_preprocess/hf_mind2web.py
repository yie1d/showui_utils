import sys
from pathlib import Path

from PIL import Image
from tqdm import tqdm

sys.path.append('/root/autodl-tmp/ShowUI')
from showui_utils.data_preprocess.config import get_path_from_name
from showui_utils.tools import read_data, write_data

DATABASE_NAME = 'Mind2Web'


def data_transform(version: str, images_path: Path, metadata_path: Path):
    mind2web_data = read_data(metadata_path / f'mind2web_data_{version}.json')

    new_data = []
    idx = 0

    for episode in tqdm(mind2web_data):
        annot_id = episode["annotation_id"]
        confirmed_task = episode["confirmed_task"]

        step_history = []
        repr_history = []
        for i, (step, step_repr) in enumerate(zip(
            episode["actions"], episode["action_reprs"]
        )):
            filename = f'{annot_id}-{step["action_uid"]}.jpg'
            img_path = images_path / filename

            if img_path.exists() is False:
                continue

            image = Image.open(img_path)

            new_data.append({
                "split": version,
                "id": f"mind2web_{idx}",
                "annot_id": annot_id,
                "action_uid": step["action_uid"],

                "website": episode["website"],
                "domain": episode["domain"],
                "subdomain": episode["subdomain"],

                "task": confirmed_task,
                "img_url": filename,
                "img_size": image.size,

                "idxd": i,
                "step": step,
                "step_repr": step_repr,
                "step_history": step_history.copy(),
                "repr_history": repr_history.copy()
            })

            step_history.append(step)
            repr_history.append(step_repr)

            idx += 1

    write_data(metadata_path / f'hf_{version}.json', new_data)
    return new_data


def main():
    images_path, metadata_path = get_path_from_name(DATABASE_NAME)

    data_transform(
        version='train',
        images_path=images_path,
        metadata_path=metadata_path
    )

    test_full = []
    for version in ['test_task', 'test_domain', 'test_website']:
        test_full.extend(data_transform(
            version=version,
            images_path=images_path,
            metadata_path=metadata_path
        ))

    write_data(metadata_path / 'hf_test_full.json', test_full)


if __name__ == '__main__':
    main()
