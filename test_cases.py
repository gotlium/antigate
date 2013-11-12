import unittest
import os

from antigate import AntiGate

API_KEY = "5407a05a14762a7413723d478cb10096"
IMAGE1 = "captcha/123.jpg"
IMAGE2 = "captcha/456.jpg"


class TestAnigateCase(unittest.TestCase):
    def test_balance(self):
        self.assertTrue(AntiGate(API_KEY).balance() > 0)

    def test_stats(self):
        self.assertTrue(len(AntiGate(API_KEY).stats()) > 0)

    def test_load(self):
        self.assertEqual(len(AntiGate(API_KEY).load()), 4)

    def test_base(self):
        self.assertEqual(str(AntiGate(API_KEY, IMAGE1)), '123')

    def test_abuse(self):
        gate = AntiGate(API_KEY, IMAGE1)
        if str(gate) != 'qwerty':
            self.assertTrue(gate.abuse())

    def test_manual(self):
        gate = AntiGate(API_KEY, auto_run=False)

        captcha_id = gate.send(IMAGE1)
        self.assertTrue(str(captcha_id).isdigit())

        captcha_value = gate.get(captcha_id)
        self.assertEqual(str(captcha_value), '123')

    def test_multiple(self):
        gate = AntiGate(API_KEY, auto_run=False)
        captcha_id1 = gate.send(IMAGE1)
        captcha_id2 = gate.send(IMAGE2)

        self.assertTrue(str(captcha_id1).isdigit())
        self.assertTrue(str(captcha_id2).isdigit())

        results = gate.get_multi([captcha_id1, captcha_id2])

        #self.assertListEqual(results, ['123', '456'])
        self.assertTrue(results == ['123', '456'])


if __name__ == '__main__':
    unittest.main()
