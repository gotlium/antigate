import unittest
from collections import OrderedDict
from base64 import b64encode

from antigate import AntiGate

API_KEY = "026a028a057848761cad3a3638ae3eb7"
IMAGE1 = "captcha/123.jpg"
IMAGE2 = "captcha/456.jpg"


class TestAnigateCase(unittest.TestCase):
    def test_balance(self):
        balance = AntiGate(API_KEY).balance()
        self.assertTrue(balance > 0.0)
        self.assertEqual(type(balance), float)

    def test_stats(self):
        stats = AntiGate(API_KEY).stats()
        self.assertTrue(len(stats) > 0)
        self.assertEqual(type(stats), list)
        self.assertEqual(type(stats[0]), OrderedDict)

    def test_load(self):
        load = AntiGate(API_KEY).load()
        self.assertTrue(len(load) > 0)
        self.assertEqual(type(load), OrderedDict)
        self.assertTrue(load.get('load') is not None)

    def test_base(self):
        self.assertEqual(str(AntiGate(API_KEY, IMAGE1)), '123')

    def test_base_binary(self):
        fp = open(IMAGE1, 'rb')
        self.assertEqual(str(AntiGate(API_KEY, fp.read())), '123')
        fp.close()

    def test_base64(self):
        fp = open(IMAGE1, 'rb')
        self.assertEqual(str(AntiGate(API_KEY, b64encode(fp.read()))), '123')
        fp.close()

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

    def test_manual_binary(self):
        gate = AntiGate(API_KEY, auto_run=False)
        fp = open(IMAGE1, 'rb')
        captcha_id = gate.send(b64encode(fp.read()))
        self.assertTrue(str(captcha_id).isdigit())
        fp.close()

        captcha_value = gate.get(captcha_id)
        self.assertEqual(str(captcha_value), '123')

    def test_manual_base64(self):
        gate = AntiGate(API_KEY, auto_run=False)
        fp = open(IMAGE1, 'rb')
        captcha_id = gate.send(fp.read())
        self.assertTrue(str(captcha_id).isdigit())
        fp.close()

        captcha_value = gate.get(captcha_id)
        self.assertEqual(str(captcha_value), '123')

    def test_multiple(self):
        gate = AntiGate(API_KEY, auto_run=False)
        captcha_id1 = gate.send(IMAGE1)
        captcha_id2 = gate.send(IMAGE2)

        self.assertTrue(str(captcha_id1).isdigit())
        self.assertTrue(str(captcha_id2).isdigit())

        results = gate.get_multi([captcha_id1, captcha_id2])
        self.assertTrue(results == ['123', '456'])

    def test_multiple_binary(self):
        gate = AntiGate(API_KEY, auto_run=False)
        fp1 = open(IMAGE1, 'rb')
        fp2 = open(IMAGE2, 'rb')
        captcha_id1 = gate.send(fp1.read())
        captcha_id2 = gate.send(fp2.read())
        fp1.close()
        fp2.close()

        self.assertTrue(str(captcha_id1).isdigit())
        self.assertTrue(str(captcha_id2).isdigit())

        results = gate.get_multi([captcha_id1, captcha_id2])
        self.assertTrue(results == ['123', '456'])

    def test_multiple_base64(self):
        gate = AntiGate(API_KEY, auto_run=False)
        fp1 = open(IMAGE1, 'rb')
        fp2 = open(IMAGE2, 'rb')
        captcha_id1 = gate.send(b64encode(fp1.read()))
        captcha_id2 = gate.send(b64encode(fp2.read()))
        fp1.close()
        fp2.close()

        self.assertTrue(str(captcha_id1).isdigit())
        self.assertTrue(str(captcha_id2).isdigit())

        results = gate.get_multi([captcha_id1, captcha_id2])
        self.assertTrue(results == ['123', '456'])


if __name__ == '__main__':
    unittest.main()
