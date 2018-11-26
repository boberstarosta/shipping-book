import tkinter as tk
from tkinter import messagebox

from app.pdf import write_and_open_addresses_pdf


class TextDialog(tk.Toplevel):
    def __init__(self, parent, title="Text dialog", width=80, height=10):
        super().__init__(parent)

        self.result = None

        self.resizable(False, False)
        self.transient(parent)
        self.title(title)

        self.add_widgets(width, height)

        self.grab_set()
        self.wait_window(self)

    def add_widgets(self, width, height):
        outer_frame = tk.Frame(self)
        outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)

        self.textbox = tk.Text(outer_frame, width=width, height=height)
        self.textbox.grid(column=0, row=0, sticky=tk.NSEW)

        vscrollbar = tk.Scrollbar(outer_frame, orient=tk.VERTICAL)
        vscrollbar.grid(column=1, row=0, sticky=tk.NS)

        hscrollbar = tk.Scrollbar(outer_frame, orient=tk.HORIZONTAL)
        hscrollbar.grid(column=0, row=1, sticky=tk.EW)

        vscrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vscrollbar.set)
        hscrollbar.config(command=self.textbox.xview)
        self.textbox.config(xscrollcommand=hscrollbar.set)

        self.textbox.bind("<KP_Enter>",
                          lambda _: self.textbox.insert(tk.INSERT, "\n"))
        self.textbox.bind("<Escape>", lambda _: self.cancel())
        self.textbox.focus_set()

        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        btn_cancel = tk.Button(btn_frame, text="Anuluj", command=self.cancel)
        btn_cancel.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        btn_ok = tk.Button(btn_frame, text="Dodaj", command=self.ok)
        btn_ok.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def validate(self):
        return len(self.textbox.get("1.0", "end").strip()) > 0

    def cancel(self):
        self.result = "cancel"
        self.destroy()

    def ok(self):
        if self.validate():
            self.result = "ok"
            self.text = self.textbox.get("1.0", "end").strip()
            self.destroy()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Książka Nadawcza")
        self.geometry("600x600+600+200")
        self.minsize(600, 600)

        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.TOP, fill=tk.X)

        btn = tk.Button(btn_frame, text="Dodaj adres",
                        command=self.add)
        btn.pack(fill=tk.X)

        btn = tk.Button(btn_frame, text="Wyczyść listę adresów",
                        command=self.clear_addresses)
        btn.pack(fill=tk.X)

        btn = tk.Button(btn_frame, text="Otwórz PDF",
                        command=self.create_pdf)
        btn.pack(fill=tk.X)

        self.addresses = []

        outer_frame = tk.Frame(self)
        outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)

        vscrollbar = tk.Scrollbar(outer_frame, orient=tk.VERTICAL)
        vscrollbar.grid(column=1, row=0, sticky=tk.NS)

        self.listbox = tk.Listbox(outer_frame)
        self.listbox.grid(column=0, row=0, sticky=tk.NSEW)

        vscrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=vscrollbar.set)

    def add(self):
        dialog = TextDialog(self, title="Dodaj adres")
        if dialog.result == "ok":
            self.addresses.append(dialog.text)
            text_row = dialog.text.replace("\n", "  ")
            self.listbox.insert(tk.END, text_row)

    def clear(self):
        self.addresses.clear()
        self.listbox.delete(0, tk.END)

    def create_pdf(self):
        if self.addresses:
            write_and_open_addresses_pdf(self.addresses)

    def clear_addresses(self):
        if self.addresses and messagebox.askyesno(
            title="Wyszyścić adresy?",
            message="Na pewno skasować wszystkie adresy z listy?"
        ):
            self.clear()
