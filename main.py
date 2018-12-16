import requests
from bs4 import BeautifulSoup as bs
import time
from os import getcwd, makedirs
from os.path import join, exists
from re import sub
import shutil


class FEMloader:

    def __init__(self, url):

        self.website = url
        first_soup = make_soup(self.website)
        song_box = first_soup.find('div', attrs={'class': 'col-lg-9 b-r no-border-md'})
        titles_links = song_box.find_all('div', attrs={'class': 'item-title text-ellipsis'})
        self.artist = self.fix_string(first_soup.find('a', attrs={'class': 'item-author _600'}).next.text)
        print(self.artist)
        self.album = self.fix_string(sub('[\ \n]{2,}', '', first_soup.find('h4', attrs={'class': 'inline'}).text))
        print(self.album)
        cwd = getcwd()
        self.dl_location = join(cwd, 'albums', self.artist, self.album)
        self.zip_location = join(cwd, 'zips')
        self.zip_name = join('zips', self.album + '.zip')

        if not exists(self.dl_location):
            makedirs(self.dl_location)
        if not exists(self.zip_location):
            makedirs(self.zip_location)

        for item in titles_links:
            anchor = item.find('a')
            self.title, pre_link = anchor.text, anchor['href']
            print(self.title)
            pre_soup = make_soup(pre_link)
            self.referer = pre_soup.find('a', attrs={'class': 'text-danger'})['href']
            page_soup = make_soup(self.referer)
            self.download_link = page_soup.find('div', attrs={'class': 'card-body px-0'}).a['href']
            self.save_song()
        self.make_zip()

    def fix_string(self, string):
        return "".join(x for x in string.replace(' ', '_') if x.isalnum() or x == '_')

    def save_song(self):
        song = requests.get(self.download_link, headers={'referer': self.referer})
        with open(f'{join(self.dl_location,self.fix_string(self.title))}.mp3', 'wb') as f:
            f.write(song.content)
        print(f'downloaded {self.title}, sleeping 3 seconds')
        time.sleep(3)

    def make_zip(self):
        shutil.make_archive(join(self.zip_location, self.album), 'zip', self.dl_location)


def make_soup(link):
    with requests.get(link) as webobj:
        soup = bs(webobj.content, "html.parser")
    time.sleep(1)
    return soup
