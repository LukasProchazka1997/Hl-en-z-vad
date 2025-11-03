import tkinter as tk
from tkinter import ttk

from spojova import Aplikace as SpojovaApp
from technicka import Aplikace as TechnickaApp
from strojni import Aplikace as StrojniApp
from manager import Manager  # import třídy Manager

root = tk.Tk()
root.title("Hlášení závad")

# maximalizace okna
try:
    root.state('zoomed')        # Windows
except:
    root.attributes('-zoomed', True)  # Linux/Mac

# notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# panely
frame_spojova = tk.Frame(notebook)
frame_technicka = tk.Frame(notebook)
frame_strojni = tk.Frame(notebook)
frame_manager = tk.Frame(notebook)  # nový frame pro manager

# přidání záložek
notebook.add(frame_spojova, text="Spojová služba")
notebook.add(frame_technicka, text="Technická služba")
notebook.add(frame_strojni, text="Strojní služba")
notebook.add(frame_manager, text="Manager")  # nová záložka

# vložení aplikací do jednotlivých záložek
app_spojova = SpojovaApp(frame_spojova)
app_technicka = TechnickaApp(frame_technicka)
app_strojni = StrojniApp(frame_strojni)
app_manager = Manager(frame_manager)  # Manager v nové záložce

root.mainloop()

