# Collective Knowledge workflows for MLPerf

CK workflows in this repository were originally created by [dividiti Limited](http://dividiti.com) and used to prepare ~50% of all results (~900 out of 1800) submitted to [MLPerf Inference](https://github.com/mlcommons/inference) [v0.5](https://mlperf.org/inference-results-0-5/) and [v0.7](https://mlperf.org/inference-results-0-7/).
These workflows are now being maintained and extended by [Krai Ltd](http://krai.ai).

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


# Table of Contents

- [Installation](#install)
    - [Install CK](#install_ck)
    - [Install CK repos](#install_ck_repos)
    - [Detect Python 3](#install_detect_python3)

- [Image Classification](#image_classification)
    - [Detect ImageNet](#image_classification_imagenet)
    - [Preprocess ImageNet](#image_classification_preprocess)
        - [ResNet50](#image_classification_preprocess_resnet50)
        - [Universal](#image_classification_preprocess_universal)
        - [ResNet50 vs universal](#image_classification_preprocess_resnet50_vs_universal)
    - [Prepare a calibration dataset](#image_classification_cal)
        - [Option 1](#image_classification_cal_option1)
        - [Option 2](#image_classification_cal_option2)

- [Object Detection](#object_detection)
    - [Install COCO](#image_classification_coco)
    - [Preprocess COCO](#object_detection_preprocess)
        - [SSD-ResNet34](#object_detection_preprocess_ssd_resnet34)
        - [SSD-MobileNet-v1](#object_detection_preprocess_ssd_mobilenet_v1)

<a name="install"></a>
# Installation

<a name="install_ck"></a>
## Install [Collective Knowledge](http://cknowledge.org/) (CK)

<pre>&#36; export CK_PYTHON=/usr/bin/python3
&#36; &#36;CK_PYTHON -m pip install --ignore-installed pip setuptools testresources --user
&#36; &#36;CK_PYTHON -m pip install ck --user
&#36; echo 'export PATH=&#36;HOME/.local/bin:&#36;PATH' >> &#36;HOME/.bashrc
&#36; source &#36;HOME/.bashrc
&#36; ck version
V1.55.2
</pre>

**NB:** CK works fine under Python 2, but we are playing safe here (as Python 2 has reached [End-Of-Life](https://www.python.org/doc/sunset-python-2/)).


<a name="install_ck_repos"></a>
## Install CK repositories

<pre>
&#36; ck pull repo --url=https://github.com/krai/ck-mlperf
</pre>


<a name="install_detect_python3"></a>
## Detect (system) Python 3

<pre>
&#36; export CK_PYTHON=/usr/bin/python3
&#36; ck detect soft:compiler.python --full_path=&#36;CK_PYTHON
&#36; ck show env --tags=compiler,python
Env UID:         Target OS: Bits: Name:  Version: Tags:

6dd55d431ea19241   linux-64    64 python 3.8.5    64bits,compiler,host-os-linux-64,lang-python,python,target-os-linux-64,v3,v3.8,v3.8.5
</pre>

**NB:** CK can normally detect available Python interpreters automatically, but we are playing safe here.


## Use generic Linux settings with dummy frequency setting scripts

<pre>&#36; ck detect platform.os --platform_init_uoa=generic-linux-dummy

OS CK UOA:            linux-64 (4258b5fe54828a50)

OS name:              Ubuntu 20.04.1 LTS
Short OS name:        Linux 5.4.0
Long OS name:         Linux-5.4.0-58-generic-x86_64-with-glibc2.29
OS bits:              64
OS ABI:               x86_64

Platform init UOA:    -
</pre>


<a name="image_classification"></a>
# Image Classification

<a name="image_classification_imagenet"></a>
## Detect ImageNet

Unfortunately, the ImageNet 2012 validation dataset (50,000 images) [cannot be freely downloaded](https://github.com/mlcommons/inference/issues/542).
If you have a copy of it e.g. under `/datasets/dataset-imagenet-ilsvrc2012-val/`, you can register it with CK ("detect") as follows:

<pre>
&#36; ck detect soft:dataset.imagenet.val --extra_tags=full \
--full_path=/datasets/dataset-imagenet-ilsvrc2012-val/ILSVRC2012_val_00000001.JPEG
</pre>

<a name="image_classification_preprocess"></a>
## Preprocess ImageNet

The [reference code](https://github.com/mlcommons/inference/blob/master/vision/classification_and_detection/python/dataset.py) uses OpenCV for preprocessing image data.
The minimal [OpenCV Python](https://pypi.org/project/opencv-python/) package can be installed via CK as follows:

<pre>
&#36; ck install package --tags=opencv-python-headless
</pre>

<a name="image_classification_preprocess_resnet50"></a>
### ResNet50

The standard image resolution used for benchmarking ImageNet models is `224x224`. The reference code uses [bilinear interpolation](https://github.com/mlcommons/inference/blob/master/vision/classification_and_detection/python/dataset.py#L154) by default. For ResNet50, however, [area interpolation](https://github.com/mlcommons/inference/blob/master/vision/classification_and_detection/python/dataset.py#L172) is used. In addition, ResNet50 requires [means to be subtracted](https://github.com/mlcommons/inference/blob/master/vision/classification_and_detection/python/dataset.py#L178).

To preprocess ImageNet specifically for ResNet50 (use `--ask` to confirm the destination):

<pre>
&#36; ck install package --tags=dataset,imagenet,preprocessed,using-opencv,full,for-resnet --ask
</pre>

The dataset preprocessed for ResNet50 requires 29G on disk, as pixel components are stored as 32-bit floats:

<pre>
&#36; du -hs $(ck locate env --tags=dataset,imagenet,preprocessed,using-opencv,full,for-resnet)
29G     /home/anton/CK-TOOLS/dataset-imagenet-preprocessed-using-opencv-crop.875-for-resnet-full-side.224-unmutilated
</pre>

<a name="image_classification_preprocess_universal"></a>
### Universal

An alternative method, dubbed universal, uses bilinear interpolation and stores pixels as 8-bit integers. The dataset preprocessed using the alternative method requires 7.1G on disk.
At load time, however, minor additional processing may be required depending on the model (e.g. see sample code for [subtracting means](https://github.com/krai/ck-tensorflow/blob/master/program/image-classification-tflite/benchmark.h#L469) and for [normalizing to the `(-1,+1)` range](https://github.com/krai/ck-tensorflow/blob/master/program/image-classification-tflite/benchmark.h#L463)).

<pre>
&#36; ck install package --tags=dataset,imagenet,preprocessed,using-opencv,full,universal --ask
&#36; du -hs $(ck locate env --tags=dataset,imagenet,preprocessed,using-opencv,full,universal)
7.1G    /home/anton/CK-TOOLS/dataset-imagenet-preprocessed-using-opencv-crop.875-full-inter.linear-side.224-universal-unmutilated
</pre>


<a name="image_classification_preprocess_resnet50_vs_universal"></a>
### ResNet50 vs universal

| Preprocessing method   | OpenCV for ResNet50       | OpenCV universal         |
|-|-|-|
| ResNet50 Top1 accuracy | 0.76456                   | 0.76422                  |
| ResNet50 Top5 accuracy | 0.93016                   | 0.93074                  |
| Matches reference?     | Yes                       | No                       |
| Additional tags        | `using-opencv,for-resnet` | `using-opencv,universal` |
| Supported models       | ResNet50 only             | ResNet50, MobileNet-224  |
| Supported platforms    | x86                       | x86                      |
| Data format            | rgbf32 (float32)          | rgb8 (int8)              |
| Data size              | 29G                       | 7.1G                     |


<a name="image_classification_cal"></a>
## Calibration

<a name="image_classification_cal_option1"></a>
For calibration, MLPerf provides two equivalent sets of 500 images, each randomly selected from the ImageNet validation dataset.

### [Option 1](https://github.com/mlcommons/inference/blob/master/calibration/ImageNet/cal_image_list_option_1.txt) (favoured [by NVIDIA](https://github.com/mlcommons/inference_results_v0.7/blob/master/closed/NVIDIA/data_maps/imagenet/cal_map.txt) and [by Intel](https://github.com/mlcommons/inference_results_v0.7/blob/master/closed/Intel/calibration/OpenVINO/resnet50/imagenet_calibration_list_1.txt))

<pre>
&dollar; ck install package --tags=dataset,imagenet,cal,mlperf.option1 --dep_add_tags.imagenet-val=full
&dollar; ck locate env --tags=dataset,imagenet,cal,mlperf.option1
/home/anton/CK-TOOLS/dataset-imagenet-calibration-mlperf.option1
&dollar; du -hs $(ck locate env --tags=dataset,imagenet,cal,mlperf.option2)
65M	/home/anton/CK-TOOLS/dataset-imagenet-calibration-mlperf.option2
</pre>

<a name="image_classification_cal_option2"></a>
### [Option 2](https://github.com/mlcommons/inference/blob/master/calibration/ImageNet/cal_image_list_option_2.txt)

<pre>
&dollar; ck install package --tags=dataset,imagenet,cal,mlperf.option2 --dep_add_tags.imagenet-val=full
&dollar; ck locate env --tags=dataset,imagenet,cal,mlperf.option2
/home/anton/CK-TOOLS/dataset-imagenet-calibration-mlperf.option2
&dollar; du -hs $(ck locate env --tags=dataset,imagenet,cal,mlperf.option2)
71M	/home/anton/CK-TOOLS/dataset-imagenet-calibration-mlperf.option2
</pre>


<a name="object_detection"></a>
# Object Detection

<a name="object_detection_coco"></a>
## Install COCO

To install the COCO 2017 validation dataset (use `--ask` to confirm the destination):

<pre>
&#36; ck install package --tags=dataset,coco,val,2017 --ask
</pre>


<a name="object_detection_preprocess"></a>
## Preprocess COCO

The [reference code](https://github.com/mlcommons/inference/blob/master/vision/classification_and_detection/python/dataset.py) uses OpenCV for preprocessing image data.
The minimal [OpenCV Python](https://pypi.org/project/opencv-python/) package can be installed via CK as follows:

<pre>
&#36; ck install package --tags=opencv-python-headless
</pre>

<a name="object_detection_preprocess_ssd_resnet34"></a>
### SSD-ResNet34

SSD-ResNet34 requires resizing images to the `1200x1200` resolution:

<pre>
&#36; ck install package --tags=dataset,coco.2017,preprocessed,using-opencv,full,side.1200 --ask
&#36; du -hs $(ck locate env --tags=dataset,coco.2017,preprocessed,using-opencv,full,side.1200
21G     /home/anton/CK-TOOLS/dataset-object-detection-preprocessed-using-opencv-coco.2017-full-side.1200
</pre>

<a name="object_detection_preprocess_ssd_mobilenet_v1"></a>
### SSD-MobileNet-v1

SSD-MobileNet-v1 requires resizing images to the `300x300` resolution:

<pre>
&#36; ck install package --tags=dataset,coco.2017,preprocessed,using-opencv,full,side.300 --ask
&#36; du -hs $(ck locate env --tags=dataset,coco.2017,preprocessed,using-opencv,full,side.300
1.3G    /home/anton/CK-TOOLS/dataset-object-detection-preprocessed-using-opencv-coco.2017-full-side.300
</pre>
