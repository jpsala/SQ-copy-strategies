import os
import shutil
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

SETTINGS_FILE = "settings.json"

class CopyStrategiesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Copy Strategies")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg="#f4f4f4")

        # Set custom icon
        try:
            self.iconbitmap('trading.ico')
        except Exception:
            pass  # Fallback to default icon if not found

        # Folder paths
        self.real_tick_var = tk.StringVar()
        self.spp_var = tk.StringVar()
        self.final_var = tk.StringVar()

        self.create_widgets()
        self.load_settings()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Folder selectors
        self.folder_rows = []
        self._trace_ids = []  # Store trace IDs for later removal
        for idx, (label, var) in enumerate([
            ("Real-Tick Folder:", self.real_tick_var),
            ("SPP Folder:", self.spp_var),
            ("Final Folder:", self.final_var)
        ]):
            row = ttk.Frame(main_frame)
            row.pack(fill=tk.X, pady=5)
            ttk.Label(row, text=label, width=16).pack(side=tk.LEFT)
            entry = ttk.Entry(row, textvariable=var, width=50)
            entry.pack(side=tk.LEFT, padx=5)
            browse_btn = ttk.Button(row, text="Browse", command=lambda v=var: self.browse_folder(v))
            browse_btn.pack(side=tk.LEFT)
            trace_id = var.trace_add('write', lambda *args: self.update_preview_async())
            self._trace_ids.append((var, trace_id))
            self.folder_rows.append(row)

        # Start button (above preview area)
        self.start_btn = ttk.Button(main_frame, text="Start", command=self.start_copy, state=tk.DISABLED)
        self.start_btn.pack(pady=(10, 10))

        # Preview label
        ttk.Label(main_frame, text="Preview: Files to be Copied", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(0, 5))

        # Preview area (Treeview, no header)
        columns = ("filename",)
        self.preview_tree = ttk.Treeview(main_frame, columns=columns, show="tree", height=15)
        self.preview_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        style = ttk.Style()
        style.configure("NoBorder.Treeview", borderwidth=0, relief="flat")
        self.preview_tree.configure(style="NoBorder.Treeview")

    def browse_folder(self, var):
        # Open dialog at current path if valid, else default
        current = var.get()
        initialdir = current if os.path.isdir(current) else os.path.expanduser("~")
        folder = filedialog.askdirectory(initialdir=initialdir)
        if folder:
            var.set(folder)

    def update_preview_async(self):
        threading.Thread(target=self.update_preview, daemon=True).start()

    def update_preview(self):
        # Only show files that are present as regular files in BOTH spp and real-tick
        self.preview_tree.delete(*self.preview_tree.get_children())
        real_tick = self.real_tick_var.get()
        spp = self.spp_var.get()
        final = self.final_var.get()
        self.files_to_copy = []
        if os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final):
            try:
                spp_files = set(f for f in os.listdir(spp) if os.path.isfile(os.path.join(spp, f)))
                real_tick_files = set(f for f in os.listdir(real_tick) if os.path.isfile(os.path.join(real_tick, f)))
                # Only show files that are in BOTH spp and real-tick
                self.files_to_copy = sorted(spp_files & real_tick_files)
                for fname in self.files_to_copy:
                    self.preview_tree.insert("", tk.END, text=fname)
            except Exception as e:
                print(f"Exception in update_preview: {e}")
        # Enable Start button only if there are files to copy and all folders are set
        if self.files_to_copy and os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final):
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.start_btn.config(state=tk.DISABLED)

    def start_copy(self):
        # Only copy files present as files in BOTH spp and real-tick, from real-tick to final
        real_tick = self.real_tick_var.get()
        final = self.final_var.get()
        errors = []
        copied = 0
        for fname in self.files_to_copy:
            src = os.path.join(real_tick, fname)
            dst = os.path.join(final, fname)
            try:
                shutil.copy2(src, dst)
                copied += 1
            except Exception as e:
                errors.append(f"{fname}: {e}")
        if errors:
            messagebox.showerror("Copy Error", f"Some files could not be copied:\n" + "\n".join(errors))
        else:
            messagebox.showinfo("Copy Complete", f"Successfully copied {copied} files to '{final}'.")
        self.update_preview_async()

    def load_settings(self):
        # Load last used folder paths from settings.json
        if os.path.exists(SETTINGS_FILE):
            try:
                # Remove trace callbacks to avoid multiple updates
                for var, trace_id in getattr(self, '_trace_ids', []):
                    try:
                        var.trace_remove('write', trace_id)
                    except Exception:
                        pass
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.real_tick_var.set(data.get('real_tick', ''))
                self.spp_var.set(data.get('spp', ''))
                self.final_var.set(data.get('final', ''))
                # Re-add trace callbacks
                self._trace_ids = []
                for var in [self.real_tick_var, self.spp_var, self.final_var]:
                    trace_id = var.trace_add('write', lambda *args: self.update_preview_async())
                    self._trace_ids.append((var, trace_id))
            except Exception:
                pass
        # Always refresh preview after restoring paths
        self.update_preview_async()

    def save_settings(self):
        # Save current folder paths to settings.json
        data = {
            'real_tick': self.real_tick_var.get(),
            'spp': self.spp_var.get(),
            'final': self.final_var.get()
        }
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def on_close(self):
        self.save_settings()
        self.destroy()

if __name__ == "__main__":
    app = CopyStrategiesApp()
    app.mainloop() 