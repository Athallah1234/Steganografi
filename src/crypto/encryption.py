import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from src.utils.logger import logger

class EncryptionManager:
    @staticmethod
    def generate_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
        """Generate a Fernet key from a password and salt."""
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt

    @staticmethod
    def encrypt(message: str, password: str) -> bytes:
        """Encrypt message with password. Returns salt + encrypted_data."""
        try:
            key, salt = EncryptionManager.generate_key(password)
            f = Fernet(key)
            encrypted_data = f.encrypt(message.encode())
            # Prepend salt to the encrypted data (16 bytes)
            return salt + encrypted_data
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    @staticmethod
    def decrypt(data: bytes, password: str) -> str:
        """Decrypt data with password. Expects salt in the first 16 bytes."""
        try:
            salt = data[:16]
            encrypted_payload = data[16:]
            key, _ = EncryptionManager.generate_key(password, salt)
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_payload)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Incorrect password or corrupted data.")
