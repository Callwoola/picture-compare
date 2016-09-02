# coding:utf-8
if __name__ == "__main__":
    for testcase in [
        'tests.test_base'
    ]:
        print testcase
        _instance = __import__(testcase)
#        print _instance
        _instance.main()
