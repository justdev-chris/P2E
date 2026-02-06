import customtkinter as ctk
from pypresence import Presence, ActivityType # Added ActivityType here
import json
import os

class NekoRPC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NekoRPC")
        self.geometry("400x500")
        self.rpc = None

        # UI
        ctk.CTkLabel(self, text="NekoRPC (Console Active)", text_color="cyan").pack(pady=10)
        
        self.cid_entry = ctk.CTkEntry(self, width=300, placeholder_text="Client ID")
        self.cid_entry.pack(pady=5)
        
        self.details_entry = ctk.CTkEntry(self, width=300, placeholder_text="Details")
        self.details_entry.pack(pady=5)
        
        self.image_entry = ctk.CTkEntry(self, width=300, placeholder_text="Image Key")
        self.image_entry.pack(pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start RPC", command=self.toggle_rpc)
        self.start_btn.pack(pady=20)

    def toggle_rpc(self):
        if self.rpc is None:
            client_id = self.cid_entry.get().strip()
            print(f"Connecting to ID: {client_id}")
            
            try:
                self.rpc = Presence(client_id)
                self.rpc.connect()

                # Fix: Use ActivityType.PLAYING instead of the number 0
                self.rpc.update(
                    details=str(self.details_entry.get()),
                    large_image=str(self.image_entry.get().strip()),
                    activity_type=ActivityType.PLAYING 
                )
                
                print("Successfully updated Presence!")
                self.start_btn.configure(text="Stop", fg_color="red")
            except Exception as e:
                print(f"Connection error: {e}")
                self.rpc = None
        else:
            self.rpc.close()
            self.rpc = None
            print("RPC Stopped.")
            self.start_btn.configure(text="Start", fg_color="green")

if __name__ == "__main__":
    app = NekoRPC()
    app.mainloop()
