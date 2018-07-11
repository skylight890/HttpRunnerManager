# encoding: utf-8

import sys

from HikCentral.base import *
from HikCentral.logger import *
from HikCentral import exception

log = LogRecord()

class runner(object):
    def __init__(self):
        self.test_group = TestGroup()

        if self.test_group.loginVsm() == -1:
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
                    "data": [],
                },
                "variable": {
                    "var1": "$var1",
                    "var2": "var2",
                },
                "extractor":[
                    {"ID": "Data.AreaList.Area.ID"},
                ],
                "validator":[
                    {
                        "check": "expect",
                        "comparator": "comparator",
                        "expect": "expect"
                    },
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
            # testcase_name = testcase.pop('name')
            template = testcase.pop("template", None)
            data = testcase.pop("data", None)
            print('running testcase...')
            print(url + method + template + str(data))

            response = self.test_group.sendRequest(0, url, method, '', 1, template, data, {}, {}, {})

        except KeyError:
            raise exception.ParamsError("URL or METHOD missed!")


    def parse_testcase(self, testcase):
        request = testcase.get('request', None)
        return request


if __name__== '__main__':
    testcase = {
        "name": "testcase_name_test",
        "setup_hook": "setup",
        "request": {
            "url": "/ISAPI/Bumblebee/System/SystemProperties",
            "method": "PUT",
            "template": "test",
            "data": ['VSM1_FrameTest'],
        },
        "variable": {
            "var1": "$var1",
            "var2": "var2",
        },
        "extract": "extract",
        "validator": [
            {
                "check": "expect",
                "comparator": "comparator",
                "expect": "expect",
            },
        ],
        "teardown_hook": "teardown_hook",
    }

    runner = runner()
    runner.run_test(testcase)