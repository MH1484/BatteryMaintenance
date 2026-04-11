import os
import csv
from datetime import datetime

def find_csv_files(start_dir="."):
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.lower().endswith(".csv"):
                yield os.path.join(root, file)

def is_float_with_comma(s):
    try:
        float(s.replace(",", "."))
        return True
    except ValueError:
        return False

def read_file(csv_path):
    first   = None
    latest  = None
    highest = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if row and is_float_with_comma(row[1]):  # skip header row
                time  = row[0]
                power = float(row[1].replace(",", "."))
                
                if power > 0:
                  latest = time
                  if first == None:
                    first = time
                  if power > highest:
                    highest = power

    duration = datetime.strptime(latest, "%H:%M:%S") - datetime.strptime(first, "%H:%M:%S")
    print(str(csv_path) + "   " + str(first) + "   " + str(latest) + "   " + str(duration) + "   " + str(highest))

def main():
    print("File                        First      Latest     Duration  MaxPower")
    #      .\G-174870\2026-04-11.csv   11:43:37   12:23:27   0:39:50   2.1W

    for csv_file in find_csv_files("."):
        read_file(csv_file)

if __name__ == "__main__":
    main()
