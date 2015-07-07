# coding:utf-8

import math
import operator

from PIL import Image


class image:
    def __init__(self):
        pass

    def getImageList(self, path, base_path):
        import os

        rootDir = path
        fileSet = []
        for dir_, _, files in os.walk(rootDir):
            for fileName in files:
                # relDir = os.path.relpath(dir_, rootDir)
                # relFile = os.path.join(relDir, fileName)
                # fileSet.add(relFile)
                # print fileName
                fileSet.append({"url": base_path + fileName,
                                "path": path + fileName,
                                })
        return fileSet

    def pil_image_similarity(self, file1, file2):
        image1 = Image.open(file1)
        image2 = Image.open(file2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        rms = math.sqrt(
            reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2)))
            /
            len(h1)
        )
        return rms

    def diff(self, f1, f2):
        return self.pil_image_similarity(f1, f2)

    # return a number to
    def getColorType(self, path):
        if not type(path) is str:
            return
