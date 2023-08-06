# coding: utf-8

# The MIT License (MIT)

# Copyright (c) 2019 Martin Bammer, mrbm74 at gmail dot com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software - recordclass library - and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom
# the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import base64

#from cryptography.fernet import Fernet -> We do not want base64 encoded data Thus we implement our own Fernet class
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature


class InvalidToken(Exception):
    pass


class Fernet(object):

    def __init__(self, key, backend=None):
        if backend is None:
            backend = default_backend()
        key = base64.urlsafe_b64decode(key)
        if len(key) != 32:
            raise ValueError("Fernet key must be 32 url-safe base64-encoded bytes.")
        self._signing_key = key[:16]
        self._encryption_key = key[16:]
        self._backend = backend

    def encrypt(self, data: bytes) -> bytes:
        iv: bytes = os.urandom(16)  # 16 bytes
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend).encryptor()
        ciphertext: bytes = encryptor.update(padded_data) + encryptor.finalize()  # 16 bytes
        basic_parts = iv + ciphertext
        h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
        h.update(basic_parts)
        return basic_parts + h.finalize()

    def decrypt(self, data: bytes) -> bytes:
        # Verify signature
        h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
        h.update(data[:-32])
        try:
            h.verify(data[-32:])
        except InvalidSignature:
            raise InvalidToken
        # Decrypt
        iv = data[:16]
        ciphertext = data[16:-32]
        decryptor = Cipher(algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend).decryptor()
        plaintext_padded = decryptor.update(ciphertext)
        try:
            plaintext_padded += decryptor.finalize()
        except ValueError:
            raise InvalidToken
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded = unpadder.update(plaintext_padded)
        try:
            unpadded += unpadder.finalize()
        except ValueError:
            raise InvalidToken
        return unpadded


class Plugin(object):

    def __init__(self, password: bytes) -> None:
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, data: bytes) -> bytes:
        return Fernet(self.key).encrypt(data)

    def decrypt(self, encData: bytes) -> bytes:
        return Fernet(self.key).decrypt(encData)


if __name__ == "__main__":
    password = b"password"
    c = Plugin(password)
    encData = c.encrypt(b"HELLO")
    print(encData)
    print(c.decrypt(encData))
