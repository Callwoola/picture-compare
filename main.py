# coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template

import lib.Image
# from template import tornado


def sortPicCode(list):
    # returnList=[]
    # thecode=list[0]['code']
    # for i in list:
    #     list['code']>thecode
    pass


PROJECT_DIR = "D:/code/image/"
IMAGE_DIR = "image/"
IMAEG_PATH = PROJECT_DIR + "img/"

COMPARE_IMG = "1.jpg"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("./")
        image = lib.Image.image()
        images = image.getImageList(IMAEG_PATH, IMAGE_DIR)

        for i in range(0, len(images)):
            images[i]['code'] = image.diff(IMAEG_PATH + COMPARE_IMG,
                                           images[i]['path']
                                           )
        print images
        html = loader.load("index.html") \
            .generate(images=images,
                      COMPARE_IMG=IMAGE_DIR + COMPARE_IMG
                      )
        self.write(html)

# settings = {'debug': True}
application = tornado.web.Application([
    (r"/", MainHandler),
    #(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "D:/code/image/static"}),
    (r'/image/(.*)', tornado.web.StaticFileHandler, {'path': IMAEG_PATH}),
])

if __name__ == "__main__":
    application.listen(8881)
    application.debug = True
    # application.autoreload=False
    tornado \
        .ioloop \
        .IOLoop \
        .current() \
        .start()
