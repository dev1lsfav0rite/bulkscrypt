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
        print("Encrypting file",x+1,"of total",len(files),"files.")
        command='scrypt enc --passphrase dev:stdin-once "{:0}" "{:1}{:2}.enc"'.format(files[x],destination,filesStrip[x])
        os.system(f"echo '{password}' | {command}")
    print()
    print("Encrypted",len(files),"files.")
        
# Decryption function
def decrypt():
    global password,files,filesStrip
    for x in range(len(files)):
        print("Decrypting file",x+1,"of total",len(files),"files.")
        filesStrip[x]=filesStrip[x].replace(".enc","")
        command='scrypt dec --passphrase dev:stdin-once "{:0}" "{:1}{:2}"'.format(files[x],destination,filesStrip[x])
        os.system(f"echo '{password}' | {command}")
    print("Decrypted",len(files),"files.")
 
    
# Makes a list of all files in a given PATH directory
files=[]
for root,d_names,f_names in os.walk(source):
	for f in f_names:
		files.append(os.path.join(root, f))
filesStrip=[]
for x in files:
    filesStrip.append(x.replace(source,""))

# Encryption
if encdec == 'enc':
    destination=source+"/scrypt_encrypted/"
    password=getpass(prompt='Encryption password:') # Password
    try:
        os.mkdir(destination) # Make a directory for encrypted files
    except FileExistsError:
        pass
    copy_dirs(source, destination)
    encrypt()

# Decryption
elif encdec == 'dec':
    destination=source+"/scrypt_decrypted/"
    password=getpass(prompt='Decryption password:') # Password
    try:
        os.mkdir(destination) # Make a directory for decrypted files
    except FileExistsError:
        pass
    copy_dirs(source, destination)
    decrypt()

else:
    print("Usage: python3 scrypt.py {enc|dec} {PATH}")
    exit()