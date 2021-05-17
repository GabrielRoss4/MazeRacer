import tkinter as tk

root = tk.Tk()

DFS_button = tk.Button(root, text="DFS", padx=29, pady=1, anchor=tk.CENTER).pack()
Djkstras_button = tk.Button(root, text="Djkstra's", padx=17, pady=1, anchor=tk.CENTER).pack()
Astar_button = tk.Button(root, text="A*", padx=32.25, pady=1, anchor=tk.CENTER).pack()

root.mainloop()