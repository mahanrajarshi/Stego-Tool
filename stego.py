from PIL import Image
import numpy as np
import binascii

class SteganographyException(Exception):
    pass

class LSBSteganographer:
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.image = None
        self.width = 0
        self.height = 0
        
    def load_image(self, image_path):
        try:
            self.image = Image.open(image_path)
            self.width, self.height = self.image.size
            return self.image
        except Exception as e:
            raise SteganographyException(f"Error loading image: {str(e)}")

    def _encode_message(self, message, key=0x1A):
        message += "%%%"  # Add terminator
        binary = ''.join(format(ord(c) ^ key, '08b') for c in message)
        return binary

    def _decode_message(self, binary, key=0x1A):
        bytes_data = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                bytes_data.append(int(byte, 2) ^ key)
        
        try:
            message = ''.join(chr(b) for b in bytes_data)
            if "%%%" in message:
                return message.split("%%%")[0]
            raise SteganographyException("No termination sequence found")
        except Exception:
            raise SteganographyException("Invalid data extracted")

    def embed_data(self, image_path, message, output_path, key=None):
        img = self.load_image(image_path)
        if img.mode not in ('RGB', 'RGBA'):
            raise SteganographyException("Image mode must be RGB/RGBA")
            
        binary_message = self._encode_message(message, key)
        total_bits = len(binary_message)
        available_bits = img.size[0] * img.size[1] * 3  # 3 channels
        
        if total_bits > available_bits:
            raise SteganographyException(f"Message too large ({total_bits} bits > {available_bits} available)")
            
        # Convert image to numpy array
        data = np.array(img)
        height, width = data.shape[:2]
        
        # Embed message bits
        idx = 0
        for h in range(height):
            for w in range(width):
                for c in range(3):  # RGB channels
                    if idx < total_bits:
                        # Clear LSB and set it to message bit
                        data[h, w, c] = (data[h, w, c] & ~1) | int(binary_message[idx])
                        idx += 1
                    else:
                        break
        
        # Save modified image
        result = Image.fromarray(data)
        result.save(output_path, "PNG")
        return output_path

    def extract_data(self, image_path, key=None):
        img = self.load_image(image_path)
        data = np.array(img)
        height, width = data.shape[:2]
        
        # Extract bits
        binary = []
        for h in range(height):
            for w in range(width):
                for c in range(3):  # RGB channels
                    bit = data[h, w, c] & 1
                    binary.append(str(bit))
                    
                    # Try to decode every 8 bits
                    if len(binary) % 8 == 0:
                        try:
                            message = self._decode_message(''.join(binary), key)
                            return message
                        except SteganographyException:
                            continue
        
        raise SteganographyException("No valid message found")