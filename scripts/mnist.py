import numpy as np
from urllib import request
import gzip
import pickle
from os import path
from torchvision.datasets import MNIST

filename = [
    ["training_images", "train-images-idx3-ubyte.gz"],
    ["test_images", "t10k-images-idx3-ubyte.gz"],
    ["training_labels", "train-labels-idx1-ubyte.gz"],
    ["test_labels", "t10k-labels-idx1-ubyte.gz"]
]


# quick fix for https://github.com/pytorch/vision/issues/1938
# yann.lecun.com server has moved under CloudFlare protection
def download_file(url, filename):
    opener = request.URLopener()
    opener.addheader('User-Agent', 'Mozilla/5.0')
    opener.retrieve(url, filename)


def download_mnist():
    base_url = "https://storage.googleapis.com/cvdf-datasets/mnist/"
    for name in filename:
        print("Downloading " + name[1] + "...")
        download_file(base_url + name[1], name[1])
    print("Download complete.")


def save_mnist():
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            tmp = np.frombuffer(f.read(), np.uint8, offset=16)
            mnist[name[0]] = tmp.reshape(-1, 1, 28, 28).astype(np.float32) / 255
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    with open("mnist.pkl", 'wb') as f:
        pickle.dump(mnist, f)
    print("Save complete.")


def init():
    # Check if already downloaded:
    if path.exists("mnist.pkl"):
        print('Files already downloaded!')
    else:  # Download Dataset
        download_mnist()
        save_mnist()

    new_resources = [
        ('https://storage.googleapis.com/cvdf-datasets/mnist/train-images-idx3-ubyte.gz', prev_mnist_urls[0][1]),
        ('https://storage.googleapis.com/cvdf-datasets/mnist/train-labels-idx1-ubyte.gz', prev_mnist_urls[1][1]),
        ('https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz', prev_mnist_urls[2][1]),
        ('https://storage.googleapis.com/cvdf-datasets/mnist/t10k-labels-idx1-ubyte.gz', prev_mnist_urls[3][1])
    ]
    MNIST.resources = new_resources
    MNIST(path.join('data', 'mnist'), download=True)


def load():
    with open("mnist.pkl", 'rb') as f:
        mnist = pickle.load(f)
    return mnist["training_images"], mnist["training_labels"], \
           mnist["test_images"], mnist["test_labels"]


if __name__ == '__main__':
    init()
