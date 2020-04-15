#!/usr/bin/env python
# -*- coding: utf-8 -*-

import HTMLTestRunner
import requests
import os
import time
import unittest


# 封装requests库的get和post请求方法为一个自定义类
class Connection:
    def __init__(self, host, port=8080):
        self.base_url = 'http://%s:%d' % (host, port)
        self.session = requests.session()

    def get(self, url, params=None, headers=None):
        if headers is None:
            headers = {}
        response = self.session.get(
            self.base_url + url, params=params, headers=headers)
        return response

    def post(self, url, data, headers=None):
        if headers is None:
            headers = {}
        response = self.session.post(
            self.base_url + url, data=data, headers=headers)
        return response

    # 清理资源，关闭会话
    def close(self):
        self.session.close()


# 构造一个针对Agileone的测试类
class Agileone(unittest.TestCase):
    """Agileone接口测试示例"""

    con = None

    @classmethod
    def setUpClass(cls):
        cls.con = Connection('192.168.248.131')

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_01_access_agileone(self):
        """打开woniusales网站主页"""
        resp = self.con.get('/woniusales/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual('OK', resp.reason)
        self.assertIn('成都市孵化园旗舰店',
                      resp.content.decode('utf-8'))

    def test_02_login_agileone(self):
        """登录woniusales网站"""
        test_data = [{'username': '', 'password': '', 'verifycode': '0000'},
                     {'username': 'a', 'password': '', 'verifycode': '0000'},
                     {'username': 'admin', 'password': '1a',
                      'verifycode': '0000'},
                     {'username': 'ab', 'password': 'admin',
                      'verifycode': '0000'},
                     {'username': 'admin', 'password': 'Milor123',
                      'verifycode': '0000'}]
        for params in test_data:
            resp = self.con.post('/woniusales/user/login', params)
            self.assertEqual(200, resp.status_code)
            self.assertEqual('OK', resp.reason)
            if params['username'] == 'admin' and params['password'] == 'Milor123':
                self.assertEqual('login-pass', resp.text)
            elif params['username'] == 'admin' and\
                    params['password'] != 'admin':
                self.assertEqual('password_invalid', resp.text)
            else:
                self.assertEqual('user_invalid', resp.text)

   
       

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Agileone)
    now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    report_path = os.path.join(os.getcwd(), 'report')
    if not os.path.exists(report_path):
        os.makedirs(report_path)
    report = os.path.join(report_path, 'agileone_test_report_%s.html' % now)
    with open(report, "w", encoding='utf8') as f:
        runner = HTMLTestRunner.HTMLTestRunner(title='agileone',
                                               description='Test Report',
                                               stream=f, verbosity=2)
        runner.run(suite)

