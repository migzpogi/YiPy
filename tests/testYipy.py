import unittest
from YiPyMain import load_rss


class TestYipyMain(unittest.TestCase):

    def testLoadRSS(self):
        yts_rss = load_rss('sample.xml')
        self.assertEqual(yts_rss.feed.title, 'YTS RSS')


if __name__ == '__main__':
    unittest.main()

# TODO exclude sample.xml in git push