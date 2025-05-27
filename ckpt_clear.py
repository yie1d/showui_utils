import shutil
import time
from pathlib import Path

CKPT_MODEL_PATH = Path('/root/autodl-tmp/ShowUI/train_save/debug/2025-05-27_09-40-58/ckpt_model/')


def clear():
    with open(CKPT_MODEL_PATH / 'latest', 'r') as f:
        latest_ckpt = f.read()

    latest_step = int(latest_ckpt.removeprefix('global_step'))

    for global_step_dir in CKPT_MODEL_PATH.glob('global_step*'):
        if global_step_dir.is_dir():
            cur_step = int(global_step_dir.name.removeprefix('global_step'))
            if cur_step < latest_step or cur_step - latest_step > 600:
                try:
                    shutil.rmtree(global_step_dir)
                    print(f'remove success:\n\tlatest_step: {latest_step}, cur_step: {cur_step}, remove {global_step_dir}')
                except:
                    print(f'remove error:\n\tlatest_step: {latest_step}, cur_step: {cur_step}, remove {global_step_dir}')


if __name__ == '__main__':
    while True:
        try:
            clear()
        except Exception as e:
            pass
        time.sleep(60 * 10)


