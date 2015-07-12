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


    def getHsi(self,path):
        '''
        Unfortunately I think that this transformation can not be done
        with Image.convert: you can only do transformations between equivalent
        color spaces (i.e. reach the destination colorspace by doing a
        multiplication with a matrix with the source colorspace).

        The HSI colorspace, instead, is not an equivalent colorspace of RGB.
        To get the HSI equivalent of a RGB pixel one must do these
        transformations:

        :return:
        '''
        import math

        R, G, B = im.open(path).convert('RGB').resize((1, 1)).getcolors()[0][1]

        I = 1/3 * (R+G+B)

        S = 1 - (3/(R+G+B))*(min(R,G,B))

        H = math.cos^-1( (((R-G)+(R-B))/2)/ (math.sqrt((R-G)^2 + (R-B)*(G-B) )))

        return (H,S,I)
    pass