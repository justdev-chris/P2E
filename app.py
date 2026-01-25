# efivm_gui_windows.py
import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import tempfile
import struct

class EFIVM_GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("stupid nigger efi thing")
        self.root.geometry("700x600")
        
        # Check for QEMU
        self.check_qemu()
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Top frame - File selection
        top_frame = ttk.LabelFrame(self.root, text="EFI File", padding=10)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        self.file_path = tk.StringVar()
        ttk.Entry(top_frame, textvariable=self.file_path, width=50).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Browse", command=self.browse_file).pack(side="left", padx=5)
        
        # QEMU path
        ttk.Label(top_frame, text="QEMU Path:").pack(side="left", padx=(20, 5))
        self.qemu_path = tk.StringVar(value=self.find_qemu())
        ttk.Entry(top_frame, textvariable=self.qemu_path, width=30).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Find", command=self.find_qemu_gui).pack(side="left", padx=5)
        
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
        displays = [("SDL", "sdl"), ("GTK", "gtk"), ("VNC", "vnc"), ("None", "none")]
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
        
        self.start_btn = ttk.Button(button_frame, text="▶ Start VM", command=self.start_vm)
        self.start_btn.pack(side="left", padx=5)
        
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Kill VM", command=self.kill_vm).pack(side="left", padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
        
        self.vm_process = None
        
    def check_qemu(self):
        """Check if QEMU is installed"""
        try:
            result = subprocess.run(["where", "qemu-system-x86_64"], 
                                   capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                self.log("QEMU not found in PATH. Please install QEMU for Windows.")
        except:
            pass
    
    def find_qemu(self):
        """Try to find QEMU installation"""
        # Common QEMU installation paths on Windows
        paths = [
            r"C:\Program Files\qemu\qemu-system-x86_64.exe",
            r"C:\Program Files (x86)\qemu\qemu-system-x86_64.exe",
            r"C:\qemu\qemu-system-x86_64.exe",
            "qemu-system-x86_64.exe"  # Try PATH
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        return "qemu-system-x86_64.exe"
    
    def find_qemu_gui(self):
        """Open file dialog to find QEMU"""
        file = filedialog.askopenfilename(
            title="Find qemu-system-x86_64.exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if file:
            self.qemu_path.set(file)
    
    def create_fat32_image(self, size_mb=64, efi_file=None):
        """Create a FAT32 disk image for Windows"""
        import ctypes
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        img_path = os.path.join(temp_dir, "efivm.img")
        
        self.log(f"Creating FAT32 image at: {img_path}")
        
        # Create empty file
        with open(img_path, 'wb') as f:
            f.write(b'\x00' * (size_mb * 1024 * 1024))
        
        # Format as FAT32 using Windows format command
        # Note: This requires admin rights or alternative method
        # For simplicity, we'll create a minimal FAT12/16/32 manually
        
        # Actually, let's use a simpler approach - download a pre-made empty image
        # or use Python to create a basic FAT
        
        # Alternative: Use PowerShell to format
        try:
            ps_cmd = f'''
            $size = {size_mb}MB
            $file = "{img_path}"
            $fs = [System.IO.File]::Open($file, [System.IO.FileMode]::OpenOrCreate)
            $fs.SetLength($size)
            $fs.Close()
            '''
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, check=True)
            
            # Copy EFI file using mcopy (from mtools) or direct write
            if efi_file and os.path.exists(efi_file):
                # Try to use mcopy if available
                try:
                    subprocess.run(["mcopy", "-i", img_path, efi_file, "::/EFI/BOOT/BOOTX64.EFI"], 
                                  capture_output=True, check=True)
                except:
                    # Fallback: just copy the file to a known location
                    efi_dir = os.path.join(temp_dir, "efi_temp")
                    os.makedirs(efi_dir, exist_ok=True)
                    os.makedirs(os.path.join(efi_dir, "EFI", "BOOT"), exist_ok=True)
                    import shutil
                    shutil.copy2(efi_file, os.path.join(efi_dir, "EFI", "BOOT", "BOOTX64.EFI"))
                    # We'll mount this directory instead
                    return efi_dir, img_path
            
            return None, img_path
            
        except Exception as e:
            self.log(f"Error creating image: {e}")
            # Fallback: Use directory mode instead of disk image
            return self.create_efi_directory(efi_file), None
    
    def create_efi_directory(self, efi_file):
        """Create a directory with EFI file structure"""
        temp_dir = tempfile.mkdtemp(prefix="efivm_")
        efi_dir = os.path.join(temp_dir, "EFI", "BOOT")
        os.makedirs(efi_dir, exist_ok=True)
        
        if efi_file and os.path.exists(efi_file):
            import shutil
            shutil.copy2(efi_file, os.path.join(efi_dir, "BOOTX64.EFI"))
        
        return temp_dir
    
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
        if not efi_file or not os.path.exists(efi_file):
            messagebox.showerror("Error", "Please select an EFI file")
            return
        
        qemu_exe = self.qemu_path.get()
        if not os.path.exists(qemu_exe) and qemu_exe == "qemu-system-x86_64.exe":
            # Try to find it in PATH
            try:
                result = subprocess.run(["where", "qemu-system-x86_64"], 
                                       capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    qemu_exe = result.stdout.strip().split('\n')[0]
                else:
                    messagebox.showerror("Error", "QEMU not found. Please install QEMU for Windows.")
                    return
            except:
                messagebox.showerror("Error", "QEMU not found. Please install QEMU for Windows.")
                return
        
        self.log("Creating EFI environment...")
        
        # Create directory-based EFI (simpler for Windows)
        efi_dir = self.create_efi_directory(efi_file)
        
        # Build QEMU command
        cmd = [qemu_exe]
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
        
        # VM configuration - use directory instead of disk image for Windows
        cmd.extend([
            "-drive", f"file=fat:rw:{efi_dir},format=raw,media=disk",
            "-bios", r"C:\Program Files\qemu\edk2-x86_64-code.fd",  # Common OVMF path
            "-vga", "std",
            "-net", "none",
            "-monitor", "stdio"
        ])
        
        # Try to find OVMF BIOS
        bios_paths = [
            r"C:\Program Files\qemu\edk2-x86_64-code.fd",
            r"C:\Program Files (x86)\qemu\edk2-x86_64-code.fd",
            r"C:\qemu\edk2-x86_64-code.fd",
            "edk2-x86_64-code.fd"
        ]
        
        bios_found = False
        for bios in bios_paths:
            if os.path.exists(bios):
                # Replace BIOS in command
                for i, arg in enumerate(cmd):
                    if arg == "-bios":
                        cmd[i + 1] = bios
                        bios_found = True
                        break
                if bios_found:
                    break
        
        if not bios_found:
            self.log("Warning: OVMF BIOS not found. Trying default...")
        
        self.log(f"Starting VM with command: {' '.join(cmd)}")
        self.status_var.set("Starting VM...")
        self.start_btn.config(state="disabled")
        
        # Run in thread
        thread = threading.Thread(target=self.run_vm, args=(cmd, efi_dir))
        thread.daemon = True
        thread.start()
    
    def run_vm(self, cmd, temp_dir):
        try:
            self.vm_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                shell=True
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
            # Cleanup temp directory
            try:
                import shutil
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except:
                pass
            
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
