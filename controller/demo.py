import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from lib import Image
from lib import Compare

PROJECT_DIR = "/Users/liyang/Code/pictureCompare/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"

COMPARE_IMG = "1.jpg"


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        loader = tornado.template.Loader(PROJECT_DIR+"web/")
        image = Image.Image()
        compare = Compare.Image()
        packages = ["img1/", "img2/","img4/"]
        #packages = ["img1/", "img2/"]

        #packages = ["img3/"]

        package_image = []
        for package in packages:
            # --------------------------
            # get differ image package
            # package = "img1/"
            images = image.getImageList(PROJECT_DIR_IMG + package, STATIC_DIR + package)
            COMPARE_IMG = image.getFirst(PROJECT_DIR_IMG + package)
            print images
            for i in range(0, len(images)):
                compare.setA(PROJECT_DIR_IMG + package + COMPARE_IMG)
                compare.setB(images[i]['path'])

                images[i]['origin_img'] = STATIC_DIR + package + COMPARE_IMG

                compare.start()
                images[i]['code'] = compare.base()
                images[i]['code2'] = compare.mse()
                images[i]['code3'] = compare.perceptualHash()
                compare.end()
                # images[i]['code3'] = Compare.correlate2d()
            package_image.append(images)

        print package_image
        html = loader.load("index.html") \
            .generate(images=images,
                      packages=packages,
                      package_image=package_image,
                      COMPARE_IMG=PROJECT_DIR_IMG + COMPARE_IMG
                      )
        self.write(html)