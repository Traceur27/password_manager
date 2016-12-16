#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/object.hpp>
#include <boost/python/str.hpp>
#include <boost/python/extract.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstdio>
#include <cstring>


using namespace std;
using namespace boost::python;


static const std::string base64_chars =
             "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             "abcdefghijklmnopqrstuvwxyz"
             "0123456789+/";


static inline bool is_base64(unsigned char c) {
  return (isalnum(c) || (c == '+') || (c == '/'));
}
/*
 * C++ base64 encode and decode based on
 * http://www.adp-gmbh.ch/cpp/common/base64.html
 */
std::string base64_encode(char* bytes_to_encode, unsigned int in_len) {
  std::string ret;
  int i = 0;
  int j = 0;
  unsigned char char_array_3[3];
  unsigned char char_array_4[4];

  while (in_len--) {
    char_array_3[i++] = *(bytes_to_encode++);
    if (i == 3) {
      char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
      char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
      char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
      char_array_4[3] = char_array_3[2] & 0x3f;

      for(i = 0; (i <4) ; i++)
        ret += base64_chars[char_array_4[i]];
      i = 0;
    }
  }

  if (i)
  {
    for(j = i; j < 3; j++)
      char_array_3[j] = '\0';

    char_array_4[0] = (char_array_3[0] & 0xfc) >> 2;
    char_array_4[1] = ((char_array_3[0] & 0x03) << 4) + ((char_array_3[1] & 0xf0) >> 4);
    char_array_4[2] = ((char_array_3[1] & 0x0f) << 2) + ((char_array_3[2] & 0xc0) >> 6);
    char_array_4[3] = char_array_3[2] & 0x3f;

    for (j = 0; (j < i + 1); j++)
      ret += base64_chars[char_array_4[j]];

    while((i++ < 3))
      ret += '=';

  }

  return ret;

}

std::string base64_decode(std::string const& encoded_string) {
  int in_len = encoded_string.size();
  int i = 0;
  int j = 0;
  int in_ = 0;
  unsigned char char_array_4[4], char_array_3[3];
  std::string ret;

  while (in_len-- && ( encoded_string[in_] != '=') && is_base64(encoded_string[in_])) {
    char_array_4[i++] = encoded_string[in_]; in_++;
    if (i ==4) {
      for (i = 0; i <4; i++)
        char_array_4[i] = base64_chars.find(char_array_4[i]);

      char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
      char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
      char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

      for (i = 0; (i < 3); i++)
        ret += char_array_3[i];
      i = 0;
    }
  }

  if (i) {
    for (j = i; j <4; j++)
      char_array_4[j] = 0;

    for (j = 0; j <4; j++)
      char_array_4[j] = base64_chars.find(char_array_4[j]);

    char_array_3[0] = (char_array_4[0] << 2) + ((char_array_4[1] & 0x30) >> 4);
    char_array_3[1] = ((char_array_4[1] & 0xf) << 4) + ((char_array_4[2] & 0x3c) >> 2);
    char_array_3[2] = ((char_array_4[2] & 0x3) << 6) + char_array_4[3];

    for (j = 0; (j < i - 1); j++) ret += char_array_3[j];
  }

  return ret;
}

str passwordXor(object dataToEncrypt, str masterPassword) {
    int masterPasswordLenght = len(masterPassword);
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::string rawMasterPassword = extract<std::string>(masterPassword);
    std::vector<char> result;
    for (int i = 0, masterPasswordCharIndex = 0; i < dataLen; i++) {
        result.push_back(rawData[i] ^ rawMasterPassword[masterPasswordCharIndex]);
        masterPasswordCharIndex++;
        if (masterPasswordCharIndex == masterPasswordLenght)
            masterPasswordCharIndex = 0;
    }
    return str(base64_encode(result.data(), result.size()));
}

/*
 * RC4 encryption implementation based on
 * https://gist.github.com/Mjiig/2727751
 */

class State
{
	unsigned char s[256];
	int i, j;

	void swap(int a, int b);

	public:
	unsigned char getbyte(void);
	State(unsigned char key[], int length );
};

State::State(unsigned char key[], int length)
{
	for(int k=0; k<256; k++)
	{
		s[k]=k;
	}

	j=0;
	for(i=0; i<256 ; i++)
	{
		j=(j + s[i] + key[i % length]) % 256;
		swap(i, j);
	}

	i=j=0;
}

void State::swap(int a, int b)
{
	unsigned char temp= s[i];
	s[i]=s[j];
	s[j]=temp;
}

unsigned char State::getbyte(void)
{
	i=(i+1)%256;
	j=(j+s[i])%256;
	swap(i, j);
	int index=(s[i]+s[j])%256;
	return s[index];
}


int gettextkey(unsigned char data[], std::string key)
{
	size_t i;
	for(i=0; i<key.length(); i++)
		data[i]=key[i];
	return i;
}

str passwordRC4(object dataToEncrypt, str masterPassword) {
    int masterPasswordLenght = len(masterPassword);
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::string rawMasterPassword = extract<std::string>(masterPassword);
    std::vector<char> result;
	unsigned char keydata[masterPasswordLenght];
    int len = gettextkey(keydata, rawMasterPassword);
	State bytestream (keydata, len);
    for (int i = 0; i < dataLen; i++) {
        char byte = bytestream.getbyte() ^ rawData[i];
        result.push_back(byte);
    }
    return str(base64_encode(result.data(), result.size()));
}

str passwordPlain(object dataToEncrypt, str masterPassword) {
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::vector<char> result;
    for (int i = 0; i < dataLen; i++) {
        char byte = rawData[i];
        result.push_back(byte);
    }
    return str(base64_encode(result.data(), result.size()));
}


BOOST_PYTHON_MODULE(cryptopp)
{
    def("passwordPlain", passwordPlain);
    def("passwordXor", passwordXor);
    def("passwordRC4", passwordRC4);
}
