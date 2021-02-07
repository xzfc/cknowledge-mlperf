# Collective Knowledge workflows for MLPerf

*This fork is maintained by [Krai Ltd](https://krai.ai).*

[![compatibility](https://github.com/ctuning/ck-guide-images/blob/master/ck-compatible.svg)](https://github.com/ctuning/ck)
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Linux/MacOS: [![Travis Build Status](https://travis-ci.org/ctuning/ck-mlperf.svg?branch=master)](https://travis-ci.org/ctuning/ck-mlperf)

# Table of Contents
- [Installation](#install)
    - [Install CK](#install_ck)
    - [Install CK repos](#install_ck_repos)
- [Image Classification](#image_classification)

<a name="install"></a>
# Installation

<a name="install_ck"></a>
## Install [Collective Knowledge](http://cknowledge.org/) (CK)

<pre>&#36; export CK_PYTHON=/usr/bin/python3
&#36; &#36;CK_PYTHON -m pip install --ignore-installed pip setuptools testresources --user
&#36; &#36;CK_PYTHON -m pip install ck
&#36; echo 'export PATH=&#36;HOME/.local/bin:&#36;PATH' >> &#36;HOME/.bashrc
&#36; source &#36;HOME/.bashrc
&#36; ck version
V1.55.2
</pre>


<a name="install_ck_repos"></a>
## Install CK repositories

### Install public repositories

<pre>
&#36; ck pull repo --url=https://github.com/krai/ck-mlperf
</pre>


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

<a name="detect_python"></a>
## Detect (system) Python

<pre>
&#36; export CK_PYTHON=/usr/bin/python3
&#36; ck detect soft:compiler.python --full_path=&#36;CK_PYTHON
&#36; ck show env --tags=compiler,python
Env UID:         Target OS: Bits: Name:  Version: Tags:

6dd55d431ea19241   linux-64    64 python 3.8.5    64bits,compiler,host-os-linux-64,lang-python,python,target-os-linux-64,v3,v3.8,v3.8.5
</pre>

**NB:** CK can normally detect available Python interpreters automatically, but we are playing safe here.


<a name="image classification"></a>
# Image Classification

