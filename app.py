import customtkinter as ctk
from pypresence import Presence
import json
import os

class NekoRPC(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("NekoRPC")
        self.geometry("400x550")
        self.rpc = None

        # --- UI Elements ---
        ctk.CTkLabel(self, text="NekoRPC Controller", font=("Arial", 20, "bold")).pack(pady=20)

        # Client ID Field
        ctk.CTkLabel(self, text="Client ID (Application ID):").pack(pady=(10, 0))
        self.cid_entry = ctk.CTkEntry(self, width=300, placeholder_text="Paste Application ID here")
        self.cid_entry.pack(pady=5)

        # Activity Type Dropdown
        ctk.CTkLabel(self, text="Activity Type:").pack(pady=(10, 0))
        self.type_dropdown = ctk.CTkOptionMenu(self, values=["Playing", "Listening", "Watching", "Competing"])
        self.type_dropdown.pack(pady=5)

        # Details and State
        ctk.CTkLabel(self, text="Details (Top Line):").pack(pady=(10, 0))
        self.details_entry = ctk.CTkEntry(self, width=300)
        self.details_entry.pack(pady=5)

        ctk.CTkLabel(self, text="State (Bottom Line):").pack(pady=(10, 0))
        self.state_entry = ctk.CTkEntry(self, width=300)
        self.state_entry.pack(pady=5)

        # Large Image Key (From Art Assets)
        ctk.CTkLabel(self, text="Large Image Key:").pack(pady=(10, 0))
        self.image_entry = ctk.CTkEntry(self, width=300, placeholder_text="e.g., neko_main")
        self.image_entry.pack(pady=5)

        # Start/Stop Button
        self.start_btn = ctk.CTkButton(self, text="Start RPC", command=self.toggle_rpc, fg_color="green", height=40)
        self.start_btn.pack(pady=30)

        # Load saved data
        self.load_config()

    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    self.cid_entry.insert(0, data.get("cid", ""))
                    self.image_entry.insert(0, data.get("image", ""))
            except:
                pass

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump({
                "cid": self.cid_entry.get().strip(),
                "image": self.image_entry.get().strip()
            }, f)

    def toggle_rpc(self):
        if self.rpc is None:
            try:
                # 1. Get and clean the Client ID
                client_id = str(self.cid_entry.get().strip())
                
                if not client_id:
                    print("Error: Client ID is empty")
                    return

                # 2. Connect to Discord
                self.rpc = Presence(client_id)
                self.rpc.connect()

                # 3. Map Activity Type
                activity_map = {"Playing": 0, "Listening": 2, "Watching": 3, "Competing": 5}
                act_type = activity_map.get(self.type_dropdown.get(), 0)

                # 4. Push Update
                self.rpc.update(
                    details=str(self.details_entry.get()),
                    state=str(self.state_entry.get()),
                    large_image=str(self.image_entry.get().strip()),
                    activity_type=act_type
                )
                
                self.save_config()
                self.start_btn.configure(text="Stop RPC", fg_color="red")
                print("RPC Started Successfully")

            except Exception as e:
                print(f"Detailed Error: {e}")
                self.rpc = None
        else:
            try:
                self.rpc.close()
            except:
                pass
            self.rpc = None
            self.start_btn.configure(text="Start RPC", fg_color="green")
            print("RPC Stopped")

if __name__ == "__main__":
    app = NekoRPC()
    app.mainloop()
