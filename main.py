import tkinter as tk
from tkinter import ttk
import webbrowser
import re

class CFOpenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CF Quick Open")
        self.root.geometry("420x220")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        # Style
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("TButton",
                  background=[("active", "#89b4fa"), ("!active", "#45475a")],
                  foreground=[("active", "#1e1e2e"), ("!active", "#cdd6f4")])

        style.configure("TEntry", fieldbackground="#2e2e44", foreground="#cdd6f4",
                        insertcolor="#f38ba8", font=("Consolas", 12))

        # Title
        ttk.Label(root, text="Codeforces Problem Opener", font=("Segoe UI", 14, "bold"),
                  foreground="#89b4fa").pack(pady=(20, 10))

        # Input field + label
        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=30, fill="x")

        ttk.Label(frame, text="CF").pack(side="left", padx=(0, 8))
        self.entry = ttk.Entry(frame, width=18, justify="center")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.focus_set()

        # Placeholder behavior
        self.placeholder = "  1985F  or  1913 A"
        self.entry.insert(0, self.placeholder)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)
        self.entry.bind("<Return>", lambda e: self.open_problem())

        # Open button
        ttk.Button(root, text="Open", command=self.open_problem,
                   style="TButton").pack(pady=15)

        # Status label
        self.status = ttk.Label(root, text="", foreground="#fab387")
        self.status.pack(pady=(0, 10))

        # Remember last opened
        self.last_url = None

    def clear_placeholder(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)

    def open_problem(self):
        s = self.entry.get().strip().upper()
        if not s or s == self.placeholder.strip().upper():
            self.status.config(text="Enter problem code", foreground="#f38ba8")
            return

        # Normalize input: CF1985F → 1985 F    CF 1913-A → 1913 A
        s = re.sub(r'[^0-9A-Z]', '', s)  # remove spaces, dashes, etc.
        m = re.match(r'^CF?([0-9]+)([A-Z][A-Z]?)$', s)

        if not m:
            self.status.config(text="Invalid format • try 1985F", foreground="#f38ba8")
            return

        contest, letter = m.groups()
        letter = letter.upper()

        urls = [
            f"https://codeforces.com/problemset/problem/{contest}/{letter}",
            f"https://codeforces.com/contest/{contest}/problem/{letter}",
            f"https://codeforces.com/gym/{contest}/problem/{letter}",
        ]

        opened = False
        for url in urls:
            if url == self.last_url:
                self.status.config(text="Already opened", foreground="#a6e3a1")
                return

            try:
                webbrowser.open_new_tab(url)
                self.last_url = url
                self.status.config(text=f"Opened {contest}/{letter}", foreground="#a6e3a1")
                opened = True
                break
            except:
                continue

        if not opened:
            self.status.config(text="Couldn't open link", foreground="#f38ba8")


if __name__ == "__main__":
    root = tk.Tk()
    app = CFOpenApp(root)
    root.mainloop()