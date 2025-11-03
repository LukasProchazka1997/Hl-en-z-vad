import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

SERVICE_FILES = {
    "Spojová služba": "spojova.csv",
    "Technická služba": "technicka.csv",
    "Strojní služba": "strojni.csv"
}

HESLO = "1234"

class Manager:
    def __init__(self, parent):
        self.parent = parent
        self.data = []
        self.drag_index = None
        self.current_file = None

        # --- UI ---
        top_frame = tk.Frame(parent)
        top_frame.pack(fill="x", pady=5)

        tk.Label(top_frame, text="Vyber službu:").pack(side="left", padx=5)
        self.service_var = tk.StringVar(value="Spojová služba")
        self.service_menu = tk.OptionMenu(top_frame, self.service_var, *SERVICE_FILES.keys(), command=self.load_service)
        self.service_menu.pack(side="left")

        # Listbox + scrollbar
        outer = tk.Frame(parent)
        outer.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(outer, activestyle="dotbox")
        self.listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar = tk.Scrollbar(outer, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=10)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind('<Button-1>', self.on_click)
        self.listbox.bind('<B1-Motion>', self.on_drag)
        self.listbox.bind('<ButtonRelease-1>', self.on_drop)
        self.listbox.bind('<Double-Button-1>', lambda e: self.edit_item())

        # tlačítka
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Přidat", command=self.add_item).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Upravit", command=self.edit_item).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Smazat", command=self.delete_item).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Nahoru", command=self.move_up).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Dolů", command=self.move_down).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Uložit (heslo)", command=self.save_csv).grid(row=0, column=5, padx=5)

        # načtení defaultní služby
        self.load_service(self.service_var.get())

    # --- načítání služby ---
    def load_service(self, service_name):
        self.current_file = SERVICE_FILES[service_name]
        self.data.clear()
        self.listbox.delete(0, tk.END)
        if os.path.exists(self.current_file):
            with open(self.current_file, newline='', encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        self.data.append(row[0])
                        self.listbox.insert(tk.END, row[0])

    # --- CRUD operace ---
    def add_item(self):
        val = simpledialog.askstring("Nová položka", "Zadej novou položku", parent=self.parent)
        if val:
            self.data.append(val)
            self.listbox.insert(tk.END, val)

    def edit_item(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Varování", "Vyber položku k úpravě")
            return
        i = sel[0]
        val = simpledialog.askstring("Upravit položku", "Nová hodnota", initialvalue=self.data[i], parent=self.parent)
        if val:
            self.data[i] = val
            self.listbox.delete(i)
            self.listbox.insert(i, val)

    def delete_item(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Varování", "Vyber položku ke smazání")
            return
        i = sel[0]
        del self.data[i]
        self.listbox.delete(i)

    # --- přesouvání ---
    def move_up(self):
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        if i == 0: return
        self.data[i-1], self.data[i] = self.data[i], self.data[i-1]
        self.refresh_listbox()
        self.listbox.selection_set(i-1)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        if i == len(self.data)-1: return
        self.data[i+1], self.data[i] = self.data[i], self.data[i+1]
        self.refresh_listbox()
        self.listbox.selection_set(i+1)

    # --- drag & drop ---
    def on_click(self, event):
        idx = self.listbox.nearest(event.y)
        if 0 <= idx < len(self.data):
            self.drag_index = idx
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)

    def on_drag(self, event):
        if self.drag_index is None: return
        idx = self.listbox.nearest(event.y)
        if 0 <= idx < len(self.data):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)

    def on_drop(self, event):
        if self.drag_index is None: return
        target = self.listbox.nearest(event.y)
        if target < 0: target = 0
        if target >= len(self.data): target = len(self.data)-1
        start = self.drag_index
        if target == start: 
            self.drag_index = None
            return
        item = self.data.pop(start)
        if target > start: target -= 1
        self.data.insert(target, item)
        self.refresh_listbox()
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(target)
        self.drag_index = None

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i in self.data:
            self.listbox.insert(tk.END, i)

    # --- uložení s heslem ---
    def save_csv(self):
        pwd = simpledialog.askstring("Heslo", "Zadej heslo pro uložení", show="*", parent=self.parent)
        if pwd != HESLO:
            messagebox.showerror("Chyba", "Špatné heslo!")
            return
        if not self.current_file:
            messagebox.showerror("Chyba", "Žádný soubor není vybraný")
            return
        with open(self.current_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for item in self.data:
                writer.writerow([item])
        messagebox.showinfo("Uloženo", f"Soubor {self.current_file} byl uložen")

# --- demo ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Manager – demo")
    Manager(root)
    root.mainloop()
