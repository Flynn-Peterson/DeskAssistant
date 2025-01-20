#ifndef SPEECHRECOGNIZER_H
#define SPEECHRECOGNIZER_H

#include <string>
#include <pocketsphinx.h>
#include <sphinxbase/ad.h>
#include <sphinxbase/err.h>

class SpeechRecognizer {
public:
    SpeechRecognizer();
    ~SpeechRecognizer();

    bool initialize(const std::string& hmm, const std::string& lm, const std::string& dict);
    std::string listen();

private:
    ps_decoder_t* ps;      // PocketSphinx decoder
    cmd_ln_t* config;      // Configuration parameters
    ad_rec_t* ad;          // Audio device
    int16 adbuf[4096];     // Audio buffer
};

#endif // SPEECHRECOGNIZER_H
IZER_H