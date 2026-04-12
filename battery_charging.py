import requests
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import signal
import sys
from datetime import datetime

SHELLY_IP = "192.168.178.193"
CSV_FILE = "shelly_verbrauch.csv"

timestamps = []
power_values = []

def shelly_on():
    try:
        requests.get(f"http://{SHELLY_IP}/relay/0?turn=on", timeout=3)
        print("Shelly eingeschaltet")
    except Exception as e:
        print("Fehler beim Einschalten:", e)

def shelly_off():
    try:
        requests.get(f"http://{SHELLY_IP}/relay/0?turn=off", timeout=3)
        print("Shelly ausgeschaltet")
    except Exception as e:
        print("Fehler beim Ausschalten:", e)

def get_power():
    try:
        raw = requests.get(f"http://{SHELLY_IP}/rpc/shelly.getstatus", timeout=3)
        power = float(raw.json()["switch:0"]["apower"])
        return power
    except Exception as e:
        print("Fehler beim Abfragen:", e)
        return 0

def update(frame):
    power = get_power()
    now = datetime.now().strftime("%H:%M:%S")

    timestamps.append(time.time())
    power_values.append(power)
    print("Power at " + str(now) + ": " + str(power) + "W")

    csv_writer.writerow([now, str(power).replace(".", ",")])
    csv_file.flush()

    start = timestamps[0]
    x_seconds = [t - start for t in timestamps]

    plt.cla()
    plt.gcf().canvas.manager.set_window_title("Live-Verbrauch")
    plt.plot(x_seconds, power_values, label="Leistung (W)")
    plt.xlabel("Zeit seit Start (s)")
    plt.ylabel("Leistung (W)")
    plt.title("Live-Verbrauch")
    plt.legend()
    plt.tight_layout()

def handle_exit(sig, frame):
    print("\nBeende Programm…")
    shelly_off()
    csv_file.close()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

if __name__ == "__main__":
    shelly_on()

    csv_file = open(CSV_FILE, "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter=";")
    csv_writer.writerow(["Timestamp", "Power_W"])

    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update, interval=1000)

    print("Live-Plot läuft… (Strg+C zum Beenden)")
    plt.show()

    shelly_off()
    csv_file.close()
