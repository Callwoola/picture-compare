def first():
    import PIL
    from PIL import Image
    from matplotlib import pyplot as plt

    im = Image.open('../img/img1/1.jpg')
    w, h = im.size
    colors = im.getcolors(w * h)

    def hexencode(rgb):
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        return '#%02x%02x%02x' % (r, g, b)

    def getColor(im):
        im.size

    for idx, c in enumerate(colors):
        plt.bar(idx, c[0], color=hexencode(c[1]))
    for idx, c in enumerate(colors):
        plt.bar(idx, c[0], color=hexencode(c[1]), edgecolor=hexencode(c[1]))

    plt.show()


def main():
    import cv2
    import matplotlib.pyplot as plt

    def show_histogram(im):
        """ Function to display image histogram.
            Supports single and three channel images. """

        if im.ndim == 2:
            # Input image is single channel
            plt.hist(im.flatten(), 256, range=(0, 250), fc='k')
            plt.show()

        elif im.ndim == 3:
            # Input image is three channels
            fig = plt.figure()
            fig.add_subplot(311)
            plt.hist(im[..., 0].flatten(), 256, range=(0, 250), fc='b')
            fig.add_subplot(312)
            plt.hist(im[..., 1].flatten(), 256, range=(0, 250), fc='g')
            fig.add_subplot(313)
            plt.hist(im[..., 2].flatten(), 256, range=(0, 250), fc='r')
            plt.show()

    if __name__ == '__main__':
        im = cv2.imread('../img/img1/1.jpg')
        if not (im is None):
            show_histogram(im)


def two():
    import cv2
    import matplotlib.pyplot as plt

    im = cv2.imread('../img/img1/1.jpg')
    plt.hist(im.flatten(), 256, range=(0, 255))
    plt.hist(im[..., 0].flatten(), 256, range=(0, 250), fc='b')
    plt.show()


def test():
    from PIL import Image
    import cv2

    path = '../img/img1/1.jpg'
    im = Image.open(path)
    im2 = cv2.imread(path)[..., 0].flatten()
    print len(im2)
    array = im.convert("RGB").histogram()
    print len(array)


def major():
    from PIL import Image

    im = Image.open("../img/img1/1.jpg")
    return max(im.getcolors(im.size[0] * im.size[1]))


def getRgba(path):
    from PIL import Image
    r, g, b, a = Image.open(path).convert('RGBA').resize((1, 1)).getcolors()[0][1]
    return "rgba(%d, %d, %d, %d)" % (r, g, b, a)


if __name__ == '__main__':
    # two()
    # test()
    print getRgba("../img/img4/1.jpg")
