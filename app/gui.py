import tkinter as tk


WHITE = "#fff"
BLUE = "#4286f4"
GREEN = "#4ca522"
RED = "#e22222"
PADDING = 10
FONT = ("TkDefaultFont", 14, "bold")
FONT_MONO = ("TkFixedFont", 14, "bold")



class TextDialog(tk.Toplevel):
    def __init__(self, parent, title="Text dialog"):
        super().__init__(parent)

        self.result = None

        self.transient(parent)
        self.title(title)

        self.add_widgets()

        self.grab_set()
        self.wait_window(self)

    def add_widgets(self):
        outer_frame = tk.Frame(self)
        outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        outer_frame.grid_columnconfigure(0, weight=1)
        outer_frame.grid_rowconfigure(0, weight=1)

        self.textbox = tk.Text(outer_frame, width=80, height=6)
        self.textbox.grid(column=0, row=0, sticky=tk.NSEW)

        vscrollbar = tk.Scrollbar(outer_frame, orient=tk.VERTICAL)
        vscrollbar.grid(column=1, row=0, sticky=tk.NS)

        hscrollbar = tk.Scrollbar(outer_frame, orient=tk.HORIZONTAL)
        hscrollbar.grid(column=0, row=1, sticky=tk.EW)

        vscrollbar.config(command=self.textbox.yview)
        self.textbox.config(yscrollcommand=vscrollbar.set)
        hscrollbar.config(command=self.textbox.xview)
        self.textbox.config(xscrollcommand=hscrollbar.set)
        
        self.textbox.bind("<KP_Enter>", lambda _: self.textbox.insert(tk.INSERT, "\n"))
        self.textbox.focus_set()
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        
        btn_ok = tk.Button(btn_frame, text="OK", command=self.ok)
        btn_ok.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        btn_cancel = tk.Button(btn_frame, text="Cancel", command=self.cancel)
        btn_cancel.pack(side=tk.RIGHT, fill=tk.X, expand=True)

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


class AddressList(tk.Frame):
    def __init__(self, parent, addresses=None):
        super().__init__(parent)

        if addresses is None:
            addresses = []

        self.addresses = addresses

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
        
        for address in self.addresses:
            self.add(address)

    def add(self, address):
        self.addresses.append(address)
        text_row = address.replace("\n", "  ")
        self.listbox.insert(tk.END, text_row)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(800, 800)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(side=tk.TOP, fill=tk.X)

        btn = tk.Button(btn_frame, text="Add address", command = self.add_address)
        btn.pack(fill=tk.BOTH)
        
        self.address_list = AddressList(self)
        self.address_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def add_address(self):
        dialog = TextDialog(self)
        if dialog.result == "ok":
            self.address_list.add(dialog.text)

