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

        btn = tk.Button(btn_frame, text="Dodaj",
                        command=self.add)
        btn.pack(side=tk.TOP, fill=tk.X)

        frame = tk.Frame(btn_frame)
        frame.pack(side=tk.TOP, fill=tk.X)

        self.btn_delete = tk.Button(frame, text="Usuń", state=tk.DISABLED,
                                    command=self.delete)
        self.btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_up = tk.Button(frame, text="W górę", state=tk.DISABLED,
                                command=self.move_up)
        self.btn_up.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_down = tk.Button(frame, text="W dół", state=tk.DISABLED,
                                  command=self.move_down)
        self.btn_down.pack(side=tk.LEFT, fill=tk.X, expand=True)

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
        self.listbox.bind("<<ListboxSelect>>", self.on_selection_changed)

        self.selected_index = None

    def add(self):
        dialog = TextDialog(self, title="Dodaj adres")
        if dialog.result == "ok":
            self.addresses.append(dialog.text)
            text_row = dialog.text.replace("\n", "  ")
            self.listbox.insert(tk.END, text_row)

    def delete(self):
        self.listbox.delete(self.selected_index)
        del self.addresses[self.selected_index]
        self.selected_index = None
        self.listbox.select_clear(0, tk.END)
        self.btn_delete.config(state=tk.DISABLED)
        self.btn_up.config(state=tk.DISABLED)
        self.btn_down.config(state=tk.DISABLED)

    def move_up(self):
        if self.selected_index:
            i, j = self.selected_index, self.selected_index - 1
            self.addresses[i], self.addresses[j] = \
                self.addresses[j], self.addresses[i]
            text = self.listbox.get(self.selected_index)
            self.listbox.delete(self.selected_index)
            self.listbox.insert(self.selected_index - 1, text)
            self.listbox.select_set(self.selected_index - 1)
            self.listbox.activate(self.selected_index - 1)
            self.on_selection_changed(None)

    def move_down(self):
        if (
            self.selected_index is not None
            and self.selected_index < len(self.addresses) - 1
        ):
            i, j = self.selected_index, self.selected_index + 1
            self.addresses[i], self.addresses[j] = \
                self.addresses[j], self.addresses[i]
            text = self.listbox.get(self.selected_index)
            self.listbox.delete(self.selected_index)
            self.listbox.insert(self.selected_index + 1, text)
            self.listbox.select_set(self.selected_index + 1)
            self.listbox.activate(self.selected_index + 1)
            self.on_selection_changed(None)

    def clear(self):
        self.addresses.clear()
        self.listbox.delete(0, tk.END)
        self.btn_delete.config(state=tk.DISABLED)
        self.btn_up.config(state=tk.DISABLED)
        self.btn_down.config(state=tk.DISABLED)

    def create_pdf(self):
        if self.addresses:
            write_and_open_addresses_pdf(self.addresses)

    def clear_addresses(self):
        if self.addresses and messagebox.askyesno(
            title="Wyszyścić adresy?",
            message="Na pewno skasować wszystkie adresy z listy?"
        ):
            self.clear()

    def on_selection_changed(self, event):
        if self.addresses:
            self.selected_index = int(self.listbox.curselection()[0])
            self.btn_delete.config(state=tk.NORMAL)
            if self.selected_index is not None and self.selected_index > 0:
                self.btn_up.config(state=tk.NORMAL)
            else:
                self.btn_up.config(state=tk.DISABLED)
            if (
                self.selected_index is not None
                and self.selected_index < len(self.addresses) - 1
            ):
                self.btn_down.config(state=tk.NORMAL)
            else:
                self.btn_down.config(state=tk.DISABLED)
