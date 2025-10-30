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
            sys.stdout.flush()
        return ''.join(chars)


def vigenere_cipher(text, key, mode="encrypt"):
    result = []
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            key_shift = ord(key_char) - ord('a')
            if mode == "decrypt":
                key_shift = -key_shift
            shifted = (ord(char) - base + key_shift) % 26 + base
            result.append(chr(shifted))
            key_index += 1
        else:
            result.append(char)  # spaces/punctuation stay as-is

    return ''.join(result)


# === MAIN PROGRAM ===
file_path = input("Enter the path to the text file: ")
key = hidden_input("Enter the encryption key: ").strip()
mode = input("Enter mode ('encrypt' or 'decrypt'): ").strip().lower()

# Read file
try:
    with open(file_path, "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found.")
    sys.exit(1)

# Encrypt or decrypt
result_text = vigenere_cipher(content, key, mode)

print("\nResulting text:\n")
print(result_text)