_SAVE_DIR="/root/autodl-tmp/ShowUI/train_save"
exp_id="debug"


exp_dir="$_SAVE_DIR/$exp_id/2025-05-22_13-36-39"
showui_dir=$(pwd)
ckpt_dir="${exp_dir}/ckpt_model/"
merge_dir="${ckpt_dir}/merged_model"

cd "$ckpt_dir" || { echo "Failed to cd to $ckpt_dir"; exit 1; }
python zero_to_fp32.py . pytorch_model.bin
mkdir -p merged_model

cd "$showui_dir"
python3 merge_weight.py --exp_dir="$exp_dir"

echo "$merge_dir"