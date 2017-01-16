#include <algorithm>
#include <boost/python/def.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/module.hpp>
#include <boost/python/str.hpp>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;
using namespace boost::python;

static const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/";

static const int maskOutFour = 0xfc;
static const int maskInThree = 0x03;
static const int maskOutLowerNibble = 0xf0;
static const int maskOutHigherNibble = 0x0f;
static const int maskInTwoUpperBits = 0xc0;
static const int maskOutTwoUpperBits = 0x3f;

/*
 * C++ base64 encode and decode based on
 * http://www.adp-gmbh.ch/cpp/common/base64.html
 */
std::string base64_encode(unsigned char *bytes_to_encode, unsigned long in_len) {
    std::string ret;
    int i = 0;
    int j = 0;
    unsigned char char_array_3[3] = {0};
    unsigned char char_array_4[4] = {0};

    while (in_len--) {
        char_array_3[i++] = *(bytes_to_encode++);
        if (i == 3) {
            char_array_4[0] = (char_array_3[0] & maskOutFour) >> 2;
            char_array_4[1] = ((char_array_3[0] & maskInThree) << 4) + ((char_array_3[1] & maskOutLowerNibble) >> 4);
            char_array_4[2] = ((char_array_3[1] & maskOutHigherNibble) << 2) + ((char_array_3[2] & maskInTwoUpperBits) >> 6);
            char_array_4[3] = char_array_3[2] & maskOutTwoUpperBits;

            for (i = 0; i < 4; i++)
                ret += base64_chars[char_array_4[i]];
            i = 0;
        }
    }

    if (i) {
        for (j = i; j < 3; j++)
            char_array_3[j] = '\0';

        char_array_4[0] = (char_array_3[0] & maskOutFour) >> 2;
        char_array_4[1] = ((char_array_3[0] & maskInThree) << 4) + ((char_array_3[1] & maskOutLowerNibble) >> 4);
        char_array_4[2] = ((char_array_3[1] & maskOutHigherNibble) << 2) + ((char_array_3[2] & maskInTwoUpperBits) >> 6);
        char_array_4[3] = char_array_3[2] & maskOutTwoUpperBits;

        for (j = 0; (j < i + 1); j++)
            ret += base64_chars[char_array_4[j]];

        while ((i++ < 3))
            ret += '=';
    }

    return ret;
}
