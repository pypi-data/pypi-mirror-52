# tb-paddle
[![Build Status](https://travis-ci.org/linshuliang/tb-paddle.svg?branch=master)](https://travis-ci.org/linshuliang/tb-paddle)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://github.com/linshuliang/tb-paddle/blob/master/README.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 简介

tb-paddle 是一个用于在 TensorBoard 中查看 PaddlePaddle 打点数据的可视化工具。

目前 tb-paddle 支持 SCALARS, HISTOGRAMS, DISTRIBUTIONS, GRAPHS, IMAGES, TEXT,
AUDIO, PROJECTOR,PR CURVES, MESH, CUSTOM SCALARS 这11个栏目的功能。

|栏目|展示图表|作用|
|:----:|:---:|:---|
|[SCALARS](instructions/SCALARS_instructions.md)|折线图|显示损失函数值、准确率等标量数据|
|[HISTOGRAMS, DISTRIBUTIONS](instructions/HISTOGRAMS_DISTRIBUTIONS_instructions.md)|分布图|显示行向量数据的数值分布与变化趋势，便于查看权重矩阵、偏置项、梯度等参数的变化|
|[GRAPHS](instructions/GRAPHS_instructions.md)|计算图|显示神经网络的模型结构|
|[IMAGES](instructions/IMAGES_instructions.md)|图片和视频|显示图片和视频|
|[AUDIO](instructions/AUDIO_instructions.md)|音频|播放音频|
|[TEXT](instructions/TEXT_instructions.md)|文本|显示文本|
|[PROJECTOR](instructions/PROJECTOR_instructions.md)|交互式的嵌入可视化|通过降维方法将高维数据嵌入到 2D/3D 中显示，支持 PCA, t-SNE, UMAP, CUSTOM 这四种降维方法|
|[PR CURVES](instructions/PR-CURVES_instructions.md)|Precision-Recall曲线|根据预测的概率值及其对应的准确答案计算[Precision-Recall](https://en.wikipedia.org/wiki/Precision_and_recall) 曲线|
|[MESH](instructions/MESH_instructions.md)|网格和点云|显示3D图形的网格和点云(Meshes and points cloud)|
|[CUSTOM SCALARS](instructions/CUSTOM_SCALARS_instructions.md)|组合折线图|显示用户自定义组合的折线图|

上面表格中的链接为各个栏目的使用说明。
此处提供了mnist手写体识别的[示例程序](API_demo/mnist_log-demo.py)，
以帮助快速上手和体验。

## 安装

```
# 需要先安装 paddlepaddle，无须安装 TensorFlow

# 必须安装 tb-nightly >= 1.15.0a20190818，否则页面无法自动刷新
pip install tb-nightly

# 安装 tb-paddle
pip install tb-paddle
```

## 创建 SummaryWriter 类的对象

使用 tb-paddle，首先得创建类`SummaryWriter`的对象，然后才能调用对象的成员函数来添加打点数据。

创建 [class SummaryWriter](tb_paddle/writer.py#L177) 的初始化函数的定义：

```python
def __init__(self, logdir=None, max_queue=1024, comment='', filename_suffix='', **kwargs):
```

其中各个参数的含义为：

* `logdir` ：指定日志文件的存放路径，如果指定路径中没有 tfevents 文件，就新建一个 tfevents 文件，否则会向已有的 tfevents 文件中写数据。`logdir`的实参可以为`None`，存放路径将设为`./runs/DATETIME_HOSTNAME/`；
* `max_queue` ： 缓冲区队列的最大长度；
* `comment` ：如果`logdir`为`None`，则在默认存放路径中添加后缀。如果`logdir`不是`None`，那么该参数没有任何作用；
* `filename_suffix` ：event 文件名后缀；

## TensorBoard 启动命令

启动 TensorBoard 服务的命令为`tensorboard`，输入 `tensorboard --helpful` 则可查看此命令的帮助文档。

启动 TensorBoard 服务，选项`--logdir`是必须的，通常还会使用选项`--host`指定IP地址, 选项`--port`指定可用端口：

```
tensorboard --logdir <path/to/dir> --host <host_IP> --port <port_num>
```

这几个选项的详细解释:

1. `--logdir`

`--logdir` 用于指定 `tfevents` 文件的存放路径，可以同时指定多个目录，比如：

```
tensorboard --logdir ExperimentA:path/to/A_dir,ExperimentB:another/path/to/B_dir
```

只需在不同目录名间加上逗号(`,`) ，则可同时指定多个目录。

事实上，TensorBoard 会自动检查指定目录下的所有子目录中的 `tfevents` 文件，并在前端网页中
按 `Runs` 分类，比如目录结构为：

```
log
|
|____log_mnist
|    |
|    |___logtest
|    |
|    |___logtrain
|   
|____paddle_log
```

则在 TensorBoard 前端页面的左侧栏中显示为：

<p align="center">
<img src="./screenshots/tensorboard_manuals/Runs.png" width=300><br/>
图1. TensorBoard Runs 选项 - 按目录分类 <br/>

2. `--host`

机器的IP地址，单机运行时，指定为 `--host 0.0.0.0`。

3. `--port`

可访问的端口。单机运行时，指定为`--port 6***`； 在服务器上运行时，指定为`--port 8***`。

## 特别致谢

tb-paddle 是在 [tensorboardX](https://github.com/lanpa/tensorboardX) 的基础上修改的，
tb-paddle 的框架和 API 接口均沿用了 tensorboardX。与 tensorboardX 不同的是，
tb-paddle 的API接口的参数类型为`numpy.ndarray`和Python基本数据类型，
并根据 Paddle 框架重新实现了GRAPHS栏目的计算图显示。
此处由衷感谢[Tzu-Wei Huang](https://github.com/lanpa)的开源贡献。
