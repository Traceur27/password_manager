import cryptopp
import base64


class EncryptorMixIn:
    """
    Obiekt szyfrujący
    """
    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        """
        str plain data -> base64 encrypted data
        """
        return self.doEncrypt(data, self.key)

    def decrypt(self, data):
        """
        base64 encrypted data -> str plain data
        """
        return base64.b64decode(self.doDecrypt(
            base64.b64decode(data), self.key))


def get_crypto_object(algorithm_name, key):
    """
    Zwraca obiekt obsługującą zadany algortym
    @algorithm_name - nazwa algortymu
    @key - klucz szyfrujący

    @return EncryptorMixIn
    """
    encryptor = EncryptorMixIn(key)
    if "xor" in algorithm_name:
        setattr(encryptor, 'doEncrypt', cryptopp.passwordXor)
        setattr(encryptor, 'doDecrypt', cryptopp.passwordXor)
    elif "rc4" in algorithm_name:
        setattr(encryptor, 'doEncrypt', cryptopp.passwordRC4)
        setattr(encryptor, 'doDecrypt', cryptopp.passwordRC4)
    else:
        setattr(encryptor, 'doEncrypt', cryptopp.passwordPlain)
        setattr(encryptor, 'doDecrypt', cryptopp.passwordPlain)
    return encryptor

