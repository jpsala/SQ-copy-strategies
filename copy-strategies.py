import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, Menu

OPTIONS_FILE = "options.json"

class CopyStrategiesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Copy Strategies")
        self.geometry("500x250")
        self.resizable(False, False)

        # Folder paths
        self.real_tick_var = tk.StringVar()
        self.spp_var = tk.StringVar()
        self.final_var = tk.StringVar()

        self.create_menu()
        self.create_widgets()
        self.load_options()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_menu(self):
        menubar = Menu(self)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions", command=self.show_instructions)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

    def show_instructions(self):
        messagebox.showinfo(
            "Copy Strategies - Instructions",
            "1. Select the Real-tick, SPP, and Final folders.\n"
            "2. Click 'Start Copy' to copy files from Real-tick to Final, only if they also exist in SPP.\n"
            "3. Your folder selections will be saved for next time.\n"
            "4. The app runs standalone as a single .exe."
        )

    def create_widgets(self):
        pad = {'padx': 10, 'pady': 10}

        # Real-tick folder
        tk.Label(self, text="Real-tick folder:").grid(row=0, column=0, sticky="e", **pad)
        tk.Entry(self, textvariable=self.real_tick_var, width=40).grid(row=0, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_real_tick).grid(row=0, column=2, **pad)

        # SPP folder
        tk.Label(self, text="SPP folder:").grid(row=1, column=0, sticky="e", **pad)
        tk.Entry(self, textvariable=self.spp_var, width=40).grid(row=1, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_spp).grid(row=1, column=2, **pad)

        # Final folder
        tk.Label(self, text="Final folder:").grid(row=2, column=0, sticky="e", **pad)
        tk.Entry(self, textvariable=self.final_var, width=40).grid(row=2, column=1, **pad)
        tk.Button(self, text="Browse", command=self.browse_final).grid(row=2, column=2, **pad)

        # Start Copy button
        tk.Button(self, text="Start Copy", command=self.start_copy, width=20, bg="#4caf50", fg="white").grid(row=4, column=0, columnspan=3, pady=20)

    def browse_real_tick(self):
        folder = filedialog.askdirectory(title="Select Real-tick Folder")
        if folder:
            self.real_tick_var.set(folder)

    def browse_spp(self):
        folder = filedialog.askdirectory(title="Select SPP Folder")
        if folder:
            self.spp_var.set(folder)

    def browse_final(self):
        folder = filedialog.askdirectory(title="Select Final Folder")
        if folder:
            self.final_var.set(folder)

    def start_copy(self):
        real_tick = self.real_tick_var.get()
        spp = self.spp_var.get()
        final = self.final_var.get()

        if not all([real_tick, spp, final]):
            messagebox.showerror("Error", "Please select all three folders.")
            return
        if not (os.path.isdir(real_tick) and os.path.isdir(spp) and os.path.isdir(final)):
            messagebox.showerror("Error", "One or more selected folders do not exist.")
            return
        try:
            spp_files = set(f for f in os.listdir(spp) if os.path.isfile(os.path.join(spp, f)))
            real_tick_files = set(f for f in os.listdir(real_tick) if os.path.isfile(os.path.join(real_tick, f)))
            to_copy = spp_files & real_tick_files
            if not to_copy:
                messagebox.showinfo("Info", "No matching files to copy.")
                return
            copied = 0
            for fname in to_copy:
                src = os.path.join(real_tick, fname)
                dst = os.path.join(final, fname)
                try:
                    shutil.copy2(src, dst)
                    copied += 1
                except Exception as e:
                    messagebox.showwarning("Warning", f"Failed to copy {fname}: {e}")
            messagebox.showinfo("Done", f"Copied {copied} file(s) to Final folder.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def load_options(self):
        if os.path.exists(OPTIONS_FILE):
            try:
                with open(OPTIONS_FILE, "r") as f:
                    data = json.load(f)
                self.real_tick_var.set(data.get("real_tick", ""))
                self.spp_var.set(data.get("spp", ""))
                self.final_var.set(data.get("final", ""))
            except Exception:
                pass

    def save_options(self):
        data = {
            "real_tick": self.real_tick_var.get(),
            "spp": self.spp_var.get(),
            "final": self.final_var.get(),
        }
        try:
            with open(OPTIONS_FILE, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def on_close(self):
        self.save_options()
        self.destroy()

if __name__ == "__main__":
    app = CopyStrategiesApp()
    app.mainloop() 