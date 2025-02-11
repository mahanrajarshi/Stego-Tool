import unittest
import os
from PIL import Image
import numpy as np
from stego import LSBSteganographer, SteganographyException

class TestLSBSteganography(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.clean_image = 'test_clean.png'
        cls.output_image = 'test_encoded.png'
        with Image.new('RGB', (100, 100), color='white') as img:
            img.save(cls.clean_image)

    @classmethod
    def tearDownClass(cls):
        for f in [cls.clean_image, cls.output_image, 'invalid_mode.png']:
            if os.path.exists(f):
                os.remove(f)

    def test_encode_decode(self):
        stego = LSBSteganographer()
        message = "Test%Message%123"
        stego.embed_data(self.clean_image, message, self.output_image, 0x1A)
        decoded = stego.extract_data(self.output_image, 0x1A)
        self.assertEqual(message, decoded)

    def test_invalid_image_mode(self):
        stego = LSBSteganographer()
        with self.assertRaises(SteganographyException):
            with Image.new('L', (100, 100), color='white') as img:
                img.save('invalid_mode.png')
            stego.embed_data('invalid_mode.png', "test", "invalid.jpg", 0x1A)

    def test_message_too_large(self):
        stego = LSBSteganographer()
        large_msg = "A" * 100000
        with self.assertRaises(SteganographyException):
            stego.embed_data(self.clean_image, large_msg, self.output_image, 0x1A)

    def test_corrupted_image(self):
        stego = LSBSteganographer()
        with open(self.output_image, 'wb') as f:
            f.write(b'invalid')
        with self.assertRaises(SteganographyException):
            stego.extract_data(self.output_image, 0x1A)

if __name__ == '__main__':
    unittest.main()
