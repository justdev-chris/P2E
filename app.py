# efivm_gui.py
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading

class EFIVM_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("stupid nigga efi thing")
        self.root.geometry("700x600")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Top frame - File selection
        top_frame = ttk.LabelFrame(self.root, text="EFI File", padding=10)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        self.file_path = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.file_path, width=50).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)
        
        # Middle frame - VM Settings
        middle_frame = ttk.LabelFrame(self.root, text="VM Settings", padding=10)
        middle_frame.pack(fill="x", padx=10, pady=10)
        
        # Memory
        ttk.Label(middle_frame, text="Memory (MB):").grid(row=0, column=0, sticky="w", pady=5)
        self.memory = ttk.Scale(middle_frame, from_=256, to=4096, length=300)
        self.memory.set(1024)
        self.memory.grid(row=0, column=1, pady=5)
        self.memory_label = ttk.Label(middle_frame, text="1024 MB")
        self.memory_label.grid(row=0, column=2, padx=10)
        self.memory.config(command=self.update_memory_label)
        
        # Display
        ttk.Label(middle_frame, text="Display:").grid(row=1, column=0, sticky="w", pady=5)
        self.display_var = tk.StringVar(value="gtk")
        displays = [("GTK", "gtk"), ("SDL", "sdl"), ("VNC", "vnc"), ("None", "none")]
        for i, (text, val) in enumerate(displays):
            ttk.Radiobutton(middle_frame, text=text, variable=self.display_var, value=val).grid(row=1, column=i+1, padx=5)
        
        # Additional options
        ttk.Label(middle_frame, text="Options:").grid(row=2, column=0, sticky="w", pady=5)
        self.smp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(middle_frame, text="Enable SMP (2 cores)", variable=self.smp_var).grid(row=2, column=1, sticky="w")
        self.audio_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(middle_frame, text="Enable Audio", variable=self.audio_var).grid(row=2, column=2, sticky="w")
        
        # Log output
        log_frame = ttk.LabelFrame(self.root, text="Output Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.pack(fill="both", expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start VM", command=self.start_vm, style="Accent.TButton")
        self.start_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Kill VM", command=self.kill_vm).pack(side="left", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
        
        self.vm_process = None
        
    def update_memory_label(self, value):
        self.memory_label.config(text=f"{int(float(value))} MB")
    
    def browse_file(self):
        file = filedialog.askopenfilename(
            title="Select EFI File",
            filetypes=[("EFI files", "*.efi"), ("All files", "*.*")]
        )
        if file:
            self.file_path.set(file)
            self.log(f"Selected: {file}")
    
    def log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def start_vm(self):
        efi_file = self.file_path.get()
        if not os.path.exists(efi_file):
            messagebox.showerror("Error", "Please select an EFI file")
            return
        
        # Create temp image
        self.log("Creating virtual disk image...")
        try:
            subprocess.run(["dd", "if=/dev/zero", "of=/tmp/efivm.img", "bs=1M", "count=64"], 
                          capture_output=True, check=False)
            subprocess.run(["mkfs.vfat", "/tmp/efivm.img"], capture_output=True, check=False)
            
            # Copy EFI file
            mmd_cmd = ["mmd", "-i", "/tmp/efivm.img", "::/EFI", "::/EFI/BOOT"]
            subprocess.run(mmd_cmd, capture_output=True, check=False)
            
            mcopy_cmd = ["mcopy", "-i", "/tmp/efivm.img", efi_file, "::/EFI/BOOT/BOOTX64.EFI"]
            subprocess.run(mcopy_cmd, capture_output=True, check=False)
        except Exception as e:
            self.log(f"Error creating image: {e}")
            return
        
        # Build QEMU command
        cmd = ["qemu-system-x86_64"]
        cmd.extend(["-m", str(int(self.memory.get()))])
        
        # Add cores if SMP enabled
        if self.smp_var.get():
            cmd.extend(["-smp", "2"])
        
        # Display
        display = self.display_var.get()
        if display != "none":
            cmd.extend(["-display", display])
        
        # Audio
        if self.audio_var.get():
            cmd.extend(["-soundhw", "hda"])
        
        # VM configuration
        cmd.extend([
            "-drive", f"file=/tmp/efivm.img,format=raw",
            "-bios", "/usr/share/OVMF/OVMF_CODE.fd",
            "-vga", "std",
            "-net", "none",
            "-monitor", "stdio"
        ])
        
        self.log(f"Starting VM with command: {' '.join(cmd)}")
        self.status_var.set("Starting VM...")
        self.start_btn.config(state="disabled")
        
        # Run in thread
        thread = threading.Thread(target=self.run_vm, args=(cmd,))
        thread.daemon = True
        thread.start()
    
    def run_vm(self, cmd):
        try:
            self.vm_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.log("VM started successfully")
            self.status_var.set("VM running")
            
            # Read output
            for line in iter(self.vm_process.stdout.readline, ''):
                if line:
                    self.log(line.strip())
            
            self.vm_process.stdout.close()
            return_code = self.vm_process.wait()
            
            if return_code == 0:
                self.log("VM exited normally")
            else:
                self.log(f"VM exited with code: {return_code}")
                
        except Exception as e:
            self.log(f"Error running VM: {e}")
        finally:
            self.start_btn.config(state="normal")
            self.status_var.set("Ready")
            self.vm_process = None
    
    def kill_vm(self):
        if self.vm_process:
            self.log("Killing VM process...")
            self.vm_process.terminate()
            try:
                self.vm_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.vm_process.kill()
            self.vm_process = None
            self.log("VM terminated")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EFIVM_GUI()
    app.run()