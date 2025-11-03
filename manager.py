# manager.py — CSV editor integrovatelný do notebooku (třída Manager)
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

class Manager:
    def __init__(self, parent):  # parent = frame v notebooku
        self.parent = parent
        self.filename = None
        self.data = []
        self.drag_index = None

        # === UI ===
        outer = tk.Frame(parent)
        outer.pack(fill="both", expand=True)

        # Listbox + scrollbar
        self.listbox = tk.Listbox(outer, activestyle="dotbox")
        self.listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar = tk.Scrollbar(outer, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Drag & drop události
        self.listbox.bind('<Button-1>', self.on_click)
        self.listbox.bind('<B1-Motion>', self.on_drag)
        self.listbox.bind('<ButtonRelease-1>', self.on_drop)
        self.listbox.bind('<Double-Button-1>', lambda e: self.edit_item())

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=6)

        tk.Button(btn_frame, text="Načíst CSV", command=self.load_csv).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Uložit CSV", command=self.save_csv).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Přidat položku", command=self.add_item).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Upravit položku", command=self.edit_item).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Smazat položku", command=self.delete_item).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Nahoru", command=self.move_up).grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Dolů", command=self.move_down).grid(row=0, column=6, padx=5)

    # === CSV operace ===
    def load_csv(self):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        self.filename = file
        self.data.clear()
        self.listbox.delete(0, tk.END)
        with open(file, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    self.data.append(row[0])
                    self.listbox.insert(tk.END, row[0])

    def save_csv(self):
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not self.filename:
            return
        with open(self.filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            for item in self.data:
                writer.writerow([item])
        messagebox.showinfo("Uloženo", f"Soubor byl uložen: {os.path.basename(self.filename)}")

    # === CRUD ===
    def add_item(self):
        new_item = self.simple_input("Nová položka")
        if new_item:
            self.data.append(new_item)
            self.listbox.insert(tk.END, new_item)

    def edit_item(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Varování", "Vyberte položku k úpravě")
            return
        index = selection[0]
        new_value = self.simple_input("Upravit položku", self.data[index])
        if new_value:
            self.data[index] = new_value
            self.listbox.delete(index)
            self.listbox.insert(index, new_value)
            self.listbox.selection_set(index)

    def delete_item(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Varování", "Vyberte položku ke smazání")
            return
        index = selection[0]
        del self.data[index]
        self.listbox.delete(index)

    # === Posouvání pořadí ===
    def move_up(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i == 0:
            return
        self.data[i-1], self.data[i] = self.data[i], self.data[i-1]
        self.refresh_listbox()
        self.listbox.selection_set(i-1)
        self.listbox.activate(i-1)
        self.listbox.see(i-1)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        i = sel[0]
        if i == len(self.data) - 1:
            return
        self.data[i+1], self.data[i] = self.data[i], self.data[i+1]
        self.refresh_listbox()
        self.listbox.selection_set(i+1)
        self.listbox.activate(i+1)
        self.listbox.see(i+1)

    # === Drag & drop ===
    def on_click(self, event):
        idx = self.listbox.nearest(event.y)
        if 0 <= idx < len(self.data):
            self.drag_index = idx
            # vizuálně zvýraznit aktuální řádek
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)

    def on_drag(self, event):
        # zvýrazňování potenciální pozice při přetahování
        if self.drag_index is None:
            return
        idx = self.listbox.nearest(event.y)
        if 0 <= idx < self.listbox.size():
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.listbox.activate(idx)
            self.listbox.see(idx)

    def on_drop(self, event):
        if self.drag_index is None:
            return
        target = self.listbox.nearest(event.y)
        if target < 0:
            target = 0
        if target >= len(self.data):
            target = len(self.data) - 1
        start = self.drag_index
        if target == start:
            self.drag_index = None
            return
        item = self.data.pop(start)
        # pokud táhnu směrem dolů, po pop se indexy posunou o -1
        if target > start:
            target -= 1
        self.data.insert(target, item)
        self.refresh_listbox()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(target)
        self.listbox.activate(target)
        self.listbox.see(target)
        self.drag_index = None

    # === Pomocné ===
    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.data:
            self.listbox.insert(tk.END, item)

    def simple_input(self, title, default=""):
        popup = tk.Toplevel(self.parent)
        popup.title(title)
        popup.transient(self.parent.winfo_toplevel())
        popup.grab_set()
        tk.Label(popup, text=title).pack(pady=5, padx=10)
        entry = tk.Entry(popup)
        entry.insert(0, default)
        entry.pack(padx=10, pady=5)

        value = {"text": None}
        def confirm():
            value["text"] = entry.get().strip()
            popup.destroy()
        tk.Button(popup, text="OK", command=confirm).pack(pady=8)

        # vycentrovat okno
        popup.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - popup.winfo_width()) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - popup.winfo_height()) // 2
        popup.geometry(f"+{x}+{y}")

        self.parent.wait_window(popup)
        return value["text"]

if __name__ == "__main__":
    # Demo režim pro samostatné spuštění
    root = tk.Tk()
    root.title("Manager – demo")
    frm = tk.Frame(root)
    frm.pack(fill="both", expand=True)
    Manager(frm)
    root.mainloop()


# =====================
# main_app.py — ukázka integrace do notebooku
# (v produkci mějte v samostatném souboru, zde jen pro přehled)
"""
import tkinter as tk
from tkinter import ttk

from spojova import Aplikace as SpojovaApp
from technicka import Aplikace as TechnickaApp
from strojni import Aplikace as StrojniApp
from manager import Manager

root = tk.Tk()
root.title("Hlášení závad")

try:
    root.state('zoomed')
except Exception:
    root.attributes('-zoomed', True)

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

frame_spojova = tk.Frame(notebook)
frame_technicka = tk.Frame(notebook)
frame_strojni = tk.Frame(notebook)
frame_manager = tk.Frame(notebook)

notebook.add(frame_spojova, text="Spojová služba")
notebook.add(frame_technicka, text="Technická služba")
notebook.add(frame_strojni, text="Strojní služba")
notebook.add(frame_manager, text="Manager")

app_spojova = SpojovaApp(frame_spojova)
app_technicka = TechnickaApp(frame_technicka)
app_strojni = StrojniApp(frame_strojni)
app_manager = Manager(frame_manager)

root.mainloop()
"""

