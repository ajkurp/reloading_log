# https://www.youtube.com/watch?v=_XR2VnvqBw4&list=PLCQT7jmSF-LrwYppkB3Xdbe6QC81-ozmT&index=2
""" you are here:
https://www.youtube.com/watch?v=Wq1MmAtp1oY&list=PLCQT7jmSF-LrwYppkB3Xdbe6QC81-ozmT&index=8
time hack 0:00
.. but resume here first to set up github ssh keys: https://www.youtube.com/watch?v=RGOj5yH7evk
time / 20:32
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path

import tkinterdnd2
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd

class Application(tkinterdnd2.Tk):  # inherits drag n drop functionality
    def __init__(self):         # constructor for parent widget
        super().__init__()
        self.title('CSV Viewer')
        self.main_frame = tk.Frame(self)    # widgets bound here
        self.main_frame.pack(fill='both', expand= True)
        self.geometry('900x500')
        self.search_page = SearchPage(parent=self.main_frame)  # create SearchPage instance, bind SP objects to main_frame

class DataTable(ttk.Treeview):      # create custom treeview inherits from ttk.Treeview
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient='vertical', command=self.yview)  # yview(self)?  define scroll bar
        scroll_X = tk.Scrollbar(self, orient='horizontal', command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)  # make scroll_X, s*_Y useable
        scroll_Y.pack(side='right', fill='y')       # fill y axis
        scroll_X.pack(side='bottom', fill='x')
        self.stored_dataframe = pd.DataFrame()      # create dataframe that this treeview will reference
    # The DataTable inherits all the functionality from ttk.Treeview, but we can add to that:
    # provide method below with dataframe, should store it and draw it out on datatable

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)          # private method, hence the underscore

    def _draw_table(self, dataframe):       # method here 'cause we'll re-use this later
        self.delete(*self.get_children())       # clears treeview
        columns = list(dataframe.columns)       # get columns of the dataframe
        # set some attributes of the treeview widget:
        self.__setitem__('column', columns)  # known as a subscription where 'column' is a key and columns a value
        self.__setitem__('show', 'headings')    # removes blank space in headings?

        for col in columns:
            self.heading(col, text=col)     # heading will be col name

        df_rows = dataframe.to_numpy().tolist()    # convert dataframe to numpy array, then to list [list of lists]

        for row in df_rows:
            self.insert("", 'end', values=row)  # no parent, insert at end
        return None         # end without returning value

    def find_values(self, pairs):   # where pairs is gonna be a dictionary
        new_df = self.stored_dataframe   # reference stored_dataframe

        for col, value in pairs.items():
            # query_string = f"(col).str.contains('(value)')"  # TODO SEE IF THIS FIX WORKS
            query_string = f"{col}.str.contains('{value}')"
            new_df = new_df.query(query_string, engine = 'python')
        self._draw_table(new_df)



    def reset_table(self):      # return table to original state
        self._draw_table(self.stored_dataframe)



class SearchPage(tk.Frame):         # 'inherits' Frame functionality- means it IS a Frame -->
    def __init__(self, parent):    # constructor- notice a pattern? "Parent is the parent needed to initialize the tk.Frame"  HUH?
        super().__init__(parent)    # super() is the constructor
        # create the listbox at left of screen
        self.file_names_listbox  = tk.Listbox(parent, selectmode=tk.SINGLE, background='dark gray') # SINGLE select one only
        # self.file_names_listbox.place(relheight=1, relwidth=0.25)   # resizes with window TODO adjust width
        self.file_names_listbox.place(relheight=1, relwidth=0.10)
        self.file_names_listbox.drop_target_register(DND_FILES)  # can drop file type paths here
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)    # bind event for DND
        self.file_names_listbox.bind("<Double-1>", self.display_file)      # bind event to display file

        # create the entrybox at the top of the screen
        self.search_entrybox = tk.Entry(parent)
        # self.search_entrybox.place(relx=0.25, relwidth=0.75)  # TODO adjust width
        self.search_entrybox.place(relx=0.10, relwidth=0.90)
        self.search_entrybox.bind("<Return>", self.search_table)   # bind for entrybox 'return'

        """ Treeview data_table"""
        self.data_table = DataTable(parent) # data_table object create of class DataTable on 'parent' which up on
                                            # line 17 is the SearchPage(parent=self.main_frame)
        # self.data_table.place(rely=0.05, relx=0.25, relheight=0.95, relwidth=0.75)  # same relx & y as search_entrybox TODO adjust size
        self.data_table.place(rely=0.05, relx=0.10, relheight=0.95, relwidth=0.90)
        self.path_map = {}      # dict object to hold paths of csv files

    def drop_inside_list_box(self, event):
        # return a list of file paths:
        file_paths = self.parse_drop_files(event.data)      # call parse_drop_files
        current_listbox_items = set(self.file_names_listbox.get(0, 'end'))
        for file_path in file_paths:
            if file_path.endswith('.csv'):      # only accept .csv files
                path_object = Path(file_path)
                file_name = path_object.name
                if file_name not in current_listbox_items:
                    self.file_names_listbox.insert('end', file_name)    # display file name in listbox
                    self.path_map[file_name] = file_path




    def display_file(self, event):
        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection())
        path = self.path_map[file_name]         # path_map is a dictionary{key=file_name:data=full path to file}
        df = pd.read_csv(path)                  # create a dataframe using pandas
        self.data_table.set_datatable(dataframe=df)    # we created the data_table.set method in class SearchPage above








    def parse_drop_files(self, filename):
        # '/home/ajk/Desktop/addresses.csv /home/ajk/Desktop/log.csv'  Some csv files may use a 'space' and will have a curly bracket in the data string
        # this is the author's code.  I think I can do better.
        size = len(filename)
        res = []  # result = list of file paths
        name = ""
        idx = 0
        while idx < size:
            # need to lose the curly braces:
            if filename[idx] == '{':    #  we're inside a string that contains spaces
                j = idx + 1
                while filename[j] != "}":   # Looking for the end curlybrace
                    name += filename[j]
                    j += 1
                res.append(name)    # append path string to name
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""
            elif filename[idx] != " ":
                name += filename[idx]
            idx +=1
        if name != "":
            res.append(name)
        return res


    def search_table(self, event):
        # column1 = value, column2 = value, ...
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(',')  # split entry key:val pairs into lists: [col1, val], [col2, val], ...
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split('=')  # [col1=val], [col2=val], ...
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
                self.data_table.find_values(pairs=column_value_pairs)


        pass


if __name__ == "__main__":
    root = Application()
    root.mainloop()

