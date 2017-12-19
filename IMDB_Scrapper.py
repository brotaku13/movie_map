from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

r = requests.get("http://www.imdb.com/title/tt0092099/")
soup = BeautifulSoup(r.content, "lxml")

for links in soup.find_all("div", class_="rec_overview"):
    link = links.find('a')
    print(link.get("href"))
    rating = links.find("div", class_="rating rating-list")
    print("title")
    print(rating.title)