import random

import numpy as np
import scipy.ndimage as ndi
import skimage


def line(draw, pad_left, pad_right, pad_up, pad_down, size, err=3):
    """
    :param draw: ImageDraw object to add line
    :pad_left
    :pad_right
    :pad_up
    :pad_down
    :param txt_w:
    :param txt_h:
    :return:
    """
    direction = random.choice(["hor", "ver"])

    # slope range (-0.01, 0.01)
    slope = random.uniform(-0.01, 0.01)

    if direction == "hor":
        lr = random.choice(["left", "right"])

        if lr == "left":
            y1 = random.choice(
                [
                    random.randint(0, pad_up + err),
                    random.randint(size[1] - pad_down - err, size[1]),
                ]
            )
            x1 = 0
            if y1 < pad_up + err:
                # 글자 위로 hor line
                y2 = 0
            else:
                # 글자 아래로 hor line
                y2 = size[1]
            x2 = (y2 - y1 + slope * x1) / slope

        else:
            y2 = random.choice(
                [
                    random.randint(0, pad_up + err),
                    random.randint(size[1] - pad_down - err, size[1]),
                ]
            )
            x2 = size[0]
            if y2 < pad_up + err:
                y1 = 0
                x1 = (slope * x2 - y2) / slope
            else:
                y1 = size[1]
                x1 = (slope * x2 - y2 + y1) / slope

    else:  # vertical line

        x1 = random.choice(
            [
                random.randint(0, pad_left + err),
                random.randint(size[0] - pad_right - err, size[0]),
            ]
        )
        y1 = 0
        y2 = size[1]
        x2 = slope * (y2 - y1) + x1

    return draw.line([(x1, y1), (x2, y2)], fill="black", width=0)


def binary_blur(image, sigma=1.5, noise=0.0):
    """
    sigma = 0.0 ~ 3.0
    noise = 0.0 ~ 0.3
    sigma makes character noisy, noise makes document noisy
    """

    def percent_black(image):
        n = np.prod(image.shape)
        k = sum(image < 0.5)
        return k * 100.0 / n

    p = percent_black(image)
    blurred = ndi.gaussian_filter(image, sigma)
    if noise > 0:
        blurred += np.random.randn(*blurred.shape) * noise
    t = np.percentile(blurred, p)
    return np.array(blurred > t, "f")


def random_blotches(image, fgblobs=3e-4, bgblobs=1e-4, fgscale=10, bgscale=10):
    """
    fgblobs = 3e-4
    bgblobs = 1e-4
    makes some loss in characters
    """

    def random_blobs(shape, blobdensity, size, roughness=2.0):
        h, w = shape
        numblobs = int(blobdensity * w * h)
        mask = np.zeros((h, w), "i")
        for i in range(numblobs):
            mask[np.random.randint(0, h - 1), np.random.randint(0, w - 1)] = 1
        dt = ndi.distance_transform_edt(1 - mask)
        mask = np.array(dt < size, "f")
        mask = ndi.gaussian_filter(mask, size / (2 * roughness))
        mask -= np.amin(mask)
        mask /= np.amax(mask)
        noise = np.random.rand(h, w)
        noise = ndi.gaussian_filter(noise, size / (2 * roughness))
        noise -= np.amin(noise)
        noise /= np.amax(noise)
        return np.array(mask * noise > 0.5, "f")

    fg = random_blobs(image.shape, fgblobs, fgscale)
    bg = random_blobs(image.shape, bgblobs, bgscale)
    new_image = np.minimum(np.maximum(image, fg), 1 - bg)
    return new_image


def noise(img):
    noise_type = [
        "gaussian",
        "localvar",
        "poisson",
        "salt",
        "pepper",
        "s&p",
        "speckle",
        "None",
    ]
    mode = random.choice(noise_type)
    if mode != "None":
        img = skimage.util.random_noise(img, mode=mode)

    return img


def water_drop(image, sigma=1.5):  # Not Yet
    """
    :return: 랜덤한 위치에 랜덤한 영역의 gaussian noise
    TODO: 현재 crop된 사각형에 gaussian noise를 취하는 방식
        -> 더 자연스러운 polygon이나 주변 영역을 추가적으로 blur처리하는 방안
    """
    rand_n = random.randint(0, 2)
    for i in range(rand_n):
        rand_portion_w = random.uniform(0.15, 0.5)
        rand_portion_h = random.uniform(0.15, 0.5)
        h, w = image.shape[:2]

        drop_width = int(w * rand_portion_w)
        drop_height = int(h * rand_portion_h)

        start_w = random.randint(0, w - drop_width)
        start_h = random.randint(0, h - drop_height)

        cropped = image[
            start_h : start_h + drop_height, start_w : start_w + drop_width, :
        ]

        dropped = ndi.gaussian_filter(cropped, sigma=sigma)

        image[
            start_h : start_h + drop_height, start_w : start_w + drop_width, :
        ] = dropped

    return image
