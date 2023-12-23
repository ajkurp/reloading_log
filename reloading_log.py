import tkinter as tk
import csv
from tkinter import scrolledtext

root = tk.Tk()
root.geometry('1000x500')
root.title('v.1.06')
""" v.1.06 added code to clear fields after write to log
    moved field 1 focus statement"""

frame_labels = tk.Frame(root, padx=15, bd=10, relief='raised')
frame_entry = tk.Frame(root, padx=15, bd=10, relief='raised')
frame_notes = tk.Frame(root, padx=15, bd=10, relief='raised')
frame_commands = tk.Frame(root, padx=15, bd=10, relief='raised')

frame_labels.grid(row=0, column=0, sticky='n')
frame_entry.grid(row=0, column=1, sticky='n')
frame_notes.grid(row=0, column=2)  # notes on right
# frame_notes.grid(row=2, columnspan=2)  # notes underneath !change root.geometry to match
frame_commands.grid(row=3, columnspan=3, sticky='w')

load_data = []  # this holds entry objects, not string data


def data_list_maker(load_data, notes_scroll_text):

    notes_text_text = notes_scroll_text.get("1.0", tk.END)      # get the text in 'notes'

    data_list = []
    for data in load_data:
        data_list.append(data.get())        # append all text in standard text widgets

    data_list.append(notes_text_text.strip())   # append notes text while stripping the \n and any extra whitespace
    clear_entry_contents(load_data, notes_scroll_text)
    # write_csv(data_list)              # uncomment to write log
    print(data_list)                    # for testing code without writing log


def clear_entry_contents(load_data, notes_scroll_text):
    for ele in load_data:  # clear entry contents
        ele.delete(0, 'end')
    notes_scroll_text.delete('1.0', tk.END)
    load_data[0].focus_set()  # cursor to first entry box


def write_csv(data_list):

    with open('/home/ajk/Desktop/log.csv', 'a', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(data_list)


def build_form(fields):  # use grid() and a loop to place labels on frame_labels
    count = 0
    for field in fields:
        label = tk.Label(frame_labels, text=field, pady=6)
        entry = tk.Entry(frame_entry, width=40, border=5)
        load_data.append(entry)
        label.grid(row=count, column=0)
        entry.grid(row=count, column=1)
        count += 1

    notes_label = tk.Label(frame_notes, text='Notes')
    notes_scroll_text = scrolledtext.ScrolledText(frame_notes,
                                                  wrap=tk.WORD,
                                                  width=40,
                                                  height=15,
                                                  font=("Times New Roman",
                                                        15))

    notes_label.grid(row=0, column=1)
    notes_scroll_text.grid(row=1, column=1)
    save_to_file_btn = tk.Button(frame_commands, command=lambda:
                                data_list_maker(load_data, notes_scroll_text),
                                text='Build List for csv', pady=20)
    save_to_file_btn.grid(row=0, column=0)
    load_data[0].focus_set()  # cursor to first entry box


fields = ["Caliber", "Date", "Case", "Powder", "Powder Weight", "Primer", "Bullet"]  # add new entry fields here
build_form(fields)
root.mainloop()

""" Next  """
