#include <algorithm>
#include <boost/python/def.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/module.hpp>
#include <boost/python/str.hpp>
#include <fstream>
#include <iostream>
#include <vector>

#include "base64.hpp"

using namespace std;
using namespace boost::python;

/*Funkcja szyfruje dane wykorzystując algorytm xor by key*/
str passwordXor(object dataToEncrypt, str masterPassword) {
    int masterPasswordLenght = len(masterPassword);
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::string rawMasterPassword = extract<std::string>(masterPassword);
    std::vector<unsigned  char> result;
    for (int i = 0, masterPasswordCharIndex = 0; i < dataLen; i++) {
        result.push_back(rawData[i] ^ rawMasterPassword[masterPasswordCharIndex]);
        masterPasswordCharIndex++;
        if (masterPasswordCharIndex == masterPasswordLenght)
            masterPasswordCharIndex = 0;
    }
    return str(base64_encode(result.data(), result.size()));
}
