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

/*Funkcja przepisująca dane do zaszyfrowania wartości zwracanej bez zaszyfrowania*/
str passwordPlain(object dataToEncrypt, str masterPassword) {
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::vector<unsigned char> result;
    for (int i = 0; i < dataLen; i++) {
        unsigned char byte = rawData[i];
        result.push_back(byte);
    }
    return str(base64_encode(result.data(), result.size()));
}
