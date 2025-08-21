import tkinter as tk
from tkinter import scrolledtext
import time
import os

# 🧠 PyCat Interpreter
def interpret_line(line, output_box, variables={}):
    tokens = line.strip().split()
    if not tokens:
        return

    cmd = tokens[0]

    try:
        if cmd == "meow" and tokens[1] == "canvas":
            w, h = int(tokens[2]), int(tokens[3])
            output_box.insert(tk.END, f"🐱 Canvas created: {w}x{h}\n")
        elif cmd == "purr" and tokens[1] == "color":
            color = tokens[2]
            output_box.insert(tk.END, f"🎨 Color set to {color}\n")
        elif cmd == "draw" and tokens[1] == "box":
            x, y = int(tokens[3]), int(tokens[4])
            w, h = int(tokens[6]), int(tokens[7])
            output_box.insert(tk.END, f"📦 Drawing box at ({x},{y}) size {w}x{h}\n")
        elif cmd == "nap":
            seconds = int(tokens[1])
            output_box.insert(tk.END, f"😴 Napping for {seconds} seconds...\n")
            output_box.update()
            time.sleep(seconds)
        elif cmd == "lick":
            compliments = [
                "You're doing amazing work 🐾",
                "Your code smells like catnip — in a good way 😸",
                "Keep going, cozy coder!",
                "This language is purring with potential!"
            ]
            output_box.insert(tk.END, f"{compliments[int(time.time()) % len(compliments)]}\n")
        elif cmd == "run":
            filename = tokens[1]
            if not os.path.exists(filename):
                output_box.insert(tk.END, f"🚫 File not found: {filename}\n")
            else:
                output_box.insert(tk.END, f"📂 Running {filename}\n")
                with open(filename, "r") as f:
                    for file_line in f:
                        interpret_line(file_line.strip(), output_box, variables)
        elif cmd == "paw":
            var_name = tokens[1]
            value = " ".join(tokens[3:])
            variables[var_name] = value
            output_box.insert(tk.END, f"🐾 Set {var_name} = {value}\n")
        elif cmd == "peek":
            var_name = tokens[1]
            value = variables.get(var_name, "undefined")
            output_box.insert(tk.END, f"👀 {var_name} = {value}\n")
        else:
            output_box.insert(tk.END, f"❓ Unknown command: {line}\n")
    except Exception as e:
        output_box.insert(tk.END, f"😿 PyCat got confused: {e}\n")

# 🖥️ GUI Setup
def launch_gui():
    root = tk.Tk()
    root.title("🐾 PyCat Terminal")

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Courier", 12))
    output_box.pack(padx=10, pady=10)

    input_entry = tk.Entry(root, width=60, font=("Courier", 12))
    input_entry.pack(pady=5)

    variables = {}

    def on_enter(event=None):
        line = input_entry.get()
        output_box.insert(tk.END, f"> {line}\n")
        interpret_line(line, output_box, variables)
        input_entry.delete(0, tk.END)

    input_entry.bind("<Return>", on_enter)

    root.mainloop()

# 🐱 Start the GUI
if __name__ == "__main__":
    launch_gui()
