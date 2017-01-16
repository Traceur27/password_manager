#ifndef CRYPTOPP_PYTHON_BINDING_BASE64_HPP
#define CRYPTOPP_PYTHON_BINDING_BASE64_HPP

#include <algorithm>
#include <boost/python/def.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/module.hpp>
#include <boost/python/object.hpp>
#include <boost/python/str.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <iostream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace boost::python;

/*
 * C++ base64 encode and decode based on
 * http://www.adp-gmbh.ch/cpp/common/base64.html
 */
/*Encodes bytes table of lenght in_len into base64 string*/
std::string base64_encode(unsigned char *bytes_to_encode, unsigned long in_len);

#endif //CRYPTOPP_PYTHON_BINDING_BASE64_HPP
