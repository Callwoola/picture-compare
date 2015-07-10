#coding:utf-8
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from src.lib import Image
from src.lib import Manage
from src.lib import Compare
from src import config


class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(config.TEMPLATE)
        image = Image.Image()
        compare = Compare.Image()
        packages = ["img1/", "img2/", "img4/"]
        manage = Manage.Manage()
        package_image = []
        for package in packages:
            # --------------------------
            # get differ image package
            # package = "img1/"
            images = manage.getImageList(config.STATIC_DIR + package, config.STATIC_DIR + package)
            COMPARE_IMG = manage.getFirst(config.STATIC_DIR + package)

            for i in range(0, len(images)):
                compare.setA(config.STATIC_DIR + package + COMPARE_IMG)
                compare.setB(images[i]['path'])

                images[i]['origin_img'] = config.STATIC_DIR + package + COMPARE_IMG

                compare.start()
                images[i]['code'] = compare.phash()
                images[i]['code2'] = compare.mse()
                images[i]['code3'] = compare.perceptualHash()
                images[i]['color'] = image.getRgbaString(images[i]['path'])
                compare.end()
                # images[i]['code3'] = Compare.correlate2d()
            package_image.append(images)

        html = loader.load("demo.html") \
            .generate(images=images,
                      packages=packages,
                      package_image=package_image,
                      COMPARE_IMG=config.STATIC_DIR + config.TEST_COMPARE_IMG
                      )
        self.write(html)


class DemoSearchHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):

        self.write(tornado.template.Loader(config.TEMPLATE).load("search.html").generate(
            action='upload_search'
        ))



class DemoUploadSearchHandler(tornado.web.RequestHandler):
    """
    TODO search test
    """
    def post(self):
        import StringIO
        from PIL import Image
        from src.lib import Manage
        from src.lib import Compare
        import os
        from src.lib import Image as ImageTool
        try:
            imagetool=ImageTool.Image()
            compare = Compare.Image()
            imgfiles = self.request.files['file_img']
            if len(imgfiles) > 1:
                return self.write("error")
            imgfile = imgfiles[0]
            filename = imgfile['filename'].strip()

            tmp = config.PROJECT_DIR + "tests/tmp/"
            tmp_image = tmp + filename
            Image.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)

            path = config.PROJECT_DIR + "tests/img/"
            # start compare imgs
            manage = Manage.Manage()
            results = []
            # ------------------------------------------
            # result must got to sort and set size
            # maybe add index for quick find image

            for i in manage.getPathAllFile(path):
                compare.setA(tmp_image)
                compare.setB(i)
                compare.start()

                results.append({
                    'filename': os.path.basename(i),
                    'code1': compare.phash(),
                    'code2': compare.mse(),
                    'code3': compare.perceptualHash(),
                    'code_mix': compare.mixHash(),
                    'color': imagetool.getRgbString(i),
                })
                compare.end()

            # ---------------------------------------------
            # simple sort list by code
            results_code1 = sorted(results, key=lambda k: k['code1'])
            results_code2 = sorted(results, key=lambda k: k['code2'])
            results_code3 = sorted(results, key=lambda k: k['code3'])
            results_mix = sorted(results, key=lambda k: k['code_mix'])

            self.write(tornado.template.Loader(config.TEMPLATE).load("search_result.html").generate(
                origin_img=filename,
                results_code1=results_code1,
                results_code2=results_code2,
                results_code3=results_code3,
                results_mix=results_mix,
            ))
        except Exception, e:
            print e
            self.redirect('search')
