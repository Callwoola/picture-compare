# coding:utf-8

from src.detector import Detector
class Perceptual(Detector):    

    def do_screening(self):
        return 'the have module'

    def perceptualHash(self, path=True):
        '''
        huhh...
        '''
        from PIL import Image
        def avhash(im):
            if not isinstance(im, Image.Image):
                im = Image.open(im)
            im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
            avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
            return reduce(
                lambda x, (y, z): x | (z << y),
                enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                0
            )

        def hamming(h1, h2):
            h, d = 0, h1 ^ h2
            while d:
                h += 1
                d &= d - 1
            return h

        a = avhash(self.image_a_path)
        b = avhash(self.image_b_path)
        value = hamming(a, b)
        self.value_of_perceptualHash = value
        return value
