# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
import lib.Compare
import lib.Image
# from template import tornado
import os


def sortPicCode(list):
    # returnList=[]
    # thecode=list[0]['code']
    # for i in list:
    #     list['code']>thecode
    pass


PROJECT_DIR = "D:/code/image/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"

COMPARE_IMG = "1.jpg"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(PROJECT_DIR+"web/")
        image = lib.Image.image()
        Compare = lib.Compare.Image()
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
                Compare.setA(PROJECT_DIR_IMG + package + COMPARE_IMG)
                Compare.setB(images[i]['path'])

                images[i]['origin_img'] = STATIC_DIR + package + COMPARE_IMG

                Compare.start()
                images[i]['code'] = Compare.base()
                images[i]['code2'] = Compare.mse()
                images[i]['code3'] = Compare.perceptualHash()
                Compare.end()
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

# settings = {'debug': True}
application = tornado.web.Application([
    (r"/", MainHandler),
    # (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "D:/code/image/static"}),
    (r'/img/(.*)', tornado.web.StaticFileHandler, {'path': PROJECT_DIR_IMG}),
])

if __name__ == "__main__":
    application.listen(8888)
    application.debug = True
    # application.autoreload=False
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()
