import unittest

from bitmap import Bitmap


class BitmapTest(unittest.TestCase):

    def test_init(self):
        bitmap = Bitmap()
        self.assertEqual(len(bitmap), 1)
        self.assertEqual(bitmap.value, 0)

    def test_size_init(self):
        bitmap = Bitmap(size=10)
        self.assertEqual(len(bitmap), 10)
        self.assertEqual(bitmap.value, 0)

    def test_value_init(self):
        bitmap = Bitmap(value=10)
        self.assertEqual(len(bitmap), 4)
        self.assertEqual(bitmap.value, 10)
        bitmap = Bitmap(size=0, value=14)
        self.assertEqual(len(bitmap), 4)
        self.assertEqual(bitmap.value, 14)

    def test_size_value_init(self):
        bitmap = Bitmap(size=10, value=10)
        self.assertEqual(len(bitmap), 10)
        self.assertEqual(bitmap.value, 10)

    def test_value_setter(self):
        bitmap = Bitmap(value=10)
        bitmap.value = 7
        self.assertEqual(bitmap.value, 7)

    def test_get_bit(self):
        bitmap = Bitmap(value=10)
        self.assertEqual(bitmap.get_bit(2), 0)
        self.assertEqual(bitmap.get_bit(1), 1)

    def test_set_bit(self):
        bitmap = Bitmap(value=10)
        bitmap.set_bit(2)
        self.assertEqual(bitmap.get_bit(2), 1)
        self.assertEqual(bitmap.value, 14)

    def test_clear_bit(self):
        bitmap = Bitmap(value=10)
        bitmap.clear_bit(1)
        self.assertEqual(bitmap.get_bit(2), 0)
        self.assertEqual(bitmap.value, 8)

    def test_flip_bit(self):
        bitmap = Bitmap(value=10)
        bitmap.flip_bit(2)
        bitmap.flip_bit(1)
        self.assertEqual(bitmap.get_bit(2), 1)
        self.assertEqual(bitmap.get_bit(1), 0)
        self.assertEqual(bitmap.value, 12)

    def test_update_bit(self):
        bitmap = Bitmap(value=10)
        # `True` and `1` are equivalent in the bitmap
        # bit was already 1
        bitmap.update_bit(3, 1)
        self.assertEqual(bitmap.get_bit(3), 1)
        # new bit set to 1
        bitmap.update_bit(2, True)
        self.assertEqual(bitmap.get_bit(2), 1)
        # `False` and `0` are equivalent in the bitmap
        # new bit set to 0
        bitmap.update_bit(1, False)
        self.assertEqual(bitmap.get_bit(1), 0)
        # bit was already 1
        bitmap.update_bit(0, 0)
        self.assertEqual(bitmap.get_bit(0), 0)
        self.assertEqual(bitmap.value, 12)

    def test_invalid_value(self):
        bitmap = Bitmap(size=10, value=10)
        with self.assertRaises(TypeError):
            bitmap.value = 7.0
        with self.assertRaises(TypeError):
            bitmap.value = '0b111'
        with self.assertRaises(TypeError):
            bitmap.value = [7]
        # value < 0
        with self.assertRaises(ValueError):
            bitmap.value = -1
        # value >= (1 << size)
        with self.assertRaises(ValueError):
            bitmap.value = 1024
        with self.assertRaises(TypeError):
            _ = Bitmap(value=(10,))

    def test_invalid_size(self):
        with self.assertRaises(TypeError):
            _ = Bitmap(size=7.0)
        with self.assertRaises(TypeError):
            _ = Bitmap(size='0b111')
        with self.assertRaises(TypeError):
            _ = Bitmap(size=[7])
        # size < len(bin(value))
        with self.assertRaises(ValueError):
            _ = Bitmap(size=3, value=10)

    def test_invalid_i(self):
        bitmap = Bitmap(size=10, value=10)
        with self.assertRaises(TypeError):
            _ = bitmap.get_bit(2.0)
        with self.assertRaises(TypeError):
            bitmap.set_bit('0b0010')
        with self.assertRaises(TypeError):
            bitmap.clear_bit([2])
        # i < 0
        with self.assertRaises(ValueError):
            bitmap.flip_bit(-1)
        # i >= size
        with self.assertRaises(ValueError):
            _ = bitmap.get_bit(10)   

    def test_invalid_v(self):
        bitmap = Bitmap(value=10)
        with self.assertRaises(ValueError):
            bitmap.update_bit(2, 2)
        with self.assertRaises(ValueError):
            bitmap.update_bit(1, None)
        with self.assertRaises(ValueError):
            bitmap.update_bit(0, '1')


if __name__ == '__main__':
    unittest.main()
