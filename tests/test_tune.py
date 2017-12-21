import unittest
import os
import shutil
from autotune.tuner import RandomSearch
from autotune.spec import Spec
import json


test_dir = os.path.join(os.getcwd(), 'unittest_tmp')
this_dir = os.path.dirname(os.path.abspath(__file__))


class TestTune(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(test_dir):
            os.makedirs(test_dir)
        self.config = Spec.load(os.path.join(this_dir, 'test.config'))

    def tearDown(self):
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)

    def test_no_gpu(self):
        tuner = RandomSearch(os.path.join(this_dir, 'executable.py'), self.config)
        tuner.tune(2, out=test_dir, wait_seconds=0)

        for i in [0, 1]:
            fname = os.path.join(test_dir, str(i))
            for ext in ['.err', '.json', '.out']:
                self.assertTrue(os.path.isfile(fname + ext))
            with open(fname + '.json') as f:
                d = json.load(f)
                for k in ['command', 'params', 'pid']:
                    self.assertIn(k, d)
                self.assertNotIn('gpu', d)
                for k in ['foo', 'bar']:
                    self.assertIn(k, d['params'])
                foo = str(d['params']['foo'])
                bar = str(d['params']['bar'])

            with open(fname + '.out') as f:
                self.assertEqual(foo, f.read().strip())
            with open(fname + '.err') as f:
                self.assertEqual(bar, f.read().strip())

    def test_gpu(self):
        tuner = RandomSearch(os.path.join(this_dir, 'executable.py'), self.config)
        tuner.tune(2, out=test_dir, wait_seconds=0)

        for i in [0, 1]:
            fname = os.path.join(test_dir, str(i))
            for ext in ['.err', '.json', '.out']:
                self.assertTrue(os.path.isfile(fname + ext))
            with open(fname + '.json') as f:
                d = json.load(f)
                for k in ['command', 'params', 'pid']:
                    self.assertIn(k, d)
                for k in ['foo', 'bar']:
                    self.assertIn(k, d['params'])
                foo = str(d['params']['foo'])
                bar = str(d['params']['bar'])

            with open(fname + '.out') as f:
                self.assertEqual(foo, f.read().strip())
            with open(fname + '.err') as f:
                self.assertEqual(bar, f.read().strip())
