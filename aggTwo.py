import scipy as sp
from scipy.misc import imread
from scipy.signal.signaltools import correlate2d as c2d


def get(i):
    # get JPG image as Scipy array, RGB (3 layer)
    print i
    data = imread(i)
    # convert to grey-scale using W3C luminance calc
    data = sp.inner(data, [299, 587, 114]) / 1000.0
    # normalize per http://en.wikipedia.org/wiki/Cross-correlation
    return (data - data.mean()) / data.std()


im1 = get("img/img1/1.jpg")
im2 = get("img/img1/2.jpg")
im3 = get("img/img1/3.jpg")

c11 = c2d(im1, im1, mode='same')  # baseline
print c11.max()

exit()
c12 = c2d(im1, im2, mode='same')
c13 = c2d(im1, im3, mode='same')
c23 = c2d(im2, im3, mode='same')
print c11.max(), c12.max(), c13.max(), c23.max()
