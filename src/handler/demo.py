# coding:utf-8
import os
import glob
import StringIO
import tornado
import tornado.ioloop
import tornado.web
import tornado.template
from PIL import Image as im

from src import config
from src.core.app import App
from src.lib.image import Image
from src.service.feature import Feature as Compare
from src.service.manage import Manage as Manage
from src.service.match import Match


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(tornado.template
            .Loader(os.environ[config.TEMPLATE])
            .load("index.html")
            .generate())

class DemoHandler(tornado.web.RequestHandler):
    def get(self):

        os.chdir(os.environ[config.PROJECT_DIR])
        loader = tornado.template.Loader(os.environ[config.TEMPLATE])
        # image = Image()
        compare = Compare()
        packages = ["img1/", "img2/", "img4/"]
        manage = Manage()
        package_image = []
        for package in packages:
            # --------------------------
            # get differ image package
            # package = "img1/"
            images = manage.getImageList(os.environ[config.STATIC_DIR] + package,
                                         os.environ[config.STATIC_DIR] + package)
            COMPARE_IMG = manage.getFirst(os.environ[config.STATIC_DIR] + package)

            for i in range(0, len(images)):
                compare.setA(os.environ[config.STATIC_DIR] + package + COMPARE_IMG)
                compare.setB(images[i]['path'])

                images[i]['origin_img'] = os.environ[config.STATIC_DIR] + package + COMPARE_IMG

                compare.start()
                images[i]['code'] = compare.basehash()
                images[i]['code2'] = compare.basehash()
                images[i]['code3'] = compare.perceptualHash()
                images[i]['code4'] = compare.colorCompare()
                images[i]['color'] = Image().getRgbaString(images[i]['path'])
                compare.end()
                # images[i]['code3'] = Compare.correlate2d()
            package_image.append(images)

        html = loader.load("demo.html") \
                     .generate(
                         images=images,
                         packages=packages,
                         package_image=package_image,
                         COMPARE_IMG=os.environ[config.STATIC_DIR] + os.environ[config.TEST_COMPARE_IMG]
                     )
        self.write(html)


class DemoSearchHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write(tornado.template.Loader(os.environ[config.TEMPLATE]).load("search.html").generate(
            name='search image result',
            action='upload_search'
        ))


class DemoUploadSearchHandler(tornado.web.RequestHandler):
    """
    TODO search test
    """

    def post(self):

        # from PIL import Image
        # from src.lib import Manage
        # from src.lib import Compare
        # import os
        # from src.lib import Image as ImageTool
        # try:
        if 1:
            os.chdir(os.environ[config.PROJECT_DIR] + "tests/tmp/")
            for i in glob.glob('*'):
                if '.py' not in i:
                    os.remove(i)
                    pass
            imagetool = Image()

            compare = Compare()
            imgfiles = self.request.files['file_img']
            if len(imgfiles) > 1:
                return self.write("error")
            imgfile = imgfiles[0]
            filename = imgfile['filename'].strip()
            import uuid
            filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
            tmp = os.environ[config.PROJECT_DIR] + "tests/tmp/"

            tmp_image = tmp + filename
            print tmp_image
            im.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)

            path = os.environ[config.PROJECT_DIR] + "tests/img/"
            # start compare imgs
            manage = Manage()
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
                    'code1': compare.basehash(),
                    'code2': compare.mse(),
                    'code3': compare.perceptualHash(),
                    'code4': compare.colorCompare(),
                    'color_package': compare.findSameColor(),
                    'code_mix': compare.mixHash(),
                    'color': imagetool.getRgbString(i),
                })
                compare.end()

            # ---------------------------------------------
            # simple sort list by code
            results_code1 = sorted(results, key=lambda k: k['code1'])
            results_code2 = sorted(results, key=lambda k: k['code2'])
            results_code3 = sorted(results, key=lambda k: k['code3'])
            results_code4 = sorted(results, key=lambda k: k['code4'])
            results_mix = sorted(results, key=lambda k: k['code_mix'])

            self.write(tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_result.html").generate(
                origin_img=filename,
                results_code1=results_code1,
                results_code2=results_code2,
                results_code3=results_code3,
                results_code4=results_code4,
                results_mix=results_mix,
            ))
        # except Exception, e:
        #     print e
        #     self.redirect('search')

class TestHandler(App):
    def get(self, *args, **kwargs):
        self.write(
            tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_test_upload.html").generate(
                name='search by index',
                action='search_test'
            )
        )

    def post(self, *args, **kwargs):
        '''
        search color test demo
        '''
        os.chdir(os.environ[config.PROJECT_DIR] + "tests/tmp/")
 
        imagetool = im
        compare = Compare()
        imgfiles = self.request.files['file_img']
        if len(imgfiles) > 1:
            return self.write("error")
        imgfile = imgfiles[0]
        filename = imgfile['filename'].strip()
        import uuid
        filename = str(uuid.uuid4()) + '.' + filename.split('.')[-1]
        tmp = os.environ[config.PROJECT_DIR] + "tests/tmp/"

        tmp_image = tmp + filename
        print tmp_image
        im.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)

        # path = os.environ[config.PROJECT_DIR] + "tests/img/"
        self.m.store_base_image_file(tmp_image)


        # 开始比对
        resultDict = Match(
            self.m
        ).get_match_result()
        
        print resultDict
        self.write(
            tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_test.html").generate(
                origin_img = '/tests/tmp/' + filename,
                results = resultDict
            )
        )

class DemoSearchColorHandler(tornado.web.RequestHandler):
    '''
    search color test demo
    '''

    def get(self, *args, **kwargs):
        self.write(tornado.template.Loader(os.environ[config.TEMPLATE]).load("search.html").generate(
            name='search image color result',
            action='upload_search_color'
        ))


class DemoUploadSearchColorHandler(tornado.web.RequestHandler):
    """
    TODO search test
    """
    def post(self):
        from src.lib.image import Image as ImageTool

        rgbList = ImageTool.rgb_list
        
        from src.service.feature import Feature as Compare


        imagetool = ImageTool()
        compare = Compare()
        imgfiles = self.request.files['file_img']

        if len(imgfiles) > 1:
            return self.write("error")
        imgfile = imgfiles[0]

        filename = imgfile['filename'].strip()

        tmp = os.environ[config.PROJECT_DIR] + "tests/tmp/"
        tmp_image = tmp + filename
        im.open(StringIO.StringIO(imgfile['body'])).save(tmp_image)
        filename = imgfile['filename'].strip()
        results = []

        list = Compare().findSameColor(
            ImageTool().getRgb(tmp_image),
            True
        )

        list = sorted(list, key=lambda k: k['score'])
        self.write(
            tornado.template.Loader(os.environ[config.TEMPLATE]).load("search_color_result.html").generate(
                origin_img=filename,
                origin_img_rgb=ImageTool().getRgbString(tmp_image),
                results=list,
            )
        )
        pass
