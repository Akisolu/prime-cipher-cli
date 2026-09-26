#!/usr/bin/env python3
import argparse
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
    """Encrypts plain text into space-separated prime numbers with modular offset."""
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
    """Decrypts space-separated prime numbers back into plain text with modular offset."""
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
    print("      PRIME CIPHER CLI — DUAL MODE EDITION        ")
    print(f"=================================================={RESET}")
    print("Interactive Commands:")
    print(
        f"  {CYAN}cipher [key] <text>{RESET}          - Encrypt text (Key is optional)"
    )
    print(
        f"  {CYAN}decipher [key] <primes>{RESET}      - Decrypt primes (Key is optional)"
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
    """Demonstrates text and key-offset cipher capabilities."""
    print(f"\n{CYAN}=== INITIAL DEMONSTRATION ==={RESET}")
    sample_text = "Secret Message 2026!"
    key = 7

    encrypted = cipher_text(sample_text, key_offset=key)
    decrypted = decipher_text(encrypted, key_offset=key)

    print(f"{YELLOW}Original Text    :{RESET} {sample_text}")
    print(f"{GREEN}Ciphered (Key {key}):{RESET} {encrypted}")
    print(f"{CYAN}Deciphered       :{RESET} {decrypted}\n")


def parse_key_and_content(parts: list):
    """Utility to extract key and text/primes from user command tokens."""
    key = 0
    start_index = 1

    if len(parts) > 1 and (
        parts[1].isdigit() or (parts[1].startswith("-") and parts[1][1:].isdigit())
    ):
        try:
            key = int(parts[1])
            start_index = 2
        except ValueError:
            pass

    content = " ".join(parts[start_index:])
    return key, content


def run_interactive_mode():
    """Runs the interactive REPL shell."""
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
                        f"{RED}[!] Usage: cipher [key] <text>\n"
                        f"    Examples:\n"
                        f"      cipher Hello World\n"
                        f"      cipher 7 Secret Message{RESET}"
                    )
                    continue

                key, text_to_encrypt = parse_key_and_content(parts)

                if not text_to_encrypt:
                    print(f"{RED}[!] Error: No text provided after key.{RESET}")
                    continue

                encrypted = cipher_text(text_to_encrypt, key_offset=key)
                print(f"{GREEN}[✓] Ciphered (Key {BOLD}{key}{RESET}{GREEN}):{RESET}")
                print(f"{YELLOW}{encrypted}{RESET}")

            elif cmd == "decipher":
                if len(parts) < 2:
                    print(
                        f"{RED}[!] Usage: decipher [key] <primes>\n"
                        f"    Examples:\n"
                        f"      decipher 3 2 67\n"
                        f"      decipher 7 67 19 83{RESET}"
                    )
                    continue

                key, primes_to_decrypt = parse_key_and_content(parts)

                if not primes_to_decrypt:
                    print(f"{RED}[!] Error: No prime tokens provided after key.{RESET}")
                    continue

                decrypted = decipher_text(primes_to_decrypt, key_offset=key)
                print(f"{GREEN}[✓] Deciphered (Key {BOLD}{key}{RESET}{GREEN}):{RESET}")
                print(f"{CYAN}{decrypted}{RESET}")

            elif cmd == "cipher-file":
                if len(parts) < 3:
                    print(
                        f"{RED}[!] Usage: cipher-file <input_file> <output_file> [key_offset]{RESET}"
                    )
                    continue
                in_path = parts[1]
                out_path = parts[2]
                key = (
                    int(parts[3])
                    if len(parts) > 3
                    and (
                        parts[3].isdigit()
                        or (parts[3].startswith("-") and parts[3][1:].isdigit())
                    )
                    else 0
                )
                process_file_encryption(in_path, out_path, key_offset=key)

            elif cmd == "decipher-file":
                if len(parts) < 3:
                    print(
                        f"{RED}[!] Usage: decipher-file <input_file> <output_file> [key_offset]{RESET}"
                    )
                    continue
                in_path = parts[1]
                out_path = parts[2]
                key = (
                    int(parts[3])
                    if len(parts) > 3
                    and (
                        parts[3].isdigit()
                        or (parts[3].startswith("-") and parts[3][1:].isdigit())
                    )
                    else 0
                )
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


def main():
# Extended help text with ANSI colors and usage constraints note
    help_epilog = f"""
{GREEN}{BOLD}Usage Examples (Direct / Batch Mode):{RESET}
  -----------------------------------
  1. Encrypt inline text using default key (0):
     {CYAN}python prime_cipher.py -t "Hello World"{RESET}

  2. Encrypt inline text with a custom numeric key (6):
     {CYAN}python prime_cipher.py -k 6 -t "Secret Message"{RESET}
     {CYAN}python prime_cipher.py --key=6 --text="Secret Message"{RESET}

  3. Decrypt a sequence of prime numbers with key (6):
     {CYAN}python prime_cipher.py -k 6 -d "103 107 109 113"{RESET}

  4. Encrypt a text file:
     {CYAN}python prime_cipher.py -k 6 -i message.txt -o encrypted.txt{RESET}

  5. Decrypt a text file:
     {CYAN}python prime_cipher.py -k 6 -i encrypted.txt -o decrypted.txt --mode decipher{RESET}

{GREEN}{BOLD}Interactive Mode (REPL):{RESET}
  -----------------------
  Executing the script without execution flags (-t, -d, or both -i and -o)
  will automatically launch the interactive command shell.

{RED}{BOLD}NOTE ON UNSUPPORTED FLAG COMBINATIONS:{RESET}
  {YELLOW}- Mixing inline parameters (-t/-d) with file flags (-i/-o) is unsupported.{RESET}
  {YELLOW}- Passing both -t and -d simultaneously is unsupported.{RESET}
  {YELLOW}- File operations require BOTH input (-i) AND output (-o) flags.{RESET}
  {YELLOW}- While the program may execute these unsupported combinations without crashing,{RESET}
  {YELLOW}  it will not behave as expected (flags may be ignored or yield unexpected results).{RESET}
"""
    parser = argparse.ArgumentParser(
        prog="prime_cipher.py",
        description="Prime Cipher CLI — Symmetric cipher tool using prime substitution and modular key shifting.",
        epilog=help_epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,
    )

    # Key offset argument definition
    parser.add_argument(
        "-k",
        "--key",
        type=int,
        default=0,
        metavar="INT",
        help="Numeric key offset for modular shifting (Caesar-like shift over primes). Default: 0.",
    )

    # Mutually exclusive group: prevents passing both -t and -d at the same time
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-t",
        "--text",
        type=str,
        metavar="TEXT",
        help="Plain text string to encrypt directly from the command line.",
    )
    mode_group.add_argument(
        "-d",
        "--decipher",
        type=str,
        metavar="PRIMES",
        help="Space-separated prime numbers sequence string to decrypt.",
    )

    # File processing arguments
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        metavar="FILE",
        help="Path to the input file to be processed.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        metavar="FILE",
        help="Path to the output file where the result will be saved.",
    )
    parser.add_argument(
        "--mode",
        choices=["cipher", "decipher"],
        default="cipher",
        help="Operation mode for file processing: 'cipher' (default) or 'decipher'.",
    )

    args = parser.parse_args()

    # Interactive Mode Fallback: Triggered when no primary processing flags are provided
    if not (args.text or args.decipher or (args.input and args.output)):
        # Defensive check: raise error if user passed only -i or only -o
        if args.input or args.output:
            print(
                f"{RED}[!] Error: File processing requires both input (-i/--input) and output (-o/--output) arguments.{RESET}"
            )
            print(
                f"{YELLOW}Example: python prime_cipher.py -k 6 -i input.txt -o output.txt{RESET}"
            )
            sys.exit(1)

        run_interactive_mode()
        return

    # Direct Execution / Batch Mode Handler
    if args.text:
        print(cipher_text(args.text, key_offset=args.key))

    elif args.decipher:
        print(decipher_text(args.decipher, key_offset=args.key))

    elif args.input and args.output:
        if args.mode == "cipher":
            process_file_encryption(args.input, args.output, key_offset=args.key)
        else:
            process_file_decryption(
                args.input, args.output, key_offset=args.key
            )


if __name__ == "__main__":
    main()