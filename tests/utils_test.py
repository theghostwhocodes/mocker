import os
import unittest

import mocker.utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.data_path = './tests/data'

    def test_compute_file_path_for_get(self):
        path = '/test'
        command = 'GET'
        file_path = mocker.utils.compute_file_path(self.data_path, path, command)
        desired_file_path = os.path.join(
            os.getcwd(),
            'tests',
            'data',
            'test.GET.json'
        )
        self.assertEqual(file_path, desired_file_path)

    def test_load_mock(self):
        path = '/test'
        command = 'GET'
        file_path = mocker.utils.compute_file_path(self.data_path, path, command)
        content = mocker.utils.load_mock(file_path)
        self.assertDictEqual(
            content,
            {
                'response': {
                    'body': {
                        'key': 'value in new format'
                    },
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'status': 200
                }
            }
        )
