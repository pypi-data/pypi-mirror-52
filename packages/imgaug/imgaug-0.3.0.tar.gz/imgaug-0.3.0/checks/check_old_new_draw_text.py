from __future__ import print_function, division
import imgaug as ia
import numpy as np


def main():
    inputs = [
        {"y": 25, "x": 0, "text": "Example", "color": (255, 255, 255),
         "size": 25},
        {"y": 5, "x": 0, "text": "Example", "color": (255, 255, 255),
         "size": 25},
        {"y": 0, "x": 0, "text": "Example", "color": (255, 255, 255),
         "size": 25},
        {"y": 25, "x": 0, "text": "Example", "color": (255, 255, 255),
         "size": 10},
    ]

    img = np.zeros((100, 200, 3), dtype=np.uint8)
    img = ia.pad(img, top=1, right=1, bottom=1, left=1, cval=128)
    imgs_out = []

    for inputs_i in inputs:
        imgs_out.append(
            np.hstack([
                ia.draw_text(img, **inputs_i),
                ia.draw_text_cv2(img, **inputs_i),
            ])
        )

    ia.imshow(np.vstack(imgs_out))


if __name__ == "__main__":
    main()
