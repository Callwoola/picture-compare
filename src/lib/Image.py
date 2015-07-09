# coding:utf-8

class Image:

    # ----------------------------------------------------------
    # get picture color
    # @:return str
    # ----------------------------------------------------------
    def getRgbaString(self,path):
        from PIL import Image
        r, g, b, a = Image.open(path).convert('RGBA').resize((1, 1)).getcolors()[0][1]
        return "rgba(%d, %d, %d, %d)" % (r, g, b, a)
    pass

    # ----------------------------------------------------------
    # get picture color
    # @:return
    # ----------------------------------------------------------
    def getRgba(self,path):
        from PIL import Image
        r, g, b, a = Image.open(path).convert('RGBA').resize((1, 1)).getcolors()[0][1]
        return (r, g, b, a)
    pass
