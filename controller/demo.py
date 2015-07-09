import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from lib import Image
from lib import Manage
from lib import Compare

PROJECT_DIR = "D:/code/image/"
STATIC_DIR = "img/"
PROJECT_DIR_IMG = PROJECT_DIR + "img/"
COMPARE_IMG = "1.jpg"
TEMPLATE_DIR = PROJECT_DIR + "template/"

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(TEMPLATE_DIR)
        image = Image.Image()
        compare = Compare.Image()
        packages = ["img1/", "img2/", "img4/"]
        manage=Manage.Manage()
        package_image = []
        for package in packages:
            # --------------------------
            # get differ image package
            # package = "img1/"
            images = manage.getImageList(PROJECT_DIR_IMG + package, STATIC_DIR + package)
            COMPARE_IMG = manage.getFirst(PROJECT_DIR_IMG + package)
            print images
            for i in range(0, len(images)):
                compare.setA(PROJECT_DIR_IMG + package + COMPARE_IMG)
                compare.setB(images[i]['path'])

                images[i]['origin_img'] = STATIC_DIR + package + COMPARE_IMG

                compare.start()
                images[i]['code'] = compare.phash()
                images[i]['code2'] = compare.mse()
                images[i]['code3'] = compare.perceptualHash()
                images[i]['color'] = image.getRgbaString(images[i]['path'])
                compare.end()
                # images[i]['code3'] = Compare.correlate2d()
            package_image.append(images)

        print package_image
        html = loader.load("demo.html") \
            .generate(images=images,
                      packages=packages,
                      package_image=package_image,
                      COMPARE_IMG=PROJECT_DIR_IMG + COMPARE_IMG
                      )
        self.write(html)


class DemoSearchHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(tornado.template.Loader(TEMPLATE_DIR).load("search.html").generate(
            action='upload_search'
        ))
"""
TODO search test
"""
class DemoUploadSearchHandler(tornado.web.RequestHandler):
    def post(self):
        import StringIO
        from PIL import Image
        from lib import Manage
        try:
            imgfiles = self.request.files['file_img']
            if len(imgfiles)>1:
                return self.write("error")
            imgfile = imgfiles[0]
            filename=imgfile['filename']
            Image.open(StringIO.StringIO(imgfile['body'])).save(filename)

            path=PROJECT_DIR+"tests/img/img1/"
            # start compare imgs
            manage=Manage.Manage()
            result=[]
            for i in manage.getPathAllFile(path):
                print result.append({
                    ''
                })
            self.write(tornado.template.Loader(TEMPLATE_DIR).load("search_result.html").generate(
                action='upload_search',
                result=result
            ))
        except Exception,e:
            print e
            self.redirect('search')