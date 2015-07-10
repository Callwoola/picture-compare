# coding:utf-8
from src.module.module import pc_module
from src.lib import Image as im


class RGB_module(pc_module):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "RGB_module"

    def compare(self):
        pass

    def get(self):
        return {"rgb":im.Image().getRgb(self.path),
                "name":"noname",
                ""
        }

