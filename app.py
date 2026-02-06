import customtkinter as ctk
from pypresence import Presence
import json
import os

class NekoRPC(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NekoRPC")
        self.geometry("400x550")
        self.rpc = None

        ctk.CTkLabel(self, text="NekoRPC Controller", font=("Arial", 20, "bold")).pack(pady=20)

        # Client ID
        ctk.CTkLabel(self, text="Client ID:").pack(pady=(10, 0))
        self.cid_entry = ctk.CTkEntry(self, width=300)
        self.cid_entry.pack(pady=5)

        # Activity Type
        ctk.CTkLabel(self, text="Activity Type:").pack(pady=(10, 0))
        self.type_dropdown = ctk.CTkOptionMenu(self, values=["Playing", "Listening", "Watching", "Competing"])
        self.type_dropdown.pack(pady=5)

        # Details/State
        ctk.CTkLabel(self, text="Details:").pack(pady=(10, 0))
        self.details_entry = ctk.CTkEntry(self, width=300)
        self.details_entry.pack(pady=5)

        ctk.CTkLabel(self, text="State:").pack(pady=(10, 0))
        self.state_entry = ctk.CTkEntry(self, width=300)
        self.state_entry.pack(pady=5)

        # Image Key
        ctk.CTkLabel(self, text="Image Key:").pack(pady=(10, 0))
        self.image_entry = ctk.CTkEntry(self, width=300)
        self.image_entry.pack(pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start RPC", command=self.toggle_rpc, fg_color="green")
        self.start_btn.pack(pady=30)

        self.load_config()

    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    self.cid_entry.insert(0, str(data.get("cid", "")))
                    self.image_entry.insert(0, str(data.get("image", "")))
            except: pass

    def toggle_rpc(self):
        if self.rpc is None:
            client_id = self.cid_entry.get().strip()
            if not client_id:
                print("Error: Paste your Client ID first!")
                return
            
            try:
                # Initialize and Connect
                self.rpc = Presence(client_id)
                self.rpc.connect()

                # Get values
                activity_map = {"Playing": 0, "Listening": 2, "Watching": 3, "Competing": 5}
                act_type = activity_map.get(self.type_dropdown.get(), 0)
                
                # Push Update
                self.rpc.update(
                    details=str(self.details_entry.get()),
                    state=str(self.state_entry.get()),
                    large_image=str(self.image_entry.get().strip()),
                    activity_type=act_type
                )
                
                # Save config
                with open("config.json", "w") as f:
                    json.dump({"cid": client_id, "image": self.image_entry.get().strip()}, f)

                self.start_btn.configure(text="Stop RPC", fg_color="red")
                print("Connected to Discord!")

            except Exception as e:
                print(f"CONNECTION ERROR: {e}")
                self.rpc = None # Reset so we can try again
        else:
            try:
                self.rpc.close()
            except: pass
            self.rpc = None
            self.start_btn.configure(text="Start RPC", fg_color="green")
            print("Disconnected.")

if __name__ == "__main__":
    app = NekoRPC()
    app.mainloop()
