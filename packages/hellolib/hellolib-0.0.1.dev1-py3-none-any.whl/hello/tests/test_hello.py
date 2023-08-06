import testtools

import hello

class TestHello(testtools.TestCase):
    def test_say_hello_with_no_name(self):
        expected = "hello!"
        actual = hello.say_hello()
        self.assertEqual(expected, actual)

    def test_say_hello_with_a_name(self):
        expected = "hello, bob!"
        actual = hello.say_hello("bob")
        self.assertEqual(expected, actual)
