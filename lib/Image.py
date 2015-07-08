# coding:utf-8


class Image:
    def __init__(self):
        pass

    def getImageList(self, project_img_path, package_path):
        import os
        imgList = []
        print project_img_path
        for dir_, _, files in os.walk(project_img_path):
            print files
            for fileName in files:
                imgList.append({"url": package_path + fileName,
                                "path": project_img_path + fileName,
                                })
        return imgList


    def getFirst(self,project_img_path):
        import os
        for dir_, _, files in os.walk(project_img_path):
            for fileName in files:
                return fileName
        return None