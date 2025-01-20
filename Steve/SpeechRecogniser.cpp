#include <iostream>
#include <fstream>
#include <vector>
#include <portaudio.h>

#define SAMPLE_RATE 44100
#define FRAMES_PER_BUFFER 256
#define NUM_SECONDS 5

// Buffer to hold audio data
std::vector<float> audioBuffer;

// Audio callback function
static int audioCallback(const void* inputBuffer, void* /*outputBuffer*/,
    unsigned long framesPerBuffer,
    const PaStreamCallbackTimeInfo* /*timeInfo*/,
    PaStreamCallbackFlags /*statusFlags*/,
    void* /*userData*/) {
    const float* data = static_cast<const float*>(inputBuffer);
    audioBuffer.insert(audioBuffer.end(), data, data + framesPerBuffer);
    return paContinue;
}

// Function to save audio data to a file
void saveAudioData(const char* filename, const std::vector<float>& data) {
    std::ofstream file(filename, std::ios::binary);
    if (!file) {
        std::cerr << "Failed to open file for writing." << std::endl;
        return;
    }
    file.write(reinterpret_cast<const char*>(data.data()), data.size() * sizeof(float));
    file.close();
}

int main() {
    PaStream* stream;
    PaError err;

    err = Pa_Initialize();
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    err = Pa_OpenDefaultStream(&stream,
        1, // Number of input channels
        0, // Number of output channels
        paFloat32, // Sample format
        SAMPLE_RATE,
        FRAMES_PER_BUFFER,
        audioCallback,
        nullptr);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    err = Pa_StartStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
        return 1;
    }

    std::cout << "Recording for " << NUM_SECONDS << " seconds..." << std::endl;
    Pa_Sleep(NUM_SECONDS * 1000);

    err = Pa_StopStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
    }

    err = Pa_CloseStream(stream);
    if (err != paNoError) {
        std::cerr << "PortAudio error: " << Pa_GetErrorText(err) << std::endl;
    }

    Pa_Terminate();

    // Save recorded audio data to a file
    saveAudioData("audio.raw", audioBuffer);

    std::cout << "Audio data saved to 'audio.raw'" << std::endl;

    return 0;
}
