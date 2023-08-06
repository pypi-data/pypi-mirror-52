import testtools

import hellolib

class TestHello(testtools.TestCase):
    def test_say_hello_with_no_name(self):
        expected = "hello!"
        actual = hellolib.say_hello()
        self.assertEqual(expected, actual)

    def test_say_hello_with_a_name(self):
        expected = "hello, bob!"
        actual = hellolib.say_hello("bob")
        self.assertEqual(expected, actual)
