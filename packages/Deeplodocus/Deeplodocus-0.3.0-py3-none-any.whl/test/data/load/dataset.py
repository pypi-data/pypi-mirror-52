from deeplodocus.utils.namespace import Namespace
from deeplodocus.data.load.dataset import Dataset
import time
import torchvision
import torch

NUM_ITEMS = 50

nsp = Namespace("dataset.yaml")

nsp.add({"transform_manager": None}, "dataset")
nsp.summary()

dataset = Dataset(**nsp.dataset.get())

t0 = time.time()
for i in range(NUM_ITEMS):
    a = dataset.__getitem__(i)
    print(a)
    if i == 10:
        b = a
time1 = time.time() - t0


mnist = torchvision.datasets.MNIST(root="./MNIST")

t0 = time.time()
for i in range(NUM_ITEMS):
    a = mnist.__getitem__(i)
    if i == 10:
        c = a

time2 = time.time() - t0
#print(b)
#print(c)
#print(time1)
#print(time2)

#print(time1 / time2)