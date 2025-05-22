## 1 base

### 1.1 下载aria2
```shell
sudo apt-get update
sudo apt-get install aria2 
```

### 1.2 修改执行权限
```shell
chmod +x hfd.sh
chmod +x quickly_start.sh
```

## 2 执行`quickly_start.sh`下载数据集及权重
### 2.1 运行autodl的代理
```shell
source /etc/network_turbo
```
### 2.2 执行下载
```shell
# ./quickly_start.sh --database /root/autodl-tmp/gui_database --weight /root/autodl-tmp/ShowUI/model_weight

sh quickly_start.sh --database <database_dir> --weight <weight_dir>>
```


## 3 清理、转换原始数据集
**运行前需要修改data_preprocess中的对应路径**
运行所有hf_开头的脚本对数据进行预处理
```shell
python showui_utils/data_preprocess/hf_*...
```

