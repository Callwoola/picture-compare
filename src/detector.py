# coding:utf-8

# define a base detector Image paser for module
class Detector:
    _weight = 1
    def match(self, source, target):
        source_path = source.get_path()
        target_path = target.get_path()
        
    def do_screening(self):
        raise Exception('You must rewrite the do screening function!!')
    
    def get_score(self):
        return self.do_screening()

