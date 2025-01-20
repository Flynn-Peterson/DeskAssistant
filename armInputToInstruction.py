
#Todo
"""

Figure out hardware

Update how you want stuff to work

"""
import threading
import os
import speech_recognition as sr
import cv2
import serial
import time
from ultralytics import YOLO
import math
import matplotlib.pyplot as plt
import calendar


class Event:
    def __init__(self, date: str, description: str):
        self.date = date
        self.description = description
class Task:

    def __init__(self, description: str, done: bool):
        self.description = description
        self.done = done

    def __str__(self):
        status = "Done" if self.done else "Not Done"
        return f"Task(description='{self.description}', status='{status}')"

    def __repr__(self):
        return self.__str__()

def save_task_to_file(tasks, filename):
    with open(filename, 'w') as f:
        f.write(f"{len(tasks)}\n")  # Write the number of tasks first
        for task in tasks:
            description = task.description.replace(' ', '_')  # Use underscores for spaces
            f.write(f"{description} {int(task.done)}\n")  # Save as 0 or 1 for done status

def save_events_to_file(events,filename):
    with open(filename, 'w') as f:
        for event in events:
            f.write(f"{event.date},{event.description}")



def read_events_from_file():
    events = []
    with open('events.txt', 'r') as file:
        for line in file:
            events.append(line.strip())
    return events

def load_task_from_file(filename):
    if not os.path.exists(filename):
        return []

    tasks = []
    with open(filename, 'r') as f:
        # Read the first line to get the number of tasks
        n = int(f.readline().strip())
        # Read each subsequent line for task details
        for _ in range(n):
            line = f.readline().strip().split()
            if len(line) < 2:  # Check if the line has at least two elements
                continue  # Skip lines that don’t have the expected format
            description = ' '.join(line[:-1]).replace('_', ' ')
            done = line[-1].lower() == 'true'  # Handle case-insensitive 'True'
            tasks.append(Task(description, done))

    return tasks

# Initialize serial communication with Arduino
port='COM3'
baudrate=9600
todoListFile = 'C:\\PersonalProjects\\ToDoListAttempt3\\x64\\Debug\\tasks.txt'

try:
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for the serial connection to initialize

except serial.SerialException as e:
    print("Error opening serial port: ", e)


# Read from the Arduino serial port
def read_from_serial(ser):
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').strip()
            return int(line)
        except ValueError:
            return None
    return None


def initialize_recognizer():
    return sr.Recognizer()


def initialize_microphone():
    return sr.Microphone()


def adjust_for_ambient_noise(recognizer, source):
    recognizer.adjust_for_ambient_noise(source)


def capture_audio(recognizer, source):
    return recognizer.listen(source)


def recognize_speech(recognizer, audio):
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))
        return None

def handle_superkey(recognizer, source):
    print("yes sir I am listening: ")
    print("What mode would you like")


    running = True
    while running:
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            break
        text = recognize_speech(recognizer, audio)
        print("Steve heard: ", text)
        if text:
            if text == "assistant":
                assistantMode(recognizer, source)
            if text == "stop":
                print("DONEZO")
                return False

            if negativePhrase(text):
                print("I am a bad robot")
            return textToInstruction(text,recognizer, source)


def addToCalendar(recognizer,source):
    print("What would you like to add")
    running = True
    while running:
        try:
            audio = recognizer.listen(source,timeout = 5)
        except sr.WaitTimeoutError:
            print("I didnt hear anything")
            assistantMode(recognizer,source)

        whatAdd = recognize_speech(recognizer,audio)
        getDay(whatAdd,recognizer,source)

def dayToDate(month,day):

def getDay(text,recognizer,source):
    months = [
        "january", "february", "march", "april",
        "may", "june", "july", "august",
        "september", "october", "november", "december"
    ]
    days_in_month = [
        "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th",
        "11th", "12th", "13th", "14th", "15th", "16th", "17th", "18th", "19th", "20th",
        "21st", "22nd", "23rd", "24th", "25th", "26th", "27th", "28th", "29th", "30th", "31st"
    ]
    days = ["monday", "tuesday", "wednesday","thursday","friday","saturday","sunday"]
    whens = ["next", "this"]
    running = True
    print("What day would you like to add this text to?")
    while running:
        try:
            audio = recognizer.listen(source,timeout = 5)
        except sr.WaitTimeoutError:
            print("I didnt hear anything")
            assistantMode(recognizer,source)
        fullWhen = recognize_speech(recognizer,audio)
        for word in fullWhen.lower().split():
            if word in months:
                month = word
            if word in days_in_month:
                day_of_month = word
            if word in days:
                day = word
            if word in whens:
                when = word
        if day and when:
            if when == "next":
                

def negativePhrase(text):
    bad = ["dumb", "stupid", "idiot", "silly", "rat"]
    isBad = False
    for word in text.lower().split():
        if word in bad:
            isBad = True

    return isBad

def assistantMode(recognizer,source):
    print("What would you like")
    running = True
    while running:
        try:
            audio = recognizer.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("I didnt hear anything")
            assistantMode(recognizer,source)

        text = recognize_speech(recognizer, audio)
        print("I heard: ", text)
        if negativePhrase(text):
            print("BAD")


        actions = ["add", "remove","what's"]
        wheres = ["list"]
        stops = ["quit", "end", "stop"]

        action = None
        where = None

        for word in text.lower().split():
            if word in actions :
                action = word
            elif word in wheres:
                where = word
            elif word in stops:
                running = False

        if action and where:
            if action == "add" and where == "list":
                addToTodoList(recognizer,source)
            if action == "what's" and where == "list":
                showTodoList(recognizer,source)

def addToTodoList(recognizer,source):

    running = True
    while running:
        print("What would you like me to add")

        text = "Get gid scrub"
        print(text)
        if text:
            tasks = load_task_from_file(todoListFile)
            print(Task(text,False))
            task = Task(text,False)
            tasks.append(task)  # Add the new task
            save_task_to_file(tasks, todoListFile)
            # Save the updated list
            assistantMode(recognizer,source)
            running = False
        else:
            running = True

def showTodoList(recognizer,source):
    tasks = load_task_from_file(todoListFile)
    for task in tasks:
        print(task)
    assistantMode(recognizer,source)

def textToInstruction(text,recognizer, source):
    print("Recognizing:", text)

    actions = ["grab", "pick", "put", "sleep", "give", "hand", "have", "find","control"]
    items = ["pen", "notes", "key", "watch", "pencil"]
    locations = ["away", "me", "I"]
    colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "orange", "lime green"]

    action = None
    item = None
    location = None
    color = None

    for word in text.lower().split():
        if word in actions:
            action = word
        elif word in items:
            item = word
        elif word in locations:
            location = word
        elif word in colors:
            color = word

    if action == "sleep":
        print("Going to sleep")
    elif action == "control" and location == "me":
        startManualControl()
    elif action and item:
        detectItem(item)
    elif action and item and color:
        if action == "find":
            detectItem(item)
    elif action and item and location:
        print("Action:", action)
        print("Item:", item)
        print("Location: ", location)
        detectItem(item)
        return True
    else:
        print("Could not recognize action or item.")
        handle_superkey(recognizer,source)

    return False

def main():

    print(load_task_from_file(todoListFile))

    recognizer = initialize_recognizer()

    with initialize_microphone() as source:
        superKey = "hey Steve"
        stopPhrase = "stop"
        addToTodoList(recognizer,source)
        running = True
        while running:
            print("Listening...")
            adjust_for_ambient_noise(recognizer, source)
            audio = capture_audio(recognizer, source)
            text = recognize_speech(recognizer, audio)
            if text:
                print("You said:", text)
                if text == superKey:
                    handle_superkey(recognizer, source)
                elif text == stopPhrase:
                    running = False


def capture_frame(camera):
    ret, frame = camera.read()
    if not ret:
        print("Failed to capture image")
        return None
    return frame


def preprocess_frame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return hsv
def sendSingnal(x,y,instruction):
    print(x,y,instruction)
    message = f"{instruction} + {x},{y}".encode('utf-8')
    ser.write(message)


def detectItem(item):
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    model = YOLO("best8.pt")
    classNames = model.names

    print(classNames)

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    checks = 0

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        if img is None or img.size == 0:
            print("Captured image is invalid")
            break

        # Perform inference
        results = model(img)


        for r in results:
            boxes = r.boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                centerX = (x1 + x2)/2
                centerY = (y1 + y2)/2
                # Draw bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])
                if classNames[cls].lower() == item.lower():
                    print(centerX,centerY)
                    sendSingnal(centerX,centerY)

                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2

                cv2.putText(img, f'{classNames[cls]} {confidence}', org, font, fontScale, color, thickness)

        # Display the image using Matplotlib
        ax.clear()
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax.axis('off')
        plt.pause(0.001) # Pause to allow the image to update
        if checks > 100:
            sendSingnal(0,0)
            break
        checks+=1
        # Check for 'q' key press to exit
        if plt.waitforbuttonpress(0.001) and plt.get_current_fig_manager().canvas.get_tk_widget().focus_get() == None:
            break

    cap.release()
    plt.ioff()  # Turn off interactive mode
    plt.close(fig)

def move_robot(x, y):
    print(f"Moving robot to: ({x}, {y})")

def startManualControl():
    print('Starting manual control')
    controlling = True
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set width
    cap.set(4, 480)  # Set height

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture initial image")
        return

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_plot = ax.imshow(img)

    def on_mouse_move(event):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            move_robot(x, y)

    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

    def update_frame():
        while controlling:
            success, frame = cap.read()
            if not success or frame is None or frame.size == 0:
                print("Failed to capture image")
                break
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for Matplotlib
            img_plot.set_array(img)
            fig.canvas.draw_idle()
            time.sleep(0.01)  # Adjust sleep time as needed

    # Start the thread to update frames
    thread = threading.Thread(target=update_frame)
    thread.start()

    # Keep the plot window open
    try:
        plt.show(block=True)  # This blocks until the window is closed
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        controlling = False  # Stop the thread
        thread.join()  # Ensure the thread has finished
        cap.release()
        plt.ioff()
        print('Manual control ended')


if __name__ == "__main__":
    main()



