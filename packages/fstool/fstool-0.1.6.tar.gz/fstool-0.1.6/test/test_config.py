import unittest

from fstool import _config as config


class TestConfig(unittest.TestCase):

    def test_get_regex_ratio(self):
        self.assertAlmostEqual(config._get_regex_ratio('hi .'), 1/4)
        self.assertAlmostEqual(config._get_regex_ratio('hi .+'), 2/5)
        self.assertAlmostEqual(config._get_regex_ratio('hi . .'), 2/6)


if __name__ == '__main__':
    unittest.main()
