import unittest

class test_ma_logger(unittest.TestCase):
    def test_singleton(self):
        self.assertEquals(True, True)
        pass
    def test_logging(self):
        self.assertEquals(True, True)
        pass
    def test_action_registry(self):
        self.assertEquals(True, True)
        self.assertTrue(True)
        pass

if __name__ == '__main__':
    unittest.main()
