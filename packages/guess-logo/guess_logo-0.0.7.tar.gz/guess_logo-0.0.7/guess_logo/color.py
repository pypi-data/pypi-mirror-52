import cv2
import numpy as np


class ColorLogo:

    @classmethod
    def replace(cls, source, target, color_upper=None, color_lower=None, color_repl='transparent'):
        im = cv2.imread(source)
        b_ch, g_ch, r_ch = cv2.split(im)
        h, w, c = im.shape

        a_ch = np.zeros((h, w), dtype=np.uint8)
        a_ch[:, :] = 255


        lower = np.array([210, 210, 210]) if color_lower is None else color_lower
        upper = np.array([255, 255, 255]) if color_upper is None else color_upper

        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        # 低于lower和高于upper的变成0
        mask = cv2.inRange(im, lower, upper)
        cv2.imshow('hsv', mask)


        erode = cv2.erode(mask, None, iterations=1)
        cv2.imshow('erode', erode)
        dilate = cv2.dilate(erode, None, iterations=1)
        cv2.imshow('dilate', dilate)

        im = cv2.merge((b_ch, g_ch, r_ch, a_ch))

        for i in range(h):
            for j in range(w):
                # print(dilate[i, j])
                if mask[i, j] == 255:
                    im[i, j] = (255, 255, 255, 0)  # 此处替换颜色，为BGR通道

        cv2.imwrite(target, im)


if __name__ == "__main__":
    source = 'demo/logo.jpeg'
    target = 'demo/logo.transparent.png'
    ColorLogo.replace(source, target)
