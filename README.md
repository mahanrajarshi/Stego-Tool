# Secure Image Steganography Implementation

A research-level implementation of steganography for secure image transmission. This project uses the Least Significant Bit (LSB) technique combined with XOR encryption to hide and extract messages within PNG images.

## Features

- LSB-based steganography for secure message hiding
- XOR encryption for additional security
- Web interface for easy interaction
- Support for PNG image format
- Input validation and error handling
- Secure file handling with automatic cleanup

## Architecture

### Core Components

1. **Steganography Engine (stego.py)**
   - LSB encoding/decoding implementation
   - XOR encryption/decryption
   - Image processing using PIL and NumPy
   - Comprehensive error handling

2. **Web Interface (app.py)**
   - Flask-based web server
   - File upload/download handling
   - User-friendly interface
   - Security validations

### Security Features

- File type validation (PNG only)
- 2MB file size limit
- XOR encryption with custom keys
- Secure temporary file handling
- Input sanitization
- Termination sequence for message integrity

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the web server:
```bash
python app.py
```

2. Access the web interface at http://localhost:5000

### Encoding a Message

1. Click "Encode Message"
2. Upload a PNG image
3. Enter your secret message
4. Provide an encryption key (hex or decimal)
5. Click "Encode Message"
6. Download the encoded image

### Decoding a Message

1. Click "Decode Message"
2. Upload the encoded PNG image
3. Enter the same encryption key used for encoding
4. Click "Extract Message"
5. View the extracted message

## Technical Details

### LSB Steganography

The implementation uses the least significant bit of each color channel (RGB) in the image pixels to store the message bits. This ensures minimal visual impact while providing sufficient capacity for message storage.

### Message Format

- Messages are terminated with "%%%" sequence
- Each character is XOR encrypted before encoding
- Binary data is distributed across RGB channels

### Capacity

Maximum message size depends on image dimensions:
- Each pixel provides 3 bits (RGB channels)
- Total capacity = width × height × 3 bits

## Testing

Run the test suite:
```bash
python test_stego.py -v
```

Tests cover:
- Message encoding/decoding
- Invalid image handling
- Message size validation
- Error scenarios
- File handling

## Research Value

This implementation demonstrates:
- Modern steganography techniques
- Practical security considerations
- Balance of security and usability
- Error handling best practices
- Clean code architecture

## Future Enhancements

- Additional image format support
- Advanced encryption options
- Compression for larger messages
- Statistical analysis resistance
- Mobile device support

## Requirements

- Python 3.10+
- PIL/Pillow 10.3.0
- NumPy 1.26.4
- Flask 3.0.2

## License

MIT License - Free to use and modify