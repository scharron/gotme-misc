import requests
from pathlib import Path
import csv
from collections import defaultdict

event_photos = defaultdict(list)

def normalize(name):
    return name.replace(" ", "_").replace("'", "_")

rows = csv.reader(open("gotme-misc/export.csv", newline=""))
headers = next(rows)

for row in rows:
    event_photos[normalize(row[1])].append(row[-2])

for event, photos in event_photos.items():
    try:
        Path(event).mkdir()
    except Exception as e:
        print(e)
        pass
