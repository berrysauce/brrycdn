# BRRYCDN INSTALLER #####################################
import os
from tools import hashing
import sys

print("/// BRRY CDN /// SETUP //////////////////////////")
print("[1/3] Which password would you like to use?")
unhashed_pass = str(input("> "))
print("[2/3] How long should file IDs be?")
id_len = str(int(input("> ")))
print("[3/3] What is the domain? (without https://)")
domain = str(input("> "))
print("/////////////////////////////////////////////////")
print("[...] Creating files directory")
os.mkdir("files")
print("[...] Hashing & salting password")
hashed_pass = hashing.hashpw(unhashed_pass)
print("[...] Verifying hashed password")
if hashing.verifypw(hashed_pass, unhashed_pass) is True:
    print("[ ✓ ] Hashed password verified")
else:
    sys.exit("[ ! ] Hashed password could not be verified")
print("[...] Writing .env")
with open(".env", "w") as env:
    env.write(f'PASSWORD = "{hashed_pass}"\nID_LEN = "{id_len}"\nDOMAIN = "{domain}"')
print("/ ✓ SETUP DONE ///////////////////////////////////")
print("[...] Starting server")
exec(open("main.py").read())
