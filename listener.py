import threading
import speech_recognition as sr
import cv2
import serial
import time
from ultralytics import YOLO
import math
import matplotlib.pyplot as plt

def listen_to_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    while True:
        print("Listening for commands...")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized command: {command}")
            process_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError:
            print("Could not request results; check your network connection")