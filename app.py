import tkinter as tk
from tkinter import scrolledtext
import time
import threading
import random

# ------------------ FUNCTIONS ------------------ #
def run_command():
    cmd = command_entry.get()
    command_entry.delete(0, tk.END)
    
    if cmd.lower() == "hack":
        append_text("Initializing hack sequence...\n")
        threading.Thread(target=fake_hack).start()
    elif cmd.lower() == "decrypt":
        append_text("Decrypting files...\n")
        threading.Thread(target=fake_decrypt).start()
    elif cmd.lower() == "scan":
        append_text("Scanning network for vulnerabilities...\n")
        threading.Thread(target=fake_scan).start()
    elif cmd.lower() == "ping":
        append_text("Pinging 127.0.0.1...\n")
        threading.Thread(target=fake_ping).start()
    elif cmd.lower() == "trace":
        append_text("Tracing route to secret.server...\n")
        threading.Thread(target=fake_trace).start()
    elif cmd.lower().startswith("track "):
        name = cmd[6:].strip()
        append_text(f"Tracking {name}...\n")
        threading.Thread(target=fake_track, args=(name,)).start()
    else:
        append_text(f"Unknown command: {cmd}\n")

def append_text(txt):
    output_text.config(state='normal')
    output_text.insert(tk.END, txt)
    output_text.see(tk.END)
    output_text.config(state='disabled')

# ------------------ FAKE COMMANDS ------------------ #
def fake_hack():
    steps = ["Bypassing firewall", "Accessing mainframe", "Cracking password", "Downloading secrets"]
    for step in steps:
        append_text(f"{step}...\n")
        time.sleep(random.uniform(0.5, 1.5))
    append_text("Hack complete! Access Granted ✅\n\n")

def fake_decrypt():
    for i in range(5):
        append_text(f"Decrypting file_{i}.txt...\n")
        time.sleep(random.uniform(0.5, 1.2))
    append_text("All files decrypted! 🔑\n\n")

def fake_scan():
    targets = ["192.168.0.1", "192.168.0.2", "10.0.0.5", "10.0.0.12"]
    for t in targets:
        append_text(f"Found open port on {t}!\n")
        time.sleep(random.uniform(0.3, 0.8))
    append_text("Scan complete. Vulnerabilities found: 9\n\n")

def fake_ping():
    for i in range(4):
        latency = random.randint(1, 200)
        append_text(f"Reply from 127.0.0.1: time={latency}ms\n")
        time.sleep(0.5)
    append_text("Ping finished.\n\n")

def fake_trace():
    hops = ["10.0.0.1", "172.16.0.5", "192.168.1.2", "secret.server"]
    for h in hops:
        append_text(f"Hop to {h}...\n")
        time.sleep(random.uniform(0.4, 1.0))
    append_text("Trace complete.\n\n")

def fake_track(name):
    append_text(f"Locating {name}'s IP address...\n")
    time.sleep(1)
    append_text(f"{name} is currently on 192.168.1.2\n\n")

# ------------------ UI ------------------ #
root = tk.Tk()
root.title("Hacker Terminal")
root.geometry("600x400")
root.config(bg="black")

output_text = scrolledtext.ScrolledText(root, width=80, height=20, bg="black", fg="lime", insertbackground='lime')
output_text.pack(padx=10, pady=10)
output_text.config(state='disabled', font=("Courier", 12))

command_entry = tk.Entry(root, width=80, bg="black", fg="lime", insertbackground='lime', font=("Courier", 12))
command_entry.pack(padx=10, pady=(0,10))
command_entry.bind("<Return>", lambda event: run_command())

append_text("Welcome to Hacker Terminal! Type commands like 'hack', 'decrypt', 'scan', 'ping', 'trace', or 'track (name)'.\n\n")

root.mainloop()