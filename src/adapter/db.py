from tinydb import TinyDB, where


class pcDB:
    def __init__(self,table="default"):
        #'/path/to/db.json'
        path=''
        self.table=table
        self.db = TinyDB(path).table(table)
    def insert(self,_dict):
        '''
        :return:
        '''
        self.db.insert(_dict)
        # db.insert({'int': 1, 'char': 'a'})
        # db.insert({'int': 1, 'char': 'b'})
        pass
    def getAll(self):
        '''
        not param just get all data
        :return:
        '''
        return self.db.all()
        #db.search()
        pass
    pass
#
# from tinydb.storages import JSONStorage
# from tinydb.middlewares import CachingMiddleware
# db = TinyDB('/path/to/db.json', storage=CachingMiddleware(JSONStorage))