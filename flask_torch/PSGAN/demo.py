import argparse
import io
import cv2
from pathlib import Path

# from PIL import Imagepy
from PIL import Image
from psgan import Inference
from fire import Fire
import numpy as np

import faceutils as futils
from psgan import PostProcess
from setup import setup_config, setup_argparser

from matplotlib import pyplot as plt


def main(source_path='./assets/images/non-makeup/04.jpg',
        refer_path='assets/images/makeup',
        save_path='transferred_image_05.png'):
    parser = setup_argparser()
    parser.add_argument(
        "--source_path",
        default=source_path,
        metavar="FILE",
        help="path to source image")
    parser.add_argument(
        "--reference_dir",
        default=refer_path,
        help="path to reference images")
    parser.add_argument(
        "--speed",
        action="store_true",
        help="test speed")
    parser.add_argument(
        "--device",
        default="cuda",
        help="device used for inference")
    parser.add_argument(
        "--model_path",
        default="assets/models/G.pth",
        help="model for loading")

    args = parser.parse_args()
    config = setup_config(args)

    # Using the second cpu
    inference = Inference(config, args.device, args.model_path)
    postprocess = PostProcess(config)

    source = Image.open(args.source_path).convert("RGB")
    reference_paths = list(Path(args.reference_dir).glob("*"))
    np.random.shuffle(reference_paths)
    for reference_path in reference_paths:
        if not reference_path.is_file():
            print(reference_path, "is not a valid file.")
            continue

        reference = Image.open(reference_path).convert("RGB")

        # Transfer the psgan from reference to source.
        image, face = inference.transfer(source, reference, with_face=True)
        source_crop = source.crop((face.left(), face.top(), face.right(), face.bottom()))
        image = postprocess(source_crop, image)
        image.save(save_path)

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
    plt.savefig('result.jpg')
    # plt.show()


def makeup_transfer():
    main(source_path='./05.jfif')
    img_list=['./05.jfif','./assets/images/makeup/make_03.jpg','./transferred_image_05.png']
    labels=['source','reference','result']
    img_merge(img_list,labels)