import argparse
import os
import random
import uuid
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from glob import glob

import cv2
import numpy as np
import PIL
from PIL import ImageFilter
from tqdm import tqdm

from data_aug import add, transform
from generate_image import cvt2img
from generate_texts import random_number
from logger import configure_log, createLogger

parser = argparse.ArgumentParser()
parser.add_argument("--dictionary_dir", "-d", type=str, help="Dictionary dir path")
parser.add_argument("--fonts_dir", "-f", help="Fonts dir path")
parser.add_argument(
    "--num_images",
    "-n",
    default=2000000,
    type=int,
    help="The number of images to generate",
)
parser.add_argument(
    "--batch_len",
    "-b",
    default=50000,
    type=int,
    help="The number of images stored in one directory",
)
parser.add_argument(
    "--save_dir", "-s", type=str, required=True, help="Directory path to save images"
)
parser.add_argument(
    "--mode",
    "-m",
    choices=["word", "number"],
    default="word",
    help="Select mode [word|number]",
)
args = parser.parse_args()


def main(args):
    logger = createLogger("Main")
    configure_log()

    word_list = []
    if args.mode == "word":
        # Read words from dictionary txt files
        dict_files = glob(os.path.join(args.dictionary_dir, "*"))
        for df in dict_files:
            if os.path.isfile(df):
                with open(df) as f:
                    data = f.read().split("\n")
                    logger.info(f"Reading {len(data)} words from {df}")
                    for d in data:
                        word_list.append(d)
    else:
        logger.info("Generating random numbers ...")
        for _ in range(args.num_images):
            word_list.append(random_number(15))

    word_list = [_ for _ in list(set(word_list)) if _ != ""]
    logger.info(f"The number of unique words ==> {len(word_list)}")

    # Read fonts from directory
    font_list = glob(os.path.join(args.fonts_dir, "*.t*"))
    logger.info(f"Reading fonts from {args.fonts_dir}")
    logger.info(f"The number of fonts ==> {len(font_list)}")

    # generate images and save
    batch_len = min(len(word_list), args.batch_len)
    iteration = args.num_images // batch_len

    for i in range(iteration + 1):
        if i == iteration:
            batch_len = min(len(word_list), args.num_images - batch_len * iteration)
        gt_save_dir = os.path.join(args.save_dir, f"split_{i}")
        image_save_dir = os.path.join(args.save_dir, f"split_{i}/images")
        if not os.path.exists(image_save_dir):
            os.makedirs(image_save_dir)
        np.random.shuffle(word_list)
        with ProcessPoolExecutor() as p:
            result = list(
                tqdm(
                    p.map(
                        partial(
                            save_image,
                            image_save_dir=image_save_dir,
                            font_list=font_list,
                        ),
                        word_list[:batch_len],
                    ),
                    total=batch_len,
                )
            )
        with open(os.path.join(gt_save_dir, "gt_lines.txt"), "a") as f:
            for r in result:
                f.write(r)


def save_image(word, image_save_dir, font_list):
    # set random variables
    pad_left = random.randint(0, 10)
    pad_right = random.randint(0, 10)
    pad_up = random.randint(0, 10)
    pad_down = random.randint(0, 10)
    do_rotate = random.choices([1, 0], weights=[0.3, 0.7])[0]
    rotate_angle = random.randrange(-7, 7)
    wrinkle = random.choices([1, 0], weights=[0.3, 0.7])[0]
    noise = random.choices([1, 0], weights=[0.3, 0.7])[0]
    blur = random.choices([1, 0], weights=[0.4, 0.6])[0]
    fontsize = random.randint(20, 40)
    font = random.choices(font_list)[0]
    spacing = random.choices([1, 0], weights=[0.2, 0.8])[0]
    do_shrink = random.choices([1, 0], weights=[0.7, 0.3])[0]
    quality = random.randint(10, 100)

    # generate image and label
    img, label = cvt2img(
        word,
        fontsize,
        fontpath=font,
        pad_left=pad_left,
        pad_right=pad_right,
        pad_up=pad_up,
        pad_down=pad_down,
        spacing=spacing,
    )
    img = np.array(img)

    # add noise
    if wrinkle:
        img = transform.wrinkle(img)
    if do_rotate:
        img = transform.random_rotate(img, rotate_angle)
    if noise:
        img = add.noise(img)
        img = (img * 255).astype(np.uint8)
    if blur:
        img = PIL.Image.fromarray(img)
        img = img.filter(ImageFilter.GaussianBlur(2))
        img = np.array(img)
    if do_shrink:
        image_shape = img.shape[:2]
        tgt_size = random.randint(
            int(min(image_shape) * 0.5), int(min(image_shape) * 0.8)
        )
        if image_shape[0] > image_shape[1]:
            ratio = tgt_size / image_shape[1]
        else:
            ratio = tgt_size / image_shape[0]
        img = cv2.resize(
            img,
            dsize=(round(ratio * image_shape[1]), round(ratio * image_shape[0])),
            interpolation=cv2.INTER_AREA,
        )
        quality = 100

    # set image name
    font_name = os.path.splitext(os.path.basename(font))[0]
    imgfile = f"augtext-{uuid.uuid4().hex[:15]}-{font_name}.jpg"
    img = PIL.Image.fromarray(img)
    img.save(os.path.join(image_save_dir, imgfile), quality=quality)

    return imgfile + "\t" + label + "\n"


if __name__ == "__main__":
    main(args)
