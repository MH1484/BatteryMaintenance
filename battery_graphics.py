import os
import csv
import json
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# KONFIGURATION
# ---------------------------------------------------------
PLOTS_PER_ROW = 3
SHOW_PARTIAL_LOADS = True

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
    x, y = [], []
    time = 0
    maxvalue = 0

    # 🔹 JSON laden (falls vorhanden)
    json_data = None
    json_file = os.path.join(os.path.dirname(csv_file), "battery_info.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as jf:
                json_data = json.load(jf)
        except Exception as e:
            print(f"Fehler beim Laden von {json_file}: {e}")

    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if row and len(row) > 1 and is_float_with_comma(row[1]):
                value = float(row[1].replace(",", "."))
                y.append(value)
                x.append(time)
                time += 1
                if value > maxvalue:
                    maxvalue = value

    if SHOW_PARTIAL_LOADS or maxvalue > 6:
        datasets.append({
            "label": label,
            "x": x,
            "y": y,
            "json": json_data
        })

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
row, col = 0, 0

for data in datasets:
    fig, ax = plt.subplots(figsize=(4, 3))

    # 🔹 Linie + Fläche
    ax.plot(data["x"], data["y"])
    ax.fill_between(data["x"], data["y"], alpha=0.2)  # 80% transparent
    
    ax.set_title(data["label"])
    ax.set_xlabel("Zeit (s)")
    ax.set_ylabel("Leistung (W)")
    ax.grid(True)

    # 🔹 Energie berechnen
    energy_Wh = sum(data["y"]) / 3600.0

    # Position berechnen (20% von Achsenbereich)
    x_pos = min(data["x"]) + 0.2 * (max(data["x"]) - min(data["x"]))
    y_pos = min(data["y"]) + 0.2 * (max(data["y"]) - min(data["y"]))

    # Wh direkt in Fläche anzeigen
    ax.text(
        x_pos,
        y_pos,
        f"{energy_Wh:.2f} Wh",
        ha="left",
        va="bottom",
        fontsize=10,
        color="black",
        bbox=dict(facecolor="white", alpha=0.5, edgecolor="none")
    )

    # 🔹 Text vorbereiten
    text_lines = []

    if data["json"]:
        jd = data["json"]
        if "Name" in jd:
            text_lines.append(f"{jd['Name']}")
        if "Voltage" in jd:
            text_lines.append(f"{jd['Voltage']}")
        if "Capacity" in jd:
            text_lines.append(f"{jd['Capacity']}")

    display_text = "\n".join(text_lines)

    # 🔹 Anzeige oben rechts
    ax.text(
        0.98, 0.95,
        display_text,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none")
    )

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
