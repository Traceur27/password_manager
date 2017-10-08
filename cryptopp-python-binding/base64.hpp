#ifndef CRYPTOPP_PYTHON_BINDING_BASE64_HPP
#define CRYPTOPP_PYTHON_BINDING_BASE64_HPP

#include <string>

/*
 * C++ base64 encode and decode based on
 * http://www.adp-gmbh.ch/cpp/common/base64.html
 */
/*Encodes bytes table of lenght in_len into base64 string*/
std::string base64_encode(unsigned char *bytes_to_encode, unsigned long in_len);

#endif //CRYPTOPP_PYTHON_BINDING_BASE64_HPP
