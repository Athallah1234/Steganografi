import zlib
from PIL import Image
import numpy as np
from src.utils.logger import logger

class LSBSteg:
    MAGIC_SIG = b"AEGIS"  # Magic signature to identify steganographed images

    @staticmethod
    def encode(image_path: str, data: bytes, output_path: str, progress_callback=None):
        """Encodes binary data into an image using LSB."""
        try:
            # Compress data
            compressed_data = zlib.compress(data)
            
            # Prepare payload: MAGIC_SIG + Length (4 bytes) + compressed_data
            payload = LSBSteg.MAGIC_SIG + len(compressed_data).to_bytes(4, 'big') + compressed_data
            
            # Load image
            img = Image.open(image_path).convert('RGBA')
            pixels = np.array(img)
            
            # Check capacity
            max_bytes = (pixels.size * 1) // 8  # 1 bit per subpixel
            if len(payload) > max_bytes:
                raise ValueError(f"Message too large! Max capacity: {max_bytes} bytes, Payload: {len(payload)} bytes")

            # Flatten pixels
            flat_pixels = pixels.flatten()
            
            # Convert payload to bits
            bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
            
            # Embed bits (LSB)
            # Use vectorized operation for speed
            flat_pixels[:len(bits)] = (flat_pixels[:len(bits)] & np.uint8(254)) | bits
            
            # Reshape and save
            new_pixels = flat_pixels.reshape(pixels.shape)
            new_img = Image.fromarray(new_pixels.astype(np.uint8), 'RGBA')
            new_img.save(output_path, "PNG")
            
            logger.info(f"Successfully encoded {len(payload)} bytes into {output_path}")
            if progress_callback: progress_callback(100)
            
        except Exception as e:
            logger.error(f"Encoding error: {e}")
            raise

    @staticmethod
    def decode(image_path: str, progress_callback=None) -> bytes:
        """Decodes binary data from an image."""
        try:
            img = Image.open(image_path).convert('RGBA')
            pixels = np.array(img)
            flat_pixels = pixels.flatten()
            
            # Extract magic signature first (5 bytes = 40 bits)
            sig_bits = flat_pixels[:40] & 1
            sig = np.packbits(sig_bits).tobytes()
            
            if sig != LSBSteg.MAGIC_SIG:
                raise ValueError("This image does not contain a valid AegisVault message.")
            
            # Extract length (4 bytes = 32 bits after sig)
            len_bits = flat_pixels[40:72] & 1
            payload_len = int.from_bytes(np.packbits(len_bits).tobytes(), 'big')
            
            # Extract compressed data
            total_bits = 72 + (payload_len * 8)
            if total_bits > flat_pixels.size:
                raise ValueError("Invalid message length or corrupted image.")
                
            data_bits = flat_pixels[72:total_bits] & 1
            compressed_data = np.packbits(data_bits).tobytes()
            
            # Decompress
            data = zlib.decompress(compressed_data)
            
            logger.info(f"Successfully decoded {len(data)} bytes from {image_path}")
            if progress_callback: progress_callback(100)
            return data
            
        except Exception as e:
            logger.error(f"Decoding error: {e}")
            raise
