import sys
import os

def hidden_input(prompt=""):
    """Cross-platform hidden input showing a single dot when typing."""
    print(prompt, end="", flush=True)

    if os.name == 'nt':  # Windows
        import msvcrt
        chars = []
        dot_shown = False
        while True:
            ch = msvcrt.getch()
            if ch in {b'\r', b'\n'}:
                sys.stdout.write('\r\n')
                sys.stdout.flush()
                break
            elif ch == b'\x08':  # Backspace
                if chars:
                    chars.pop()
            else:
                try:
                    char = ch.decode()
                except UnicodeDecodeError:
                    continue
                chars.append(char)
                if not dot_shown:
                    sys.stdout.write('•')
                    sys.stdout.flush()
                    dot_shown = True
        return ''.join(chars)

    else:  # macOS/Linux
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        chars = []
        dot_shown = False
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ('\n', '\r'):
                    sys.stdout.write('\r\n')
                    sys.stdout.flush()
                    break
                elif ch == '\x7f':  # Backspace
                    if chars:
                        chars.pop()
                else:
                    chars.append(ch)
                    if not dot_shown:
                        sys.stdout.write('•')
                        sys.stdout.flush()
                        dot_shown = True
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            sys.stdout.flush()   # ensure prompt resets correctly
        return ''.join(chars)


def shift_text(text, shift, direction):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            if direction == "left":
                shifted = (ord(char) - base - shift) % 26 + base
            elif direction == "right":
                shifted = (ord(char) - base + shift) % 26 + base
            else:
                print("Error: Invalid direction")
                sys.exit(1)
            result += chr(shifted)
        else:
            result += char
    return result


# Normal inputs
file_path = input("Enter the path to the text file: ")
shift_amount = int(hidden_input("Enter how many characters to shift by: "))
direction = hidden_input("Enter shift direction ('left' or 'right'): ").strip().lower()

# Read and shift
try:
    with open(file_path, "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found.")
    sys.exit(1)

shifted_text = shift_text(content, shift_amount, direction)

print("\nShifted text:\n")
print(shifted_text)
