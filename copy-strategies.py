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

        # Prefix variables for Real-Tick and SPP
        self.real_tick_prefix = tk.StringVar()
        self.spp_prefix = tk.StringVar()

        self.folder_file_lists = []  # To hold Listbox widgets for .sqx file display
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
            entry = ttk.Entry(row, textvariable=var, width=40)
            entry.pack(side=tk.LEFT, padx=5)
            browse_btn = ttk.Button(row, text="Browse", command=lambda v=var, i=idx: self.browse_folder(v, i))
            browse_btn.pack(side=tk.LEFT)
            # Add prefix entry for Real-Tick and SPP only
            if idx == 0:
                ttk.Label(row, text="Prefix (optional):").pack(side=tk.LEFT, padx=(10, 0))
                prefix_entry = ttk.Entry(row, textvariable=self.real_tick_prefix, width=12)
                prefix_entry.pack(side=tk.LEFT)
                self.real_tick_prefix.trace_add('write', lambda *args: self.update_folder_file_list(0) or self.update_preview_async())
            elif idx == 1:
                ttk.Label(row, text="Prefix (optional):").pack(side=tk.LEFT, padx=(10, 0))
                prefix_entry = ttk.Entry(row, textvariable=self.spp_prefix, width=12)
                prefix_entry.pack(side=tk.LEFT)
                self.spp_prefix.trace_add('write', lambda *args: self.update_folder_file_list(1) or self.update_preview_async())
            trace_id = var.trace_add('write', lambda *args, i=idx: self.update_folder_file_list(i))
            self._trace_ids.append((var, trace_id))
            self.folder_rows.append(row)
            # Add Listbox for .sqx files
            file_listbox = tk.Listbox(main_frame, height=3, width=80, exportselection=False)
            file_listbox.pack(padx=20, pady=(0, 5))
            self.folder_file_lists.append(file_listbox)

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

    def browse_folder(self, var, idx):
        current = var.get()
        initialdir = current if os.path.isdir(current) else os.path.expanduser("~")
        folder = filedialog.askdirectory(initialdir=initialdir)
        if folder:
            var.set(folder)
            self.update_folder_file_list(idx)

    def update_folder_file_list(self, idx):
        folder = [self.real_tick_var.get(), self.spp_var.get(), self.final_var.get()][idx]
        listbox = self.folder_file_lists[idx]
        listbox.delete(0, tk.END)
        prefix = ''
        if idx == 0:
            prefix = self.real_tick_prefix.get().strip()
        elif idx == 1:
            prefix = self.spp_prefix.get().strip()
        if os.path.isdir(folder):
            try:
                sqx_files = sorted(f for f in os.listdir(folder)
                                  if os.path.isfile(os.path.join(folder, f))
                                  and f.lower().endswith('.sqx')
                                  and (not prefix or f.lower().startswith(prefix.lower())))
                print(f"DEBUG: Checking folder: {folder}")
                print(f"DEBUG: .sqx files found: {sqx_files}")
                for f in sqx_files:
                    listbox.insert(tk.END, f)
            except Exception as e:
                print(f"Exception in update_folder_file_list: {e}")

    def update_preview_async(self):
        threading.Thread(target=self.update_preview, daemon=True).start()

    def update_preview(self):
        # Only show .sqx files that are present as regular files in BOTH spp and real-tick, matching by base name after prefix
        self.preview_tree.delete(*self.preview_tree.get_children())
        real_tick = self.real_tick_var.get()
        spp = self.spp_var.get()
        final = self.final_var.get()
        real_tick_prefix = self.real_tick_prefix.get().strip()
        spp_prefix = self.spp_prefix.get().strip()
        self.files_to_copy = []
        if os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final):
            try:
                # Build base name to full name mapping for SPP
                spp_map = {}
                for f in os.listdir(spp):
                    if os.path.isfile(os.path.join(spp, f)) and f.lower().endswith('.sqx') and (not spp_prefix or f.lower().startswith(spp_prefix.lower())):
                        base = f[len(spp_prefix):] if spp_prefix and f.lower().startswith(spp_prefix.lower()) else f
                        spp_map[base] = f
                # Build base name to full name mapping for Real-Tick
                real_tick_map = {}
                for f in os.listdir(real_tick):
                    if os.path.isfile(os.path.join(real_tick, f)) and f.lower().endswith('.sqx') and (not real_tick_prefix or f.lower().startswith(real_tick_prefix.lower())):
                        base = f[len(real_tick_prefix):] if real_tick_prefix and f.lower().startswith(real_tick_prefix.lower()) else f
                        real_tick_map[base] = f
                # Find base names present in both
                common_bases = set(spp_map.keys()) & set(real_tick_map.keys())
                self.files_to_copy = sorted(common_bases)
                self.copy_pairs = [(real_tick_map[base], spp_map[base], base) for base in self.files_to_copy]
                for base in self.files_to_copy:
                    # Show the base name (filename without prefix)
                    self.preview_tree.insert("", tk.END, text=base)
            except Exception as e:
                print(f"Exception in update_preview: {e}")
        # Enable Start button only if there are files to copy and all folders are set
        if self.files_to_copy and os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final):
            self.start_btn.config(state=tk.NORMAL)
        else:
            self.start_btn.config(state=tk.DISABLED)

    def start_copy(self):
        # Only copy files present as files in BOTH spp and real-tick, from real-tick to final, matching by base name
        real_tick = self.real_tick_var.get()
        final = self.final_var.get()
        errors = []
        copied = 0
        for real_tick_fname, spp_fname, base in getattr(self, 'copy_pairs', []):
            src = os.path.join(real_tick, real_tick_fname)
            dst = os.path.join(final, real_tick_fname)
            try:
                shutil.copy2(src, dst)
                copied += 1
            except Exception as e:
                errors.append(f"{real_tick_fname}: {e}")
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
        # Also update .sqx file lists for all folders
        for idx in range(3):
            self.update_folder_file_list(idx)

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