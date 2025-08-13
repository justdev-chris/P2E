import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
import os
import shutil

VAULT_FILE = "vault_data.json"
PIN = "1234"  # nuh uh uhh

# Load or create vault data
if not os.path.exists(VAULT_FILE):
    with open(VAULT_FILE, "w") as f:
        json.dump({"texts": [], "files": []}, f)

with open(VAULT_FILE, "r") as f:
    vault = json.load(f)

# Functions
def save_vault():
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)

def add_text():
    text = simpledialog.askstring("Add Text/Password", "Enter text to save:")
    if text:
        vault["texts"].append(text)
        save_vault()
        refresh_lists()

def add_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        dest_folder = os.path.join(os.getcwd(), "vault_files")
        os.makedirs(dest_folder, exist_ok=True)
        filename = os.path.basename(file_path)
        dest_path = os.path.join(dest_folder, filename)
        shutil.copy(file_path, dest_path)
        vault["files"].append(dest_path)
        save_vault()
        refresh_lists()

def copy_text():
    selected = text_listbox.curselection()
    if selected:
        text = vault["texts"][selected[0]]
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Copied!", "Text copied to clipboard!")

def open_file():
    selected = file_listbox.curselection()
    if selected:
        path = vault["files"][selected[0]]
        if os.path.exists(path):
            os.startfile(path)
        else:
            messagebox.showerror("Error", "File not found!")

def refresh_lists():
    text_listbox.delete(0, tk.END)
    for t in vault["texts"]:
        text_listbox.insert(tk.END, t if len(t) <= 20 else t[:20]+"...")
        file_listbox.delete(0, tk.END)
    for f in vault["files"]:
        file_listbox.insert(tk.END, os.path.basename(f))

# PIN Lock
def ask_pin():
    entered = simpledialog.askstring("Vault PIN", "Enter your PIN:", show='*')
    if entered != PIN:
        messagebox.showerror("Wrong PIN", "Incorrect PIN! Bye~ 😿")
        root.destroy()

# GUI Setup
root = tk.Tk()
root.title("My Vault 🐾")

ask_pin()

tk.Label(root, text="Saved Texts/Passwords:").pack()
text_listbox = tk.Listbox(root, width=50)
text_listbox.pack()
tk.Button(root, text="Add Text", command=add_text).pack()
tk.Button(root, text="Copy Selected Text", command=copy_text).pack()

tk.Label(root, text="Saved Files:").pack(pady=(10,0))
file_listbox = tk.Listbox(root, width=50)
file_listbox.pack()
tk.Button(root, text="Add File", command=add_file).pack()
tk.Button(root, text="Open Selected File", command=open_file).pack()

refresh_lists()
root.mainloop()
