import os
import unittest

import mocker.utils


class TestUtils(unittest.TestCase):
    def test_compute_file_path_for_get(self):
        data_path = './data'
        path = '/prova'
        command = 'GET'
        file_path = mocker.utils.compute_file_path(data_path, path, command)
        desired_file_path = os.path.join(
            os.getcwd(),
            'data',
            'prova.GET.json'
        )
        self.assertEqual(file_path, desired_file_path)

    def test_load_mock(self):
        data_path = './data'
        path = '/prova'
        command = 'GET'
        file_path = mocker.utils.compute_file_path(data_path, path, command)
        content = mocker.utils.load_mock(file_path)
        self.assertEqual(content, b'{\n    "key": "value"\n}\n')
