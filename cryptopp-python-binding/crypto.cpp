#include <algorithm>
#include <boost/python/def.hpp>
#include <boost/python/extract.hpp>
#include <boost/python/module.hpp>
#include <boost/python/str.hpp>

using namespace std;
using namespace boost::python;

str passwordPlain(object dataToEncrypt, str masterPassword);
str passwordXor(object dataToEncrypt, str masterPassword);
str passwordRC4(object dataToEncrypt, str masterPassword);

BOOST_PYTHON_MODULE (cryptopp) {
    def("passwordPlain", passwordPlain);
    def("passwordXor", passwordXor);
    def("passwordRC4", passwordRC4);
}
