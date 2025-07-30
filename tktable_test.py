import tkinter as tk
from tktable import Table

root = tk.Tk()
root.geometry("800x400")

table_headers = ("Name", "Age", "Email")
mytable = Table(root, table_headers, col_width=150, headings_bold=True)
mytable.pack(pady=100)

row = ("Nitin", 18, "ngarg@mail.com")
mytable.insert_row(row)

root.mainloop()