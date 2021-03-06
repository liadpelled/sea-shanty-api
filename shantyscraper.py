from typing import Type
import requests
from lxml import html
import json
import urllib.parse
import re
from bs4 import BeautifulSoup


# The website URL to be scraped
url = "https://mainsailcafe.com/songs"

# Scraped titles and lyrics will be stored in this dictionary
shanties = {}

#TODO DEAL WITH SPECIAL CHARACTERS IN URL
def get_tree(url):
    """This function uses the requests module to get a web page and returns its content to be later searched using XPath."""
    resp = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    })
    resp.raise_for_status()

    tree = html.fromstring(html=resp.content)

    return tree


def get_tree_bs4(url):
    """This function uses the requests module to get a web page and returns its content to be later searched using BeautifulSoup."""
    resp = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    })
    resp.raise_for_status()

    return resp.content


def scrape_song(url: str, song_name: str):
    """This function uses XPath to scrape the lyrics of a shanty, given its URL."""

    print("Scraping song "+song_name+"...")

    song_lyrics = []
    try:
        song_tree = get_tree(url)
    except requests.exceptions.HTTPError:
        return

    try:
        lyrics_div = song_tree.xpath("//div[@class='lyrics']")[-1]
    except IndexError:
        return

    lyrics_paragraphs = lyrics_div.xpath(".//p")

    for lyrics_p in lyrics_paragraphs:
        p_lines = lyrics_p.xpath(".//text()")

        for i in range(len(p_lines)):
            p_lines[i] = p_lines[i].strip()
            p_lines[i] = re.sub("[^ A-Za-z’:]", "", p_lines[i])
            p_lines[i] = re.sub("Ch:", "", p_lines[i])

        joined_p = " / ".join(p_lines)
        joined_p = re.sub("  /", "", joined_p)
        
        song_lyrics.append(joined_p)

    if song_lyrics:
        shanties[song_name] = song_lyrics


def add_to_lyrics(song_lyrics, row):
    """This function assits in dividing lyrics into 4 line verses, when the original lyrics appear in one large paragraph."""

    num_verses = len(song_lyrics)

    for i in range(num_verses):
        if len(song_lyrics[i]) < 4:
            song_lyrics[i].append(row)
        else:
            if i == num_verses - 1:
                song_lyrics.append([])
                song_lyrics[i+1].append(row)


def scrape_song_bs4(url: str, song_name: str):
    """This function uses BeautifulSoup to scrape the lyrics of a shanty, given its URL."""

    print("Scraping song " + song_name + "...")

    song_lyrics = [[]]
    verse=0

    try:
        song_tree = get_tree_bs4(url)
    except requests.exceptions.HTTPError:
        return

    soup = BeautifulSoup(song_tree, 'html.parser')
    lyrics_div = soup.find('div', class_ = 'lyrics')

    try:
        lyrics_ps = lyrics_div.find_all('p')
        singlep = True if len(lyrics_ps)==1 else False

        for item in lyrics_ps:
            em_tags = item.find_all('em')
            for emt in em_tags:
                emt.replace_with(emt.text)
            
            strong_tags = item.find_all('strong')
            for strt in strong_tags:
                strt.replace_with(strt.text)
            
            str_item = str(item)[3:-4].replace('<br/>', '&')
            if str_item[-1] == '&':
                str_item = str_item[:-1]
            str_item = re.sub(r'&+', r'&', str_item)
            str_item = re.sub(r'Ch:', '', str_item)
            lyrics_rows = str_item.split('&')

            if singlep:
                for row in lyrics_rows:
                    add_to_lyrics(song_lyrics, row.strip())
            else:
                for row in lyrics_rows:
                    if verse == len(song_lyrics):
                        song_lyrics.append([])
                    song_lyrics[verse].append(row.strip())
                verse += 1
    except IndexError as e:
        print(f"Error scraping song: {e}")
        return

    if song_lyrics[0]:
        shanties[song_name] = song_lyrics


# Go through 9 pages on the website
for i in range(9):
    if i==0:
        tree = get_tree(url)
    else:
        tree = get_tree(url+"?page="+str(i+1))

    song_entries = tree.xpath("//div[@class='song-entry']/a")

    for song_entry in song_entries:
        song_name = song_entry.xpath(".//text()")[0].strip()
        song_url = song_entry.xpath(".//@href")[0]

        split_url = urllib.parse.urlsplit(song_url)
        split_url = list(split_url)

        split_url[2] = urllib.parse.quote(split_url[2]) 
        song_url = urllib.parse.urlunsplit(split_url)

        scrape_song_bs4(song_url, song_name)


# Save the scraped shanties to a JSON file         
with open('shanties.json', 'w') as fp:
    json.dump(shanties, fp)