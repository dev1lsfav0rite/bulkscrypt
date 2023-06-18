# bulkscrypt
Python script for a recursive bulk encryption/decryption of files using scrypt.

# How does it work?
In a directory you want to encrypt/decrypt, it creates a new directory called ```scrypt_encrypted``` / ```scrypt_decrypted``` (depending on what you're doing with it), recursively replicates the folder structure of the base directory, and then encrypts files in their folders with a password using a ```scrypt``` package.

# Prerequisites
- scrypt
  - Debian/Ubuntu
    - ```apt-get install scrypt```
  - Arch
    - ```pacman -S scrypt```
  - MacOS
    - ```brew install scrypt```
- python3
- required libraries
  - ```pip install -r requirements.txt```

# Usage:
```bash
python3 scrypt.py {enc|dec} {PATH}
```
