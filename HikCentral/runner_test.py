# encoding: utf-8

import sys
from .base import *
from .logger import *
from HikCentral import exception

log = LogRecord()

class runner(object):
    def __init__(self):
        self.test_group = TestGroup()

        if self.test_group.logoutVsm() == -1:
            log.log_error('Failed to login!')
            print('Failed to login')
            sys.exit()

    def run_test(self, testcase):
        ''' 执行测试用例，
        测试用例的格式为：
        testcase:
            {
                "name": "name",
                "setup_hook": "setup",
                "request": {
                    "url": "url",
                    "method": "POST",
                    "template": "template",
                    "data": "data",
                },
                "variable": {
                    "var1": "$var1",
                    "var2": "var2",
                },
                "extract": "extract",
                "validator":[
                    {
                        "check": "expect",
                        "comparator": "comparator",
                        "expect“: "expect"
                    }
                ],
                "teardown_hook": "teardown_hook",
            }

        :param testcase: json格式的测试用例
        :return:
        '''
        testcase = self.parse_testcase(testcase)

        try:
            url = testcase.pop('url')
            method = testcase.pop('method')
            group_name = testcase.pop("group", None)
        except KeyError:
            raise exception.ParamsError("URL or METHOD missed!")


    def parse_testcase(self, testcase):
        request = testcase.get('request', None)