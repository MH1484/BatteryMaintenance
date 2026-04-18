import os
import csv
from datetime import datetime

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

def PrintLine(data):
    width = [42, 11, 11, 11, 5]
    for d, w in zip(data, width):
        print(f"{d:<{w}}", end="")
    print("")

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
    PrintLine([str(csv_path), str(first), str(latest), str(duration), str(highest) + "W"])

def main():
    PrintLine(["File", "First", "Latest", "Duration", "MaxPower"])
    for csv_file in find_csv_files("."): read_file(csv_file)

if __name__ == "__main__":
    main()
