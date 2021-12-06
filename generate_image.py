import argparse
import os
import random
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from data_aug import add


def cvt2img(
    txt,
    fontsize=20,
    fontpath="./font/batang.ttc",
    background="white",
    pad_left=3,
    pad_right=3,
    pad_up=3,
    pad_down=3,
    spacing=True,
    line_p=0.12,
    bbox=False,
):
    font = ImageFont.truetype(fontpath, fontsize, layout_engine=ImageFont.LAYOUT_BASIC)
    #     char_space = ' '*char_spacing

    # Add blank between characters
    if spacing:
        txt = list(txt)
        num_space = random.randint(0, len(txt) + 1)
        total_txt_len = len(txt) + num_space
        space_pos = random.sample(list(range(total_txt_len)), k=num_space)
        txt_cand = []
        for i in range(total_txt_len):
            if i in space_pos:
                txt_cand.append(" ")
            else:
                txt_cand.append(txt.pop(0))
        word = "".join(txt_cand)
        label = []
        prev = " "
        for w in word:
            if prev == " " and w == " ":
                continue
            else:
                label.append(w)
            prev = w

        label = "".join(label)
    else:
        word = txt
        label = txt
    label = label.strip(" ")

    # get text width and height
    try :
        txt_w, txt_h = font.getsize(word)
    except :
        print(fontpath)

    color = int(np.random.randint(100, 255, 1)[0])
    if background == "black":
        # blank = np.zeros((txt_h, txt_w), dtype=np.uint16)
        # set background size according to text size
        img = Image.new(
            "L", (txt_w + pad_left + pad_right, txt_h + pad_up + pad_down), "black"
        )
    elif background == "white":
        # blank = np.full((txt_h, txt_w),255, dtype=np.uint16)
        img = Image.new(
            "L", (txt_w + pad_left + pad_right, txt_h + pad_up + pad_down), color
        )
    elif background == ".jpg":
        # TODO: 글자 뒤에 이미지
        pass

    word_color = int(np.random.randint(0, 150, 1)[0])
    diff_thresh = 30
    while abs(color - word_color) < diff_thresh:
        if word_color > 75:
            word_color = int(
                np.random.randint(
                    0, min(75, color - diff_thresh, word_color - diff_thresh), 1
                )[0]
            )
        else:
            word_color = int(
                np.random.randint(
                    max(75, color - diff_thresh, word_color - diff_thresh), 150, 1
                )[0]
            )
    draw = ImageDraw.Draw(img)
    draw.text(xy=(pad_left, pad_up), text=word, font=font, fill=word_color)

    # add line
    add_line = random.choices([True, False], [line_p, 1 - line_p])[0]

    if add_line:
        add.line(draw, pad_left, pad_right, pad_up, pad_down, img.size)

    bboxes = []
    for i in range(1, len(txt) + 1):
        coord = [
            pad_left + fontsize * (i - 1),
            pad_up,
            pad_left + fontsize * (i),
            pad_up + txt_h,
        ]
        bboxes.append(coord)
    if bbox:
        return img, bboxes

    return img, label


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--txt", required=True, help="입력텍스트")
    parser.add_argument("--background", required=False, default="white", help="배경색")
    parser.add_argument("--pad_l", default=3, help="단어 왼쪽 패딩")
    parser.add_argument("--pad_r", default=3, help="단어 오른쪽 패딩")
    parser.add_argument("--pad_up", default=3, help="단어 위쪽 패딩")
    parser.add_argument("--pad_down", default=3, help="단어 아래쪽 패딩")
    parser.add_argument("--spacing", default=False, help="단어/글자 간 스페이스 여부")
    parser.add_argument("--word_space", default=1, help="단어 간 스페이스 값 설정(숫자)")
    parser.add_argument("--char_space", default=0, help="글자 간 스페이스 값 설정(숫자)")
    parser.add_argument("--line_p", default=0.12, help="임의의 선 추가할 확률값 설정")
    parser.add_argument("--save_path", default="./img", help="저장위치")
    parser.add_argument(
        "--fontpath", default="./font/batang.ttc", help="font path # dictionary 추가"
    )

    args = parser.parse_args()

    img = cvt2img(
        txt=args.txt,
        fontpath=args.fontpath,
        background=args.background,
        pad_left=args.pad_l,
        pad_right=args.pad_r,
        pad_up=args.pad_up,
        pad_down=args.pad_down,
        spacing=args.spacing,
        word_spacing=args.word_space,
        char_spacing=args.char_space,
        line_p=args.line_p,
    )

    font_dict = {
        "baekmuk_batang": "bm_bt",
        "baekmuk_dotum": "bm_dt",
        "baekmuk_gulim": "bm_gl",
        "batang": "bt",
        "gulim": "gl",
        "malgun": "mg",
        "malgunbd": "mgbd",
        "malgunsl": "mgsl",
        "NanumMyeongjo": "nmj",
        "NanumSquare_acB": "ns_acb",
        "NanumSquare_acEB": "ns_aceb",
        "NanumSquare_acL": "ns_acl",
        "NanumSquare_acR": "ns_acr",
    }

    font_name = args.fontpath.split("/")[-1].replace(".ttc", "")
    font_name = font_dict.get(font_name, font_name)

    now = datetime.now()
    dt_string = now.strftime("%m%d%H%M")

    img = np.array(img)

    os.makedirs(args.save_path, exist_ok=True)

    plt.imsave(
        os.path.join(
            args.save_path, args.txt + "_" + font_name + "_" + dt_string + ".jpg"
        ),
        img,
        cmap="gray",
    )
