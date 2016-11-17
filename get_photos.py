import requests
import argparse
from pathlib import Path
import re


access_token = "EAACEdEose0cBABKmf2X0nE5rV4j2PZBCN4r8SV7AuQtmi5lLZApOPgqkAS46g0HOKYo5f4oEBRRsWFgJshIEST0Uhvua8ZAF39vAel3aIuTusUNAZCa2GGdRQI538ZAkzaYvaVNVTifbgtmPU8zIkJhAggQptuPGJsbinzoVlOQZDZD"


parser = argparse.ArgumentParser(usage="%(prog)s [-h] --album-url ALBUM_URL --dir DIR --token TOKEN\nPlease go to http://developers.facebook.com/tools/explorer/145634995501895/ to get a token.")
parser.add_argument('--album', help='facebook album url to fetch', required=True)
parser.add_argument('--dir', help='name of the directory where to store the album', required=True)
parser.add_argument('--token', help='fb token', required=True)

# Valid for me, replace this by your own valid url or implement a real token getter ;)
args = parser.parse_args()


album_id = None
for regexp in [
    "https://www.facebook.com/media/set/\?set=a\.(\d+)\.\d+\.\d+&type=3",
    "https://www.facebook.com/(?:.*)/photos/?tab=album&album_id=(\d+)",
]:
    m = re.match(regexp, args.album)
    if m:
        album_id = m.group(1)
        break
else:
    print("Unable to extract id from url " + args.album)
    exit(1)

url = "https://graph.facebook.com/v2.8/" + album_id + "/photos?fields=images&limit=100&access_token=" + args.token

try:
    Path(args.dir).mkdir()
except Exception as e:
    print(e)
    pass

all_images = []
while True:
    print(url)
    res = requests.get(url)
    data = res.json()
    if res.status_code == 400 and data["error"]["code"] == 190:
        print("https://developers.facebook.com/tools/explorer/145634995501895/")
        exit(1)

    try:
        pictures = data["data"]
    except:
        print(res.status_code)
        print(data)
        exit(1)

    src = [
        img["images"][0]["source"]
        for img in pictures
    ]
    all_images += src

    if "next" not in data["paging"]:
        break
    url = data["paging"]["next"]


def download(url):
    fname = url.split("/")[-1]
    with open(args.dir + "/" + fname, "wb") as f:
        f.write(requests.get(url).content)
    return url


import concurrent.futures
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    for url in executor.map(download, all_images):
        print(url)
