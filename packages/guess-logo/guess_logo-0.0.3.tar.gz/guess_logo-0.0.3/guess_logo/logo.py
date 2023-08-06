import os
import cv2
import numpy as np
from PIL import Image


class Logo:

    @staticmethod
    def new_image(width, height, bgcolor, alpha=0):
        im_mt = np.zeros((height, width), dtype=np.uint8)

        im = cv2.cvtColor(im_mt, cv2.COLOR_GRAY2BGR)

        b_ch, g_ch, r_ch = cv2.split(im)

        a_ch = np.zeros((height, width), dtype=np.uint8) 

        a_ch[:, :] = alpha

        im = cv2.merge((b_ch, g_ch, r_ch, a_ch))

        return im

    @classmethod
    def resize(cls, source, target, width, height, bgcolor=None):
        width = int(width)
        height = int(height)
        bgcolor = (0, 0, 0) if bgcolor is None else bgcolor

        im_source = cv2.imread(source)

        height_source, width_source, channels_source = im_source.shape

        im = cls.new_image(width, height, bgcolor, alpha=0)

        ratio_target = width / height
        ratio_source = width_source / height_source

        if ratio_target >= ratio_source:
            """
                如果比例小于目标比例，说明宽度不够
                则调整宽度，高度保持不变
            """
            width_adj = int(width_source * height / height_source)
            im_target = cv2.resize(im_source, (width_adj, height), interpolation=cv2.INTER_CUBIC)
            y1, y2 = 0, height
            x1 = int((width - width_adj) /  2)
            x2 = x1 + width_adj
        else:
            """
                如果比例大于目标比例，说明高度不够
                则调整高度，宽度保持不变
            """
            height_adj = int(height_source * width / width_source)
            im_target = cv2.resize(im_source, (width, height_adj), interpolation=cv2.INTER_CUBIC)
            x1, x2 = 0, width
            y1 = int((height - height_adj) / 2)
            y2 = y1 + height_adj

        im[y1:y2, x1:x2, :3] = im_target[:, :, :]
        im[y1:y2, x1:x2, 3] = 255 # 因为这张新图片有4个通道，需要新图片这个位置的4通道设置为255，即不透明

        cv2.imwrite(target, im)
        return im
    
    


if __name__ == "__main__":
    height = 256
    width = 512
    source = 'demo/ifengLogo.png'
    target = 'demo/ifengLogo_{}_{}.png'.format(width, height)
    Logo.resize(source, target, width, height, bgcolor='transparent')