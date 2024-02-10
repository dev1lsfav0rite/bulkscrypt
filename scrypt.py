import os
import sys
from getpass import getpass
from pathlib import Path

# Gets user input
try:
    encdec=sys.argv[1]
    source=str(Path(sys.argv[2]).resolve())
    if encdec == "enc" or encdec == "dec":
        pass
    else:
        print("Usage: python3 scrypt.py {enc|dec} {PATH}")
        exit()
except:
    print("Usage: python3 scrypt.py {enc|dec} {PATH}")
    exit()

# Create (sub)directories
def copy_dirs(src, dst):
    for item in os.listdir(src):
        if item == "scrypt_encrypted" or item =="scrypt_decrypted":
            continue
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            copy_dirs(s, d)
    
# Encryption function
def encrypt():
    global password,files,filesStrip
    for x in range(len(files)):
        print("Encrypting file",x+1,"of total",len(files),f"files. Filename: {filesStrip[x]}")
        command='scrypt enc --passphrase dev:stdin-once "{:0}" "{:1}{:2}.enc"'.format(files[x],destination,filesStrip[x])
        os.system(f"echo '{password}' | {command}")
    print()
    print("Encrypted",len(files),"files.")
        
# Decryption function
def decrypt():
    global password,files,filesStrip
    for x in range(len(files)):
        print("Decrypting file",x+1,"of total",len(files),f"files. Filename: {filesStrip[x]}")
        filesStrip[x]=filesStrip[x].replace(".enc","")
        command='scrypt dec --passphrase dev:stdin-once "{:0}" "{:1}{:2}"'.format(files[x],destination,filesStrip[x])
        os.system(f"echo '{password}' | {command}")
    print()
    print("Decrypted",len(files),"files.")
 
def get_password(encdec):
    if encdec == 'enc':
        prompt="Encryption password:"
    else:
        prompt="Decryption password:"
    password=getpass(prompt=prompt) # Password
    if encdec == 'enc':
        conPassword=getpass(prompt='Confirm password:') # Confirm Password
        if password!=conPassword:
            print("Passwords do not match!")
            exit()
    try:
        os.mkdir(destination) # Make a directory for encrypted files
    except FileExistsError:
        pass
    copy_dirs(source, destination)
    return password
    
# Makes a list of all files in a given PATH directory
files=[]
for root,d_names,f_names in os.walk(source):
    for f in f_names:
        if ".DS_Store" not in f:
            files.append(os.path.join(root, f))

filesStrip=[]
for x in files:
    filesStrip.append(x.replace(source,""))

# Encryption
if encdec == 'enc':
    destination=source+"/scrypt_encrypted/"
    password = get_password(encdec)
    encrypt()

# Decryption
elif encdec == 'dec':
    destination=source+"/scrypt_decrypted/"
    password = get_password(encdec)
    decrypt()

else:
    print("Usage: python3 scrypt.py {enc|dec} {PATH}")
    exit()