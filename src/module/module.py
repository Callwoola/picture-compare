# coding:utf-8
class pc_module(object):
    """often listing the methods you're expected to supply
    Must be tells you it's abstract,
    often listing the methods you're expected to supply."""

    def __init__(self, path):
        raise NotImplementedError("Should have implemented this __init__ ")

    def init(self):
        pass

    def get(self):
        raise NotImplementedError("Should have implemented this get()")
