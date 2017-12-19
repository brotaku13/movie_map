from bs4 import BeautifulSoup
import requests

r = requests.get("http://www.imdb.com/title/tt0092099/")
soup = BeautifulSoup(r.content, "lxml")

movies = {}
for links in soup.find_all("div", class_="rec_overview"):
    #find link
    link = links.find('a')
    print(link.get("href"))

    #ttcode
    tt_code = link.get('href').split('/')[2]

    #find title
    title = link.next_element['alt']
    print(title)

    #find rating
    div = links.find('div', class_='rating rating-list')
    #rating = float(div.attrs['id'].split('|')[2])  this gets star rating
    #find votes

    print(title)




