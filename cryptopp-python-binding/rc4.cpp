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

/* Stała definiująca wielkość tablicy permutacji */
static const int MAX_ARRAY_SIZE = 256;

/*
 * Implementacja algorytmu szyfrowania RC4 bazująca na:
 * https://gist.github.com/Mjiig/2727751
 * https://en.wikipedia.org/wiki/RC4
 */

/* Klasa opisująca stan strumienia szyfrującego RC4 */
class State {
    /*Tablica permutacji*/
    unsigned char state_table[MAX_ARRAY_SIZE];
    /*Pomocnicze indeksy*/
    int first_index, second_index;

    /*Metoda zamieniająca miejscami elementy tablicy permutacji wskazywane przez pomocnicze indeksy*/
    void swap();

public:
    /*Zwraca następny zaszyfrowany bajt ze strumienia*/
    unsigned char getbyte(void);

    /*c-tor*/
    State(unsigned char key[], int length_of_key);
};

State::State(unsigned char key[], int length_of_key) {
    for (int k = 0; k < MAX_ARRAY_SIZE; k++) {
        state_table[k] = k;
    }

    second_index = 0;
    for (first_index = 0; first_index < MAX_ARRAY_SIZE; first_index++) {
        second_index = (second_index + state_table[first_index] + key[first_index % length_of_key]) % MAX_ARRAY_SIZE;
        swap();
    }

    first_index = second_index = 0;
}

void State::swap() {
    unsigned char temp = state_table[first_index];
    state_table[first_index] = state_table[second_index];
    state_table[second_index] = temp;
}

unsigned char State::getbyte(void) {
    first_index = (first_index + 1) % MAX_ARRAY_SIZE;
    second_index = (second_index + state_table[first_index]) % MAX_ARRAY_SIZE;
    swap();
    int index = (state_table[first_index] + state_table[second_index]) % MAX_ARRAY_SIZE;
    return state_table[index];
}

int gettextkey(unsigned char data[], std::string key) {
    size_t i;
    for (i = 0; i < key.length(); i++)
        data[i] = key[i];
    return i;
}

/*Funkcja szyfrująca dane, wykorzystując algorytm RC4*/
str passwordRC4(object dataToEncrypt, str masterPassword) {
    int masterPasswordLenght = len(masterPassword);
    int dataLen = len(dataToEncrypt);
    std::string rawData = extract<std::string>(dataToEncrypt);
    std::string rawMasterPassword = extract<std::string>(masterPassword);
    std::vector<unsigned char> result;
    unsigned char keydata[masterPasswordLenght];
    int len = gettextkey(keydata, rawMasterPassword);
    State bytestream(keydata, len);
    for (int i = 0; i < dataLen; i++) {
        unsigned char byte = bytestream.getbyte() ^rawData[i];
        result.push_back(byte);
    }
    return str(base64_encode(result.data(), result.size()));
}