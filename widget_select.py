"""Two ways to focus_set():
1   name the widget and focus_set; eg. entry_1 = tk.Entry() | entry1.focus_set()  and
2   put unnamed entry widgets in a list to loop over and set focus by position reference as
    in line 28 here using list load_data[position]"""
import tkinter as tk
root = tk.Tk()
root.geometry("500x500")

load_data = []      # list to hold entry widgets
def make_entrys(fields):
    count = 0                           # row count for entry.grid()
    for field in fields:
        entry = tk.Entry(root, width=40, border=5)
        entry.grid(row=count, column=1)
        load_data.append(entry)         # build the list of widgets
        count += 1

    for ent in load_data:
        print('f: field:  ', ent)

    load_data[0].focus_set()



fields  = ["One", "two", "three"]
make_entrys(fields)
root.mainloop()

