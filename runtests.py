# coding:utf-8

import importlib

if __name__ == "__main__":
    from server import config_yaml
    config_yaml()
    
    for testcase in [
        'tests.test_base'
    ]:
        __instance = importlib.import_module(testcase)       
        __instance.main()
