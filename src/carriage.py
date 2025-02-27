import sys
import time
import threading
import msvcrt  # Windows-only for non-blocking input

def show_message(message):
    """ Clears user input, prints server message, and restores input """
    sys.stdout.write("\r" + " " * 100 + "\r")  # Clear current input
    sys.stdout.write(f"\n[Server] {message}\n")  # Print server message
    sys.stdout.write("<You> ")  # Restore user prompt
    sys.stdout.flush()

def fake_server_messages():
    """ Simulates incoming server messages at random intervals """
    count = 2
    while count:
        show_message(f"YOU GOT {count} MESSAGES!!")
        time.sleep(1)
        count += 1


# Start fake server messages in a background thread
threading.Thread(target=fake_server_messages, daemon=True).start()

# print("Start typing. Messages will appear without overwriting your input.\n")

buffer = ""  # Store typed characters

while True:
    if msvcrt.kbhit():  # Check if a key was pressed
        char = msvcrt.getch().decode("utf-8")  # Read character
        if char == "\r":  # Enter key
            sys.stdout.write("\n")  # Move to new line
            sys.stdout.flush()
            buffer = ""  # Reset input buffer
        elif char == "\b":  # Backspace
            buffer = buffer[:-1]  # Remove last character
            sys.stdout.write("\r" + " " * 100 + "\r")  # Clear line
            sys.stdout.write("<You> " + buffer)  # Reprint buffer
            sys.stdout.flush()
        else:
            buffer += char  # Add character to buffer
            sys.stdout.write(char)  # Show character
            sys.stdout.flush()
