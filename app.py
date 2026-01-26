# Save as install.py
import os, shutil, sys

# Auto-install without prompts
exe = 'pycat.exe'
dest = os.path.join(os.environ['WINDIR'], 'System32', 'pycat.exe')

if os.path.exists(exe):
    try:
        shutil.copy(exe, dest)
        print(f"Installed! Use: pycat --help")
    except:
        print("Run as Admin!")
else:
    print(f"Place {exe} next to this script")
input()
