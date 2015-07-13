# coding:utf-8


class Manage:
    def __init__(self):
        pass

    # ----------------------------------------------------------
    # get directory file list
    # ----------------------------------------------------------
    def getImageList(self, project_img_path, package_path):
        '''
        :param project_img_path:
        :param package_path:
        :return:
        '''
        import os
        imgList = []
        for dir_, _, files in os.walk(project_img_path):
            for fileName in files:
                imgList.append({"url": package_path + fileName,
                                "path": project_img_path + fileName,
                                })
        return imgList

    # ----------------------------------------------------------
    # return the package first file name
    # ----------------------------------------------------------
    def getFirst(self, project_img_path):
        '''
        :param project_img_path:
        :return:
        '''
        import os
        for dir_, _, files in os.walk(project_img_path):
            for fileName in files:
                return fileName
        return None

    # ----------------------------------------------------------
    # return path all file pull path name
    # ---------------------------------------------------------
    def getPathAllFile(self, PATH):
        '''
        :param PATH:
        :return:
        '''
        import os, glob

        pathList = []
        os.chdir(PATH)
        for i in glob.glob('*'):
            pathList.append(os.getcwd() + "/" + i)
        return pathList
