import random

import cv2
import matplotlib.pyplot as plt
import numpy as np


def random_rotate(img, angle):
    """
    img : input image
    angle : rotation range
    """
    # 80%확률 15도 내에 회전, 나머지 15와 30도 사이

    #     prob=random.randint(0,100)
    #     if prob>=90:
    #         # 10도 미만
    #         rotate_angle=random.randint(-int(angle*0.3), int(angle*0.3))
    #     else:
    #         # 15도와 30도 사이
    #         rotate_angle=random.randint(*random.choice([(-int(angle), -int(angle*0.3)), (int(angle*0.3), int(angle))]))
    rotate_angle = angle
    # if type(img)==np.ndarray:
    #     img=Image.fromarray(img)
    if type(img) == str:
        img = plt.imread(img)

    # now rotate image without cropping
    height, width = img.shape[:2]
    image_center = (width / 2, height / 2)

    rotate_img = cv2.getRotationMatrix2D(image_center, rotate_angle, 1.0)

    abs_cos = abs(rotate_img[0, 0])
    abs_sin = abs(rotate_img[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center(bringing image back to origo) and adding the new image center coordinates
    rotate_img[0, 2] += bound_w / 2 - image_center[0]
    rotate_img[1, 2] += bound_h / 2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    borderMode = cv2.BORDER_REPLICATE
    #     cv2.BORDER_REFLECT101
    rotate_img = cv2.warpAffine(
        img, rotate_img, (bound_w, bound_h), borderMode=borderMode
    )

    return rotate_img


def wrinkle(img):
    rows, cols = img.shape[:2]

    mapy, mapx = np.indices((rows, cols), dtype=np.float32)

    rep = random.randint(1, 3)

    for i in range(rep):
        l = random.uniform(4, 12)
        amp = random.uniform(1, 3)
        extra = random.choice(range(10))

        # print('trial {}\namp:{}\nwavelength:{}\nextra:{}'.format(i + 1, amp, l, extra))

        plus_x = random.choice(
            [amp * np.sin(mapy / l + extra), amp * np.cos(mapy / l + extra)]
        )
        mapx += plus_x
        plus_y = random.choice(
            [amp * np.sin(mapy / l + extra), amp * np.cos(mapy / l + extra)]
        )
        mapy += plus_y

    img = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR, None, cv2.BORDER_REPLICATE)

    return img


# fiducial point 지정후, distort 작업, 아직 완성X
def get_new_pt(og_point, radius):
    r = random.randint(0, radius)

    theta = random.uniform(0, 360)
    x = np.cos(theta) * r
    y = np.sin(theta) * r

    new_point = (og_point[0] + x, og_point[1] + y)

    return new_point


def get_fiducial_point(img, num, radius=10):
    h, w = img.shape[:2]
    width = w / (num)

    img = np.pad(
        img,
        ((radius, radius), (radius, radius), (0, 0)),
        mode="constant",
        constant_values=3,
    )
    img.copy()

    plt.imshow(img)
    plt.show()
    points = [int(radius + i * width) for i in range(num + 1)]

    upper = [(pt, radius) for pt in points]
    lower = [(pt, radius + h) for pt in points]

    new_upper = [get_new_pt(pt, radius) for pt in upper]
    new_lower = [get_new_pt(pt, radius) for pt in lower]

    warps = []

    maxWidth = int(width + 2 * radius)
    maxHeight = int(h + 2 * radius)

    print(maxWidth, maxHeight)
    for i in range(len(new_upper) - 1):
        og_pts = np.array((upper[i], upper[i + 1], lower[i], lower[i + 1]), np.float32)
        new_pts = np.array(
            (new_upper[i], new_upper[i + 1], new_lower[i], new_lower[i + 1]), np.float32
        )

        #         print(new_pts)
        #         print(og_pts[2][1],og_pts[-1][1], og_pts[2][0],og_pts[-1][0])

        #         plt.imshow(img[og_pts[0][1]:og_pts[-1][1], og_pts[2][0]:og_pts[-1][0] ])
        #         plt.show()

        #         maxWidth = int(max(new_pts[1][0], new_pts[-1][0]) - min(new_pts[0][0], new_pts[2][0]) )
        #         maxHeight = int(max(new_pts[1][1], new_pts[-1][1]) - min(new_pts[0][1], new_pts[2][1]))

        img_part = img[upper[i][1] : lower[i][1], upper[i][0] : upper[i + 1][0]]

        M = cv2.getPerspectiveTransform(new_pts, og_pts)

        #         bx, by, bwidth, bheight = cv2.boundingRect(M[0])
        A = np.eye(3, 3)
        A[0, 2] = (upper[i][0] - new_upper[i][0]) + (
            upper[i + 1][0] - new_upper[i + 1][0]
        )
        A[1, 2] = (upper[i][1] - new_upper[i][1]) + (
            upper[i + 1][1] - new_upper[i + 1][1]
        )

        A * M

        #         print(F)
        warped = cv2.warpPerspective(
            img_part,
            M,
            (maxWidth, maxHeight),
            cv2.INTER_LINEAR,
            cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255),
        )
        plt.imshow(warped)
        plt.show()
        #         warped = cv2.warpPerspective(warped, F, (maxWidth,maxHeight), cv2.INTER_LINEAR,cv2.BORDER_CONSTANT, borderValue=(255,255,255))
        #         plt.imshow(warped)
        #         plt.show()
        #         print(int(min(new_pts[0][0], new_pts[2][0])-radius))

        #         print(int(max(new_pts[1][0], new_pts[-1][0])+radius))

        warps.append(warped)

    plt.imshow(np.hstack(warps))
