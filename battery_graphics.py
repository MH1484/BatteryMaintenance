
import os
import csv
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------
PLOTS_PER_ROW = 3         # Anzahl der Plots nebeneinander?
SHOW_PARTIAL_LOADS = True # Halbe Ladungen anzeigen?

def find_csv_files(start_dir="."):
    csv_files = []

    for dirpath, _, filenames in os.walk(start_dir):
        for f in filenames:
            if f.lower().endswith(".csv"):
                csv_files.append(os.path.join(dirpath, f))

    return sorted(csv_files)

def is_float_with_comma(s):
    try:
        float(s.replace(",", "."))
        return True
    except ValueError:
        return False

datasets = []
for csv_file in find_csv_files():
  label = csv_file
  x = []
  y = []
  time = 0
  maxvalue = 0
  with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    for row in reader:
        if row and is_float_with_comma(row[1]):  # skip header row
            value = float(row[1].replace(",", "."))
            y.append(value)
            x.append(time)
            time = time + 1
            if value > maxvalue:
              maxvalue = value

  if SHOW_PARTIAL_LOADS or maxvalue > 6: 
    datasets.append({"label": label, "x": x, "y": y})

print("Visualizing " + str(len(datasets)) + " datasets")

root = tk.Tk()
root.title("Mehrere Verbrauchsplots")

root.state("zoomed")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

content_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")


plot_canvases = []

row = 0
col = 0

for data in datasets:
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(data["x"], data["y"])
    ax.set_title(data["label"])
    ax.set_xlabel("Zeit (s)")
    ax.set_ylabel("Leistung (W)")
    ax.grid(True)

    fig.subplots_adjust(left=0.15)
    fig.subplots_adjust(bottom=0.25)

    plot_canvas = FigureCanvasTkAgg(fig, master=content_frame)
    widget = plot_canvas.get_tk_widget()
    widget.grid(row=row, column=col, padx=10, pady=10, sticky="n")

    plot_canvases.append(widget)

    col += 1
    if col >= PLOTS_PER_ROW:
        col = 0
        row += 1

def resize_plots(event=None):
    total_width = root.winfo_width()
    plot_width = total_width / PLOTS_PER_ROW * 0.95

    for widget in plot_canvases:
        widget.config(width=int(plot_width))

root.bind("<Configure>", resize_plots)

try:
    while True:
        root.update_idletasks()
        root.update()
except KeyboardInterrupt:
    print("Beende Programm…")
    root.destroy()
