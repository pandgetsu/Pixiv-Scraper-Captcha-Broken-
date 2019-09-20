# Search for href and entry
# append that to root url
# Visit new link and search for src and large
# https://weheartit.com/pinkystrawberri/collections/18974807-kim-seuk-hye?page=16&before=97868273
# Number of pages look for pagination-counter-total
# Visit each page individually
# pixiv
# use the id number to find the img
# https://i.pximg.net/img-original/img/2019/05/01/18/23/20/74493751_p0.jpg
# use the numbers up to the date to find the right url for img
# the last 3 numbers are seemingly random so loop through all,
# use page source and search for the date using
# https:\/\/i.pximg.net\/c\/540x540_70\/img-master\/img\/2019\/05\/18\/07\/28\/22\/74778139_p0_master1200.jpg"
# that has all the data copy up to the date and replace the id
# scratch that use page source and find "original":"https: to do it

import urllib.request
import time
import requests
from bs4 import BeautifulSoup
import re
from pixiv_scraper import scrape
import shutil

"""
    :param url: the url of the image page
    :param path: path to download to
"""
#main url
def pixiv_page_scrape(url, path):
    #print("this is it")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pattern = re.compile(r'https:\\/\\/i.pximg.net\\/c\\/\d{2,3}x\d{2,3}_\d{2}\\/img-master\\/img\\/\d{4}\\/\d{2}\\/\d{2}\\/\d{2}\\/\d{2}\\/\d{2}\\/\d{6,8}_p\d_[A-z]{6}\d{4}.[a-z]{3}')
    namepattern = re.compile(r'\d{6,8}_p\d{1,2}')
    #print(str(soup))
    link = pattern.search(str(soup))
    num = 0

    def downloadfile(extension):
        download = scrape(link.group(0), num, extension)
        filepath = namepattern.search(download)
        req = urllib.request.Request(download)
        req.add_header('Referer', 'http://wwww.pixiv.net/')
        r = urllib.request.urlopen(req)
        down_path = path + filepath.group(0) + extension
        with open(down_path, 'b+w')as f:
            f.write(r.read())
        print("Downloading: ", download)

    while 1:
        try:
            downloadfile(".png")
            num += 1
        except OSError as exc:
            try:
               downloadfile(".jpg")
               num += 1
            except OSError as exc:
                break

    # with urllib.request.urlopen(download) as response, open("DATA/sheya.png", 'wb') as out_file:
    #     shutil.copyfileobj(response, out_file)


if __name__ == "__main__":
    url = input("Please input the url: ") #url for illust page of artist
    path = ''   #Path to download to including tmp if including
    pixiv_page_scrape(url, path)