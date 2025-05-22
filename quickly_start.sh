#!/bin/bash

# 设置默认路径
DATABASE_DIR=""
WEIGHT_DIR=""

# 解析命令行参数
while [ "$#" -gt 0 ]; do
    case "$1" in
        --database)
            DATABASE_DIR="$2"
            shift 2  # 跳过两个参数：--database 和它的值
            ;;
        --weight)
            WEIGHT_DIR="$2"
            shift 2  # 跳过两个参数：--weight 和它的值
            ;;
        *)
            echo "Unknown parameter: $1"
            echo "Usage: $0 [--database <database_dir>] [--weight <weight_dir>]"
            exit 1
            ;;
    esac
done
export HF_ENDPOINT=https://hf-mirror.com

echo "*******************************************************"
echo "Using database directory: $DATABASE_DIR"
echo "Using weight directory: $WEIGHT_DIR"

echo "*******************************************************"
# 下载数据库
echo "******************01 download database******************"
echo "------------>start ShowUI-desktop"
echo "./hfd.sh showlab/ShowUI-desktop --dataset --local-dir ${DATABASE_DIR}/ShowUI-desktop"
./hfd.sh showlab/ShowUI-desktop --dataset --local-dir ${DATABASE_DIR}/ShowUI-desktop --tool aria2c -x 10

echo "------------>start ShowUI-web"
echo "./hfd.sh showlab/ShowUI-web --dataset --local-dir ${DATABASE_DIR}/ShowUI-web"

./hfd.sh showlab/ShowUI-web --dataset --local-dir ${DATABASE_DIR}/ShowUI-web --tool aria2c -x 10

# 等待 ShowUI-web 下载完成
echo "------------>start unzip ShowUI-web"
tar -xzf ${DATABASE_DIR}/ShowUI-web/images.tar.gz -C ${DATABASE_DIR}/ShowUI-web &

echo "------------>start ScreenSpot"
echo "./hfd.sh KevinQHLin/ScreenSpot --dataset --local-dir ${DATABASE_DIR}/ScreenSpot"

./hfd.sh KevinQHLin/ScreenSpot --dataset --local-dir ${DATABASE_DIR}/ScreenSpot --tool aria2c -x 10

echo "------------>start GUIAct"
echo "./hfd.sh yiye2023/GUIAct --dataset --local-dir ${DATABASE_DIR}/GUIAct"

./hfd.sh KevinQHLin/ScreenSpot --dataset --local-dir ${DATABASE_DIR}/ScreenSpot --tool aria2c -x 10

# 下载权重
echo "******************02 download weight******************"
echo "------------>start Qwen2.5-VL-7B-Instruct"
echo "./hfd.sh Qwen/Qwen2.5-VL-7B-Instruct --local-dir ${WEIGHT_DIR}/Qwen2.5-VL-7B-Instruct"
./hfd.sh Qwen/Qwen2.5-VL-7B-Instruct --local-dir ${WEIGHT_DIR}/Qwen2.5-VL-7B-Instruct --tool aria2c -x 10

echo "------------>end Qwen2.5-VL-7B-Instruct"


wait $!
echo "All tasks completed successfully"