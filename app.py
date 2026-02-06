import customtkinter as ctk
from pypresence import Presence
from PIL import Image
import json
import os

class NekoRPC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NekoRPC")
        self.geometry("450x750")
        self.rpc = None
        self.preview_img = None

        # --- UI Elements ---
        ctk.CTkLabel(self, text="Client ID:").pack(pady=(10, 0))
        self.cid_entry = ctk.CTkEntry(self, width=300)
        self.cid_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Activity Type:").pack(pady=(10, 0))
        self.type_dropdown = ctk.CTkOptionMenu(self, values=["Playing", "Listening", "Watching", "Competing"])
        self.type_dropdown.pack(pady=5)

        ctk.CTkLabel(self, text="Details (Top Line):").pack(pady=(10, 0))
        self.details_entry = ctk.CTkEntry(self, width=300)
        self.details_entry.pack(pady=5)

        ctk.CTkLabel(self, text="State (Bottom Line):").pack(pady=(10, 0))
        self.state_entry = ctk.CTkEntry(self, width=300)
        self.state_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Discord Image Key:").pack(pady=(10, 0))
        self.image_entry = ctk.CTkEntry(self, width=300, placeholder_text="Enter key from Dev Portal")
        self.image_entry.pack(pady=5)

        # --- Image Preview Section ---
        self.preview_label = ctk.CTkLabel(self, text="No Image Selected", width=200, height=200, fg_color="gray20", corner_radius=10)
        self.preview_label.pack(pady=10)

        self.upload_btn = ctk.CTkButton(self, text="Select Preview Image", command=self.select_image)
        self.upload_btn.pack(pady=5)

        self.file_path_label = ctk.CTkLabel(self, text="File: None", font=("Arial", 10), text_color="gray")
        self.file_path_label.pack()

        # --- Control Buttons ---
        self.status_indicator = ctk.CTkLabel(self, text="● Offline", text_color="red")
        self.status_indicator.pack(pady=5)

        self.start_btn = ctk.CTkButton(self, text="Start RPC", command=self.toggle_rpc, fg_color="green", height=40)
        self.start_btn.pack(pady=20)

        self.load_config()

    def select_image(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            # Show the filename
            filename = os.path.basename(file_path)
            self.file_path_label.configure(text=f"File: {filename}")

            # Create the preview
            img = Image.open(file_path)
            self.preview_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))
            self.preview_label.configure(image=self.preview_img, text="")

    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    data = json.load(f)
                    self.cid_entry.insert(0, data.get("cid", ""))
                    self.image_entry.insert(0, data.get("image", ""))
            except: pass

    def save_config(self):
        with open("config.json", "w") as f:
            json.dump({"cid": self.cid_entry.get(), "image": self.image_entry.get()}, f)

    def toggle_rpc(self):
        if self.rpc is None:
            try:
                self.save_config()
                self.rpc = Presence(self.cid_entry.get())
                self.rpc.connect()

                activity_map = {"Playing": 0, "Listening": 2, "Watching": 3, "Competing": 5}
                act_type = activity_map.get(self.type_dropdown.get(), 0)

                self.rpc.update(
                    details=self.details_entry.get(),
                    state=self.state_entry.get(),
                    large_image=self.image_entry.get(),
                    activity_type=act_type
                )
                
                self.status_indicator.configure(text="● Online", text_color="green")
                self.start_btn.configure(text="Stop RPC", fg_color="red")
            except Exception as e:
                self.status_indicator.configure(text=f"● Error: {str(e)[:20]}...", text_color="yellow")
        else:
            self.rpc.close()
            self.rpc = None
            self.status_indicator.configure(text="● Offline", text_color="red")
            self.start_btn.configure(text="Start RPC", fg_color="green")

if __name__ == "__main__":
    app = NekoRPC()
    app.mainloop()
