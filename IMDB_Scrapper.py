import bs4 as bs
import urllib.request
import pandas as pd

sauce =  urllib.request.urlopen("http://www.imdb.com/title/tt0092099/").read()
soup = bs.BeautifulSoup(sauce, "lxml")

body = soup.body

for paragraph in body.find_all("div", class_ = "rec_overview"):
    print(paragraph.get('href'))