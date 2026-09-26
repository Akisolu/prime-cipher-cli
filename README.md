# Prime Cipher CLI

![Build status](https://github.com/Akisolu/prime-cipher-cli/actions/workflows/build.yml/badge.svg)

Prime Cipher CLI is a lightweight command-line tool that encrypts and decrypts text using prime-based encoded values. It can process inline text as well as files, making it useful for quick experiments and simple data obfuscation.

## Features

- Encrypt plain text into prime-number sequences
- Decrypt prime-number sequences back to text
- Encrypt and decrypt files from the command line
- Simple interactive terminal interface

## Usage

Run the script with Python:

```bash
python prime_cipher.py
```

Available commands include:

```bash
cipher Hello World
decipher 3 2 67
cipher-file input.txt output.txt
decipher-file input.txt output.txt
menu
exit
```

## Releases

Download the latest executable from the GitHub Releases page:

https://github.com/Akisolu/prime-cipher-cli/releases

The latest release includes a ready-to-run binary for supported platforms.

## Windows warning

On Windows, when you run the downloaded executable, you may see a warning such as "Windows protected your PC" or an alert that the file is unrecognized or potentially dangerous. This is a common warning for downloaded executables that are not signed by a trusted certificate.

If this happens:

1. Click More info
2. Click Run anyway
3. Continue using the application normally

This warning does not necessarily mean the file is malicious, but it is important to only download executables from the official GitHub Releases page.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
