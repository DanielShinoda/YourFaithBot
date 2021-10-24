import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)
        return

def habitCollectionSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestStringMethods('test_isupper'))
    suite.addTest(TestStringMethods('test_split'))
    return suite

if __name__ == '__main__':
    unittest.main()
    #runner = unittest.TextTestRunner()
    #runner.run(habitCollectionSuite())
    #runner.run(habitCollectionSuite())
