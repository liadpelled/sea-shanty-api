from typing import Type
import requests
from lxml import html
import json
import urllib.parse
import re


url = "https://mainsailcafe.com/songs"

shanties = {}

#TODO DEAL WITH SPECIAL CHARACTERS IN URL
def get_tree(url):
    resp = requests.get(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    })
    resp.raise_for_status()

    tree = html.fromstring(html=resp.content)

    return tree

def scrape_song(url: str, song_name: str):

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

        print(song_url)

        scrape_song(song_url, song_name)

with open('shanties.json', 'w') as fp:
    json.dump(shanties, fp)