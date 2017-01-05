"""
Moduł pomocniczy implementujący fabrykę algorytmów szyfrujących
"""
import cryptopp
import base64
from collections import namedtuple

algorithms = {}


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
        data = base64.b64decode(self.doDecrypt(base64.b64decode(data), self.key))
        return data.decode()


AlgorithmDescription = namedtuple("AlgorithmDescription", [
    "name",
    "verbose_name",
    "encryption_function",
    "decryption_function"])


def register_algorithm(name, verbose_name, encryption_function,
                       decryption_function):
    """
    Rejestruje nowy algorytm w fabryce
    Algorytm jest rozpoznawany po nazwie skróconej

    :param name: nazwa skrócona
    :param verbose_name: nazwa
    :param encryption_function: funkcja szyfrująca
    :param decryption_function: funkcja deszyfrująca
    """
    algorithms[name] = AlgorithmDescription(
        name=name,
        verbose_name=verbose_name,
        encryption_function=encryption_function,
        decryption_function=decryption_function)


def get_algorithm(name):
    """
    Zwraca algorytm z fabryki

    :param name: nazwa skrócona algorytmu
    :rtype AlgorithmDescription
    """
    return algorithms[name]


def get_all_algorithms_choices():
    """
    Zwraca opis wszyskich zajestrowanych algorytmów.
    Do użycia w modelach django jako choices
    """
    choices = []
    for k, v in algorithms.items():
        choices.append((v.name, v.verbose_name))
    return set(choices)


def get_crypto_object(algorithm_name, key):
    """
    Zwraca obiekt obsługującą zadany algortym

    :param algorithm_name: nazwa algortymu
    :parma key: klucz szyfrujący

    :rtype EncryptorMixIn
    """
    encryptor = EncryptorMixIn(key)
    algorithm = get_algorithm(algorithm_name)
    setattr(encryptor, 'doEncrypt', algorithm.encryption_function)
    setattr(encryptor, 'doDecrypt', algorithm.decryption_function)
    return encryptor


register_algorithm('xor', "Xor", cryptopp.passwordXor,
                   cryptopp.passwordXor)
register_algorithm('rc4', "RC4", cryptopp.passwordRC4,
                   cryptopp.passwordRC4)
register_algorithm('plain', "Plain", cryptopp.passwordPlain,
                   cryptopp.passwordPlain)
