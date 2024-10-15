import time
import speech_recognition as sr
import pyautogui
import pygetwindow as gw
import sys

ACTIVATION_WORDS = [
    "except", "except except", "accept", "except queue", 
    "except the queue", "accept the queue", "set except", 
    "except you", "except the key", "except key"
]
WINDOW_TITLE = "League of Legends"  # Click window
PAUSE_WINDOW_TITLE = "League of Legends (TM) Client"  # Change this to the window you want to check
accept_button_location = None
def listen_for_activation_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say 'accept' 'accept queue' or 'accept the queue'...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return None

def find_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        return window[0]
    else:
        print(f"Window with title '{window_title}' not found.")
        return None

def click_in_window(button_location):  # Clicks the detected button location
    if button_location is not None:
        accept_button_center = pyautogui.center(button_location)
        pyautogui.click(accept_button_center)
        time.sleep(5)

def is_pause_window_open():
    return bool(gw.getWindowsWithTitle(PAUSE_WINDOW_TITLE))

def is_click_window_open():
    return bool(gw.getWindowsWithTitle(WINDOW_TITLE))

def check_queue_pop():
    while True:
        try:
            accept_button_location = pyautogui.locateOnScreen('accept.png', confidence=0.7)
            if accept_button_location is not None:
                print("Match found! Say 'accept queue' or 'accept' to accept queue.")
                return pyautogui.locateOnScreen('accept.png', confidence=0.7)
            else:
                print("Accept button not found. Checking again...")
        except Exception as e:
            print(f"Waiting for queue pop...")

        time.sleep(1)  # Wait before checking again

def wait_for_pause_window_to_close():
    print(f"Waiting for '{PAUSE_WINDOW_TITLE}' to close...")
    while is_pause_window_open():
        time.sleep(1)
    print(f"'{PAUSE_WINDOW_TITLE}' is closed. Resuming...")

def wait_for_click_window_to_open():
    print(f"Waiting for '{WINDOW_TITLE}' to open...")
    while not is_click_window_open():
        time.sleep(1)
    print(f"'{WINDOW_TITLE}' is now open. Resuming...")

def main():
    while True:
        if is_pause_window_open():
            wait_for_pause_window_to_close()
            continue  # Return to the top of the loop

        if not is_click_window_open():
            wait_for_click_window_to_open()
            continue  # Return to the top of the loop

        # Check if the accept button is visible
        button_location = check_queue_pop()

        if button_location is not None:  # Proceed if a button location is found
            # Wait for the activation words after detecting the match
            word = listen_for_activation_word()

            # Check if the spoken word matches the activation words
            if word in ACTIVATION_WORDS:
                print(f"Activation word detected. Accepting queue...")
                click_in_window(button_location)
            else:
                print("Activation word not detected.")
                continue  # Continue checking for the button location in the next iteration
        else:
            print("No accept button found, continuing to check...")
            
if __name__ == "__main__":
    main()
