import unittest

import headlesschrome

class TestHeadlessChrome(unittest.TestCase):

    def test_success(self):
        c = headlesschrome.Client()
        result = c.capture('http://example.com')
        self.assertIn('har', result)

    def test_timeout(self):
        c = headlesschrome.Client(timeout=1)
        with self.assertRaisesRegex(RuntimeError, 'Timeout'):
            result = c.capture('http://wsj.com')

if __name__ == '__main__':
    unittest.main()
