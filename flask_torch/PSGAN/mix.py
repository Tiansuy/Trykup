import argparse
import io
import cv2
from pathlib import Path

from PIL import Image
from fire import Fire
import numpy as np
from matplotlib import pyplot as plt


def mix(args,inference,postprocess,source_path,reference_path,save_path):
    source = Image.open(source_path).convert("RGB")
    reference = Image.open(reference_path).convert("RGB")

    # Transfer the psgan from reference to source.
    image, face = inference.transfer(source, reference, with_face=True)
    source_crop = source.crop((face.left(), face.top(), face.right(), face.bottom()))
    image = postprocess(source_crop, image)
    for single_save_path in save_path:
        image.save(single_save_path)

    if args.speed:
        import time
        start = time.time()
        for _ in range(100):
            inference.transfer(source, reference)
        print("Time cost for 100 iters: ", time.time() - start)



def img_merge(img_list,labels):
    fig = plt.figure()
    for i in range(len(img_list)):
        t = 131+i
        plt.subplot(t)
        img = cv2.imread(img_list[i])
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img)
        plt.title(labels[i])
        plt.xticks([])
        plt.yticks([])
    plt.savefig('static/result.jpg')
    # plt.show()


def makeup_transfer2(args,inference,postprocess,source_path,reference_path,save_path):
    mix(args,inference,postprocess,source_path,reference_path,save_path)
    img_list=[source_path,reference_path,save_path[0]]
    labels=['source','reference','result']
    img_merge(img_list,labels)