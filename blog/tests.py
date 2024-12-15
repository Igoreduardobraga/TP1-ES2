from django.test import TestCase

class AlwaysFailTest(TestCase):
    def test_always_fails(self):
        self.fail("This test is designed to always fail.")
