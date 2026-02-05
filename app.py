import customtkinter as ctk
from tkinter import filedialog
import requests, base64, threading, time, json, os
from pypresence import Presence

class NekoRPCApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NekoRPC")
        self.geometry("450x600")
        self.rpc = None
        self.config_file = "config.json"
        
        # UI Setup
        self.label = ctk.CTkLabel(self, text="NekoRPC", font=("Arial", 24, "bold"))
        self.label.pack(pady=10)

        self.cid_entry = ctk.CTkEntry(self, placeholder_text="Client ID", width=350)
        self.cid_entry.pack(pady=5)

        self.token_entry = ctk.CTkEntry(self, placeholder_text="Bot Token", width=350, show="*")
        self.token_entry.pack(pady=5)

        self.details_entry = ctk.CTkEntry(self, placeholder_text="Details (Top Line)", width=350)
        self.details_entry.pack(pady=5)

        self.state_entry = ctk.CTkEntry(self, placeholder_text="State (Bottom Line)", width=350)
        self.state_entry.pack(pady=5)

        self.img_btn = ctk.CTkButton(self, text="Select Image", command=self.select_image)
        self.img_btn.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="Start NekoRPC", fg_color="green", command=self.toggle_rpc)
        self.start_btn.pack(pady=10)

        self.load_config()

    def select_image(self):
        self.path = filedialog.askopenfilename()
        
    def save_config(self):
        data = {"cid": self.cid_entry.get(), "token": self.token_entry.get()}
        with open(self.config_file, "w") as f:
            json.dump(data, f)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.cid_entry.insert(0, data.get("cid", ""))
                self.token_entry.insert(0, data.get("token", ""))

    def toggle_rpc(self):
        if not self.rpc:
            self.save_config()
            self.rpc = Presence(self.cid_entry.get())
            self.rpc.connect()
            self.rpc.update(
                details=self.details_entry.get(),
                state=self.state_entry.get(),
                large_image="neko_img" # Note: requires upload logic from previous step
            )
            self.start_btn.configure(text="Stop", fg_color="red")
        else:
            self.rpc.close()
            self.rpc = None
            self.start_btn.configure(text="Start NekoRPC", fg_color="green")

if __name__ == "__main__":
    app = NekoRPCApp()
    app.mainloop()

