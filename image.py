# coding:utf-8

from PIL import Image
# import Image
import math
import operator
import pyquery

def getImage():
    pass


class imageDiff:
    def open(self):
        pass

# sudo pip install PIL
'''
    to open the file
'''
def pil_image_similarity(filepath1, filepath2):
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    return rms


"""
@:return list
"""
def getImageList():
    import os

    rootDir = "./image"
    fileSet = []

    for dir_, _, files in os.walk(rootDir):
        for fileName in files:
            relDir = os.path.relpath(dir_, rootDir)
            relFile = os.path.join(relDir, fileName)
            # fileSet.add(relFile)
            fileSet.append(relFile)
    return fileSet


path = "./image/"
firstImg = path + "1.jpg"
for i in getImageList():
    print pil_image_similarity(
        firstImg,
        path+i
    )


    # i1 = path + "6.jpg"
    # i2 = path + "9.jpg"
    # i3 = path + "1.jpg"
    #
    # print pil_image_similarity(i1, i2)
    # print pil_image_similarity(i1, i3)
