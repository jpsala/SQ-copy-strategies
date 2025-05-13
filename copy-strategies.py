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
        self.geometry("800x600")
        self.minsize(600, 400)
        self.resizable(True, True)
        self.configure(bg="#f8f9fa")
        style = ttk.Style(self)
        style.configure("TLabelFrame", font=("Segoe UI", 11, "bold"), background="#f8f9fa")
        style.configure("TLabelFrame.Label", font=("Segoe UI", 11, "bold"), foreground="#3a3a3a")
        style.configure("TFrame", background="#f8f9fa")
        style.configure("TLabel", background="#f8f9fa")
        style.configure("FileLabel.TLabel", background="#e9ecef", relief="groove", borderwidth=1, font=("Segoe UI", 10), padding=(2, 1))
        style.map("FileLabel.TLabel", background=[("active", "#d0e7ff")])

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

        self.folder_file_lists = []  # Now will hold Frames, not Canvases
        self.folder_inner_frames = []  # Will be the same as folder_file_lists
        self.folder_scrollbars = []  # To hold scrollbars for each canvas
        self.create_widgets()
        self.load_settings()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding=4)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Folder selectors
        self.folder_rows = []
        self._trace_ids = []  # Store trace IDs for later removal
        self.folder_file_lists = []  # Now will hold Frames, not Canvases
        self.folder_inner_frames = []  # Will be the same as folder_file_lists
        folder_sections = [
            ("Real-Tick Folder", self.real_tick_var, self.real_tick_prefix, True),
            ("SPP Folder", self.spp_var, self.spp_prefix, True),
            ("Final Folder", self.final_var, None, False)
        ]
        for idx, (section_title, var, prefix_var, has_prefix) in enumerate(folder_sections):
            lf = ttk.LabelFrame(main_frame, text=section_title, padding=(4, 2, 4, 2))
            lf.grid(row=idx, column=0, sticky="nsew", pady=(0, 8))
            main_frame.rowconfigure(idx, weight=1)
            main_frame.columnconfigure(0, weight=1)
            lf.rowconfigure(1, weight=1)
            lf.columnconfigure(0, weight=1)
            row = ttk.Frame(lf)
            row.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            row.columnconfigure(1, weight=1)
            ttk.Label(row, text="Path:").grid(row=0, column=0, sticky="w", padx=(0, 4))
            entry = ttk.Entry(row, textvariable=var, width=48)
            entry.grid(row=0, column=1, sticky="ew", padx=(0, 4))
            browse_btn = ttk.Button(row, text="Browse", command=lambda v=var, i=idx: self.browse_folder(v, i))
            browse_btn.grid(row=0, column=2, padx=(0, 4))
            if has_prefix:
                ttk.Label(row, text="Prefix (optional):").grid(row=0, column=3, padx=(0, 4))
                prefix_entry = ttk.Entry(row, textvariable=prefix_var, width=14)
                prefix_entry.grid(row=0, column=4, padx=(0, 0))
                prefix_var.trace_add('write', lambda *args, i=idx: self.update_folder_file_list(i) or self.update_preview_async())
            trace_id = var.trace_add('write', lambda *args, i=idx: self.update_folder_file_list(i))
            self._trace_ids.append((var, trace_id))
            self.folder_rows.append(row)
            # File label area (Frame only)
            file_frame = ttk.Frame(lf, style="TFrame")
            file_frame.grid(row=1, column=0, sticky="nsew")
            lf.rowconfigure(1, weight=1)
            lf.columnconfigure(0, weight=1)
            file_frame.rowconfigure(0, weight=1)
            file_frame.columnconfigure(0, weight=1)
            file_inner = ttk.Frame(file_frame, style="TFrame")
            file_inner.grid(row=0, column=0, sticky="nsew")
            file_frame.bind("<Configure>", lambda e, idx=idx: self.update_folder_file_list(idx))
            self.folder_file_lists.append(file_inner)
            self.folder_inner_frames.append(file_inner)

        # Start button (centered)
        self.start_btn = ttk.Button(main_frame, text="Start", command=self.start_copy, state=tk.DISABLED)
        self.start_btn.grid(row=3, column=0, pady=(4, 4))

        # Preview section in its own LabelFrame
        preview_lf = ttk.LabelFrame(main_frame, text="Preview: Files to be Copied", padding=(4, 2, 4, 2))
        preview_lf.grid(row=4, column=0, sticky="nsew")
        main_frame.rowconfigure(4, weight=2)
        preview_lf.rowconfigure(0, weight=1)
        preview_lf.columnconfigure(0, weight=1)
        preview_frame = ttk.Frame(preview_lf, style="TFrame")
        preview_frame.grid(row=0, column=0, sticky="nsew")
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        self.preview_inner = ttk.Frame(preview_frame, style="TFrame")
        self.preview_inner.grid(row=0, column=0, sticky="nsew")
        preview_frame.bind("<Configure>", lambda e: self.update_preview())

    def browse_folder(self, var, idx):
        current = var.get()
        initialdir = current if os.path.isdir(current) else os.path.expanduser("~")
        folder = filedialog.askdirectory(initialdir=initialdir)
        if folder:
            var.set(folder)
            self.update_folder_file_list(idx)

    def update_folder_file_list(self, idx):
        folder = [self.real_tick_var.get(), self.spp_var.get(), self.final_var.get()][idx]
        inner = self.folder_inner_frames[idx]
        for widget in inner.winfo_children():
            widget.destroy()
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
                # --- Place file labels in a grid, wrapping as needed ---
                if not sqx_files:
                    return
                max_width = inner.winfo_width() or 600
                lbl_width = 120  # Use a fixed width for all labels
                cols = max(1, max_width // lbl_width)
                for i, f in enumerate(sqx_files):
                    lbl = ttk.Label(inner, text=f, style="FileLabel.TLabel")
                    row, col = divmod(i, cols)
                    lbl.grid(row=row, column=col, padx=2, pady=2, sticky="w")
                for c in range(cols):
                    inner.grid_columnconfigure(c, weight=1)
            except Exception as e:
                print(f"Exception in update_folder_file_list: {e}")

    def update_preview_async(self):
        threading.Thread(target=self.update_preview, daemon=True).start()

    def update_preview(self):
        for widget in self.preview_inner.winfo_children():
            widget.destroy()
        real_tick = self.real_tick_var.get()
        spp = self.spp_var.get()
        final = self.final_var.get()
        real_tick_prefix = self.real_tick_prefix.get().strip()
        spp_prefix = self.spp_prefix.get().strip()
        self.files_to_copy = []
        if os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final):
            try:
                spp_map = {}
                for f in os.listdir(spp):
                    if os.path.isfile(os.path.join(spp, f)) and f.lower().endswith('.sqx') and (not spp_prefix or f.lower().startswith(spp_prefix.lower())):
                        base = f[len(spp_prefix):] if spp_prefix and f.lower().startswith(spp_prefix.lower()) else f
                        spp_map[base] = f
                real_tick_map = {}
                for f in os.listdir(real_tick):
                    if os.path.isfile(os.path.join(real_tick, f)) and f.lower().endswith('.sqx') and (not real_tick_prefix or f.lower().startswith(real_tick_prefix.lower())):
                        base = f[len(real_tick_prefix):] if real_tick_prefix and f.lower().startswith(real_tick_prefix.lower()) else f
                        real_tick_map[base] = f
                common_bases = set(spp_map.keys()) & set(real_tick_map.keys())
                self.files_to_copy = sorted(common_bases)
                self.copy_pairs = [(real_tick_map[base], spp_map[base], base) for base in self.files_to_copy]
                if not self.files_to_copy:
                    return
                max_width = self.preview_inner.winfo_width() or 600
                lbl_width = 120  # Use a fixed width for all labels
                cols = max(1, max_width // lbl_width)
                for i, base in enumerate(self.files_to_copy):
                    lbl = ttk.Label(self.preview_inner, text=base, style="FileLabel.TLabel")
                    row, col = divmod(i, cols)
                    lbl.grid(row=row, column=col, padx=2, pady=2, sticky="w")
                for c in range(cols):
                    self.preview_inner.grid_columnconfigure(c, weight=1)
            except Exception as e:
                print(f"Exception in update_preview: {e}")
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