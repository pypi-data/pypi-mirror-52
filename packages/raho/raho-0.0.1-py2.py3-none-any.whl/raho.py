#!/usr/bin/env python

import argparse
import binascii
from base64 import urlsafe_b64decode, urlsafe_b64encode
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import getpass
import os
import sys

USAGE_EXAMPLE = """Example:

    $ raho generate
    Generating key: /path/to/key/file
    $ echo 'secret message' | raho encrypt > encrypted
    $ cat encrypted | raho decrypt
    secret message

Example with non-echoed text input:

    $ raho encrypt --prompt-text > encrypted
    Text to Encrypt: <enter clear text>
    $ raho decrypt --prompt-text
    Text to Decrypt: <enter encrypted text>
    secret message

Example using a password:

    $ echo 'secret message' | raho encrypt --password > encrypted
    Password: <enter password>
    $ cat encrypted | raho decrypt --password
    Password: <enter password>
    secret message

For more infromation, see https://github.com/abhayagiri/raho.

For more information on the supporting library, see https://cryptography.io/.
"""

DEFAULT_KEY_FILE = '.raho-key'


def decrypt(b64_encrypted, fernet):
    """Decrypt encrypted text.

    A ValueError will be thrown when encrypted is invalid or the key is
    incorrect."""
    try:
        encrypted = urlsafe_b64decode(b64_encrypted.encode())
        return fernet.decrypt(encrypted).decode()
    except (TypeError, binascii.Error):
        raise ValueError('Invalid encrypted format')
    except InvalidToken:
        raise ValueError('Invalid encrypted format or incorrect key')


def decrypt_with_key_file(b64_encrypted, key_file):
    """Decrypt encrypted text with a key file."""
    fernet = get_key_file_fernet(key_file)
    return decrypt(b64_encrypted, fernet)


def decrypt_with_password(b64_encrypted_and_salt, password):
    """Decrypt encrypted text with a password.

    A ValueError will be thrown when encrypted is invalid or the password is
    incorrect."""
    try:
        b64_encrypted, base_64_salt = b64_encrypted_and_salt.split(',', 1)
        salt = urlsafe_b64decode(base_64_salt.encode())
    except (TypeError, ValueError, binascii.Error):
        raise ValueError('Invalid encrypted format')
    fernet = get_password_fernet(password, salt)
    return decrypt(b64_encrypted, fernet)


def encrypt(text, fernet):
    """Encrypt some text."""
    encrypted = fernet.encrypt(text.encode())
    return urlsafe_b64encode(encrypted).decode()


def encrypt_with_key_file(text, key_file):
    """Encrypt some text with a key file."""
    fernet = get_key_file_fernet(key_file)
    return encrypt(text, fernet)


def encrypt_with_password(text, password):
    """Encrypt some text with a password."""
    salt = os.urandom(16)
    fernet = get_password_fernet(password, salt)
    b64_encrypted = encrypt(text, fernet)
    b64_salt = urlsafe_b64encode(salt).decode()
    return b64_encrypted + ',' + b64_salt


def generate_fernet():
    """Generate and return a Fernet."""
    key = Fernet.generate_key()
    return Fernet(key)


def generate_key_file(key_file):
    """Safely generate and write a key to a key file."""
    # https://stackoverflow.com/a/33223732
    fd = os.open(key_file, os.O_CREAT | os.O_EXCL)
    os.close(fd)
    os.chmod(key_file, 0o600)
    key = Fernet.generate_key()
    with open(key_file, 'w') as f:
        f.write(urlsafe_b64encode(key).decode())


def get_password_fernet(password, salt):
    """Return a Fernet for a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)


def get_key_file_fernet(key_file):
    """Return a key from a key file."""
    with open(key_file) as f:
        b64_key = f.read()
    try:
        key = urlsafe_b64decode(b64_key)
    except (TypeError, binascii.Error):
        raise ValueError('Invalid key format')
    return Fernet(key)


def main(sys_args=None):
    parser = argparse.ArgumentParser(
        description='Simple symmetric encryption built on cryptography.',
        epilog=USAGE_EXAMPLE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('command', choices=('generate', 'encrypt', 'decrypt'))
    parser.add_argument('-k', '--key-file', default=DEFAULT_KEY_FILE,
                        help='path to the key file')
    parser.add_argument('-p', '--password', action='store_true',
                        help='prompt for a password and use that instead of a key file')
    parser.add_argument('-t', '--prompt-text', action='store_true',
                        help='prompt for text to be encrypted/decrypted')
    args = parser.parse_args(args=sys_args)
    key_file = os.path.abspath(args.key_file)

    if args.command == 'generate':
        _print_stdout('Generating key: %s' % key_file)
        generate_key_file(key_file)
        return

    if args.password:
        password = getpass.getpass()

    if args.prompt_text:
        prompt = 'Text to %s: ' % args.command.title()
        text = getpass.getpass(prompt=prompt)
    else:
        text = _read_stdin()

    if args.command == 'encrypt':
        if args.password:
            output = encrypt_with_password(text, password)
        else:
            output = encrypt_with_key_file(text, key_file)
    else:  # decrypt
        if args.password:
            output = decrypt_with_password(text, password)
        else:
            output = decrypt_with_key_file(text, key_file)

    _print_stdout(output)


def _read_stdin():
    return sys.stdin.read()


def _print_stdout(text):
    print(text)


if __name__ == '__main__':
    main()
