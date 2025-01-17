# Condensed Movies Challenge 

This repository contains the code and details for the data download, baseline model, and evaluation for Condensed Movie Challenge. Official Repository is present at 
https://github.com/m-bain/CondensedMovies 


## Dataset Overview

Here, we provide an overview and detail for the downloaded dataset. For more information on the following features in the dataset, including details architectures and datsets, see [here](https://www.robots.ox.ac.uk/~vgg/research/condensed-movies/features.html "here"). Below is an overview of the dataset tree structure with details:

```

├── features
│   ├── pred_audio
│   │      └── vggish   (audio features)
│   ├── pred_i3d_25fps_256px_stride8_offset0_inner_stride1
│   │      └── i3d  (action features)
│   ├── pred_imagenet_25fps_256px_stride25_offset0
│   │      └── resnext101_32x48d  (Instagram Hashtags, fine-tuned on ImageNet features)
│   │      └── senet154  (ImageNet features)
│   ├── pred_r2p1d_30fps_256px_stride16_offset0_inner_stride1
│   │      └── r2p1d-ig65m  (Instagram 65m, fine-tuned on Kinetics)
│   └── pred_scene_25fps_256px_stride25_offset0
│   │      └── densenet161  (scene features)
│   └── pred_subs
│   │      └── bert-base-uncased_line  (BERT subtitle features)
├── metadata
│   ├── subs_test.json (raw text subtitle files for the test set)
│   ├── subs_train_val.json (raw text subtitle files for the train/val set)
│   ├── test_challf0.csv (raw text descriptions for the test set)
│   └── train_val_challf0.csv (raw text descriptions for the train/val set)

```

Below is an overview for the dataset tree structure within a specific feature directory. The features from the train/val videos are further subaranged by year (i.e. 2011 -> 2019 directories). The features from the test videos are found in the 'test' directory.

```

└── vggish 
    ├── 2011 
        ├── sBjNpZ5t9S4.npy
        ├── SBLMTDMdTIU.npy
        ├── SbTWLdT_tgk.npy
        ├── ...
    ├── 2012 
        ├── ...
    ├── 2013
        ├── ...
    ├── 2014
        ├── ...
    ├── 2015
        ├── ...
    ├── 2016
        ├── ...
    ├── 2017
        ├── ...
    ├── 2018
        ├── ...
    ├── 2019
        ├── ...
    └── test (the features for the test videos)
        ├── 1061.npy
        ├── 1062.npy
        ├── 1063.npy
        ├── ...
```


**Train/Val/Test Splits:** the splits are contained in and read from the text description csv files (e.g. metadata/train_val_challf0.csv & metadata/test_challf0.csv)


## Training and Evaluation

### 📝 Preparation 

Create conda env `conda env create -f requirements/environment.yaml` (assumes CUDA 11.1, adjust if needed).

Experiment checkpoints / dataset saves to `exps` by default, can become large in size, set up symlink if you want to store elsewhere.

### 🏋️‍️ Baseline Training

`python train.py --config configs/baseline.json`

Adjust batch_size, n_gpu, exp_name in the config file accordingly.

### 🏁 Evaluation

#### Validation Check
Evaluate on val set `python test.py --resume exps/models/{EXP_NAME}/{TIMESTAMP}/model_best.pth --split val`

#### Test Submission
Evaluate on test set `python test.py --resume exps/models/{EXP_NAME}/{TIMESTAMP}/model_best.pth --split test`

Similarity matrix should be zipped at `exps/models/{EXP_NAME}/{TIMESTAMP}/submission.zip`.


