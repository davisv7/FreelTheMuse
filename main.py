import requests
from bs4 import BeautifulSoup as bs
import time
from os import getcwd, makedirs
from os.path import join, exists


def fix_title(title):
    return "".join(x for x in title.replace(' ', '_') if x.isalnum() or x == '_')


def make_soup(link):
    with requests.get(link) as webobj:
        soup = bs(webobj.content, "html.parser")
    time.sleep(1)
    return soup


def save_song(title, artist, link, referer):
    cwd = getcwd()
    path = join(cwd, artist)
    song = requests.get(link, headers={'referer': referer})
    if not exists(path):
        makedirs(path)
    with open(f'{join(path,title)}.mp3', 'wb') as f:
        f.write(song.content)
    print(f'downloaded {title}, sleeping 3 seconds')
    time.sleep(3)


def main():
    # website = input('url?')
    website = 'https://freeallmusic.top/album/3283-6611-3447'

    a_soup = make_soup(website)
    box = a_soup.find('div', attrs={'class': 'col-lg-9 b-r no-border-md'})
    songs_titles_links = box.find_all('div', attrs={'class': 'item-title text-ellipsis'})
    artist = a_soup.find('a', attrs={'class': 'item-author _600'}).next.text
    print(artist)
    for item in songs_titles_links:
        anchor = item.find('a')
        song_title = anchor.text
        print(song_title)
        pre_song_link = anchor['href']
        pre_soup = make_soup(pre_song_link)
        song_link = pre_soup.find('a', attrs={'class': 'text-danger'})['href']
        page_soup = make_soup(song_link)

        download_link = \
            page_soup.find('a', attrs={'class': 'btn btn-outline-success text-uppercase mt-3 font-weight-bold db'})[
                'href']
        save_song(song_title, artist, download_link, song_link)


if __name__ == '__main__':
    main()
