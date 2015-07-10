# coding:utf-8
from PIL import Image as im

class Image:
    '''
    tranlate  value for color
    '''

    def __init__(self):
        pass
    # ----------------------------------------------------------
    # get picture color rgba
    # @:return str
    # ----------------------------------------------------------
    def getRgbaString(self,path):
        r, g, b, a = im.open(path).convert('RGBA').resize((1, 1)).getcolors()[0][1]
        return "rgba(%d, %d, %d, %d)" % (r, g, b, a)
    pass

    # ----------------------------------------------------------
    # get picture color rgba
    # @:return
    # ----------------------------------------------------------
    def getRgba(self,path):
        r, g, b, a = im.open(path).convert('RGBA').resize((1, 1)).getcolors()[0][1]
        return (r, g, b, a)
    pass

    # ----------------------------------------------------------
    # get picture color rgb
    # @:return str
    # ----------------------------------------------------------
    def getRgbString(self,path):
        r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
        return "rgb(%d, %d, %d)" % (r, g, b)
    pass

    # ----------------------------------------------------------
    # get picture color rgb
    # @:return
    # ----------------------------------------------------------
    def getRgb(self,path):
        r, g, b = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]
        return (r, g, b)
    pass
