# Flowers Azure ML

You have to implement **an image classification neural network** for the [FLOWERS dataset](https://drive.google.com/file/d/1OxuNIvlJ6FLWtS5POvJv54Dm0Gj8wqAv/view?usp=sharing). Feel free to reduce the number of examples for each class in your dataset if training on your hardware takes too much time.

For this task, you should make at least **two neural networks**: a fully connected one that works on top of some extracted classic features/descriptors (histograms, Gabor, HOG, etc.) and a convolutional one with class prediction at the end. In the code you can propose a few alternative architectures and pick the best among them.

You can do it either in Keras or Pytorch. It's better to do both.

As an **output**, you should provide your **code, trained model files** (2 pcs. at least), and a brief report with standard **metrics** for classifiers (confusion matrix, precision, recall, F1 score) [calculated on test images].

Your code should provide **3 execution modes/functions: train** (for training new model), **test** (for testing the trained and saved model on the test dataset), and **infer** (for inference on a particular folder with images or a single image).

## Project structure

```
02-problem
│   README.md
│   .gitignore
│
└───data (contains train/val/test data)
│   └───daisy
│       │   5547758_eea9edfd54_n.jpg
│       │   5673551_01d1ea993e_n.jpg
│       │   ...
│   └───...
│       │   ...
│   
└───output (contains best models and training logs)
│   └───models
│       │   FlowersConvModel_model_best.pth
│       │   FlowersFcModel_model_best.pth
│       │   ...
│   └───tensorboard_logs
│       └───FlowersConvModel
│           │   ...
│       └───FlowersFcModel
│           │   ...
└───src (contains source code and notebooks with report)
│   config.py
│   01-fc-model-run.ipynb
│   02-conv-model-run.ipynb
│
│   └───datasets
│       │   __init__.py
│       │   flowers_dataset.py
│       │   preprocessing.py
│   └───models
│       │   __init__.py
│       │   model_conv.py
│       │   model_fc.py
│   └───utils
│       │   __init__.py
│       │   functions.py
│       │   loops.py
│       │   meters.py
```
