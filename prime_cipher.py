#!/usr/bin/env python3
import os
import sys

# Terminal Color Formatting (ANSI)
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def is_prime(n: int) -> bool:
    """Checks if a given integer is a prime number."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def generate_primes(count: int) -> list:
    """Generates the first N prime numbers dynamically."""
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes


# Map printable ASCII characters (codes 32 to 126) + newline/tab to prime numbers
ASCII_CHARS = [chr(i) for i in range(32, 127)] + ["\n", "\t"]
PRIMES = generate_primes(len(ASCII_CHARS))

CHAR_TO_PRIME = {char: str(prime) for char, prime in zip(ASCII_CHARS, PRIMES)}
PRIME_TO_CHAR = {str(prime): char for char, prime in zip(ASCII_CHARS, PRIMES)}


def cipher_text(plain_text: str, key_offset: int = 0) -> str:
    """Encrypts plain text into space-separated prime numbers."""
    tokens = []
    num_primes = len(PRIMES)

    for char in plain_text:
        if char in CHAR_TO_PRIME:
            base_idx = ASCII_CHARS.index(char)
            shifted_idx = (base_idx + key_offset) % num_primes
            tokens.append(str(PRIMES[shifted_idx]))
        else:
            tokens.append(f"[{char}]")

    return " ".join(tokens)


def decipher_text(ciphered_text: str, key_offset: int = 0) -> str:
    """Decrypts space-separated prime numbers back into plain text."""
    tokens = ciphered_text.strip().split(" ")
    decoded_chars = []
    num_primes = len(PRIMES)

    for token in tokens:
        if token in PRIME_TO_CHAR:
            base_idx = PRIMES.index(int(token))
            shifted_idx = (base_idx - key_offset) % num_primes
            decoded_chars.append(ASCII_CHARS[shifted_idx])
        elif token.startswith("[") and token.endswith("]"):
            decoded_chars.append(token[1:-1])
        elif token == "":
            continue
        else:
            decoded_chars.append("?")

    return "".join(decoded_chars)


def process_file_encryption(
    input_path: str, output_path: str, key_offset: int = 0
) -> bool:
    """Reads a text file, encrypts its contents, and saves it to an output file."""
    if not os.path.isfile(input_path):
        print(f"{RED}[!] Error: Input file '{input_path}' does not exist.{RESET}")
        return False

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        encrypted_data = cipher_text(content, key_offset=key_offset)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(encrypted_data)

        print(
            f"{GREEN}[✓] File successfully encrypted! Saved to: {BOLD}{output_path}{RESET}"
        )
        return True
    except Exception as e:
        print(f"{RED}[!] File processing error: {e}{RESET}")
        return False


def process_file_decryption(
    input_path: str, output_path: str, key_offset: int = 0
) -> bool:
    """Reads an encrypted prime file, decrypts it, and saves it to an output file."""
    if not os.path.isfile(input_path):
        print(f"{RED}[!] Error: Input file '{input_path}' does not exist.{RESET}")
        return False

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()

        decrypted_data = decipher_text(content, key_offset=key_offset)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(decrypted_data)

        print(
            f"{GREEN}[✓] File successfully decrypted! Saved to: {BOLD}{output_path}{RESET}"
        )
        return True
    except Exception as e:
        print(f"{RED}[!] File processing error: {e}{RESET}")
        return False


def print_menu():
    """Displays the interactive menu and available options."""
    print(f"{GREEN}{BOLD}==================================================")
    print("      PRIME CIPHER CLI — FILE I/O EDITION        ")
    print(f"=================================================={RESET}")
    print("Commands:")
    print(
        f"  {CYAN}cipher <text>{RESET}                - Encrypt text inline"
    )
    print(
        f"  {CYAN}decipher <primes>{RESET}            - Decrypt primes inline"
    )
    print(
        f"  {CYAN}cipher-file <in> <out> [key]{RESET}  - Encrypt input file to output file"
    )
    print(
        f"  {CYAN}decipher-file <in> <out> [key]{RESET}- Decrypt input file to output file"
    )
    print(
        f"  {CYAN}menu{RESET} / {CYAN}help{RESET}                   - Show this menu"
    )
    print(
        f"  {CYAN}clear{RESET} / {CYAN}cls{RESET}                   - Clear screen and show menu"
    )
    print(
        f"  {CYAN}init{RESET}                          - Run demonstration"
    )
    print(
        f"  {CYAN}exit{RESET}                          - Quit CLI"
    )
    print(f"{GREEN}--------------------------------------------------{RESET}\n")


def clear_screen():
    """Clears terminal screen cross-platform and displays the menu."""
    os.system("cls" if os.name == "nt" else "clear")
    print_menu()


def run_init_demo():
    """Demonstrates text and file encryption capabilities."""
    print(f"\n{CYAN}=== INITIAL DEMONSTRATION ==={RESET}")
    sample_text = "Secret Message 2026!"
    key = 7

    encrypted = cipher_text(sample_text, key_offset=key)
    decrypted = decipher_text(encrypted, key_offset=key)

    print(f"{YELLOW}Original Text    :{RESET} {sample_text}")
    print(f"{GREEN}Ciphered (Key {key}):{RESET} {encrypted}")
    print(f"{CYAN}Deciphered       :{RESET} {decrypted}\n")


def main():
    clear_screen()

    while True:
        try:
            user_input = input(f"{GREEN}prime-cipher>{RESET} ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd in ["clear", "cls"]:
                clear_screen()

            elif cmd in ["menu", "help"]:
                print_menu()

            elif cmd == "init":
                run_init_demo()

            elif cmd == "cipher":
                if len(parts) < 2:
                    print(
                        f"{RED}[!] Error: Text required. Example: cipher Hello World{RESET}"
                    )
                    continue
                text_to_encrypt = " ".join(parts[1:])
                print(f"{YELLOW}Result:{RESET} {cipher_text(text_to_encrypt)}")

            elif cmd == "decipher":
                if len(parts) < 2:
                    print(
                        f"{RED}[!] Error: Primes required. Example: decipher 3 2 67{RESET}"
                    )
                    continue
                primes_to_decrypt = " ".join(parts[1:])
                print(
                    f"{YELLOW}Result:{RESET} {decipher_text(primes_to_decrypt)}"
                )

            elif cmd == "cipher-file":
                if len(parts) < 3:
                    print(
                        f"{RED}[!] Usage: cipher-file <input_file> <output_file> [key_offset]{RESET}"
                    )
                    continue
                in_path = parts[1]
                out_path = parts[2]
                key = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                process_file_encryption(in_path, out_path, key_offset=key)

            elif cmd == "decipher-file":
                if len(parts) < 3:
                    print(
                        f"{RED}[!] Usage: decipher-file <input_file> <output_file> [key_offset]{RESET}"
                    )
                    continue
                in_path = parts[1]
                out_path = parts[2]
                key = int(parts[3]) if len(parts) > 3 and parts[3].isdigit() else 0
                process_file_decryption(in_path, out_path, key_offset=key)

            elif cmd == "exit":
                print("Exiting CLI. Goodbye!")
                break

            else:
                print(
                    f"{RED}[!] Unknown command: '{cmd}'. Type 'menu' for help.{RESET}"
                )

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. Goodbye!")
            break


if __name__ == "__main__":
    main()