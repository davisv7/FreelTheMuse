import requests
from bs4 import BeautifulSoup as bs


def fix_title(title):
    return "".join(x for x in title.replace(' ', '_') if x.isalnum() or x == '_')


# website = input('url?')
# website = 'https://freeallmusic.top/album/6244-7067-6415'
website = 'https://freeallmusic.top/album/6244-7067-6415'
with requests.get(website) as webobj:
    # print(bs(webobj.content))
    bsobj = bs(webobj.content, "html.parser")
box = bsobj.find('div', attrs={'class': 'col-lg-9 b-r no-border-md'})
# print(box)
songs_titles_links = box.find_all('div', attrs={'class': 'item-title text-ellipsis'})
artist = bsobj.find('a', attrs={'class': 'item-author _600'}).next.text
print(artist)
for item in songs_titles_links:
    anchor = item.find('a')
    song_title = anchor.text
    print(song_title)
    pre_song_link = anchor['href']
    # print(pre_song_link)
    with requests.get(pre_song_link) as pre_linkobj:
        pre_page = bs(pre_linkobj.content, "html.parser")
        song_link = pre_page.find('a', attrs={'class': 'text-danger'})['href']
    # print(song_link)
    with requests.get(song_link) as linkobj:
        page = bs(linkobj.content, 'html.parser')
        download_link = \
        page.find('a', attrs={'class': 'btn btn-outline-success text-uppercase mt-3 font-weight-bold db'})['href']
    # print(page)
    # print(download_link)
    song = requests.get(download_link, headers={'referer': song_link})
    with open(f'{fix_title(song_title)}.mp3', 'wb') as f:
        f.write(song.content)
    print('downloaded')
