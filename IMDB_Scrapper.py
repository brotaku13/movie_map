from bs4 import BeautifulSoup
import requests
from collections import OrderedDict

r = requests.get("http://www.imdb.com/title/tt0092099/")
soup = BeautifulSoup(r.content, "lxml")

movies = {}
for links in soup.find_all("div", class_="rec_overview"):
    # find link
    link = links.find('a')  #relative hyperlink

    # ttcode
    tt_code = link.get('href').split('/')[2]

    # find title
    title = link.next_element['alt']

    # find rating
    div = links.find('div', class_='rating rating-list')
    rating = float(div.attrs['id'].split('|')[2])

    # find votes
    temp = div.attrs['title']

    # following function finds number between parentheses, replaces the ',' with '' and then turns the number into an int
    votes = int(temp[temp.find('(') + 1:temp.find(' ', temp.find('('))].replace(',', ''))

    #adds information to a dictionary
    movies[votes] = [title, tt_code, rating]


sorted = sorted(movies)  # sorts movies, returns list of movie keys in sorted order
topThree = {}
for i in range(len(sorted) - 1, len(sorted) - 4, -1):  # iterates backwards over list and adds last three to a new dictionary
    topThree[sorted[i]] = movies[sorted[i]]

print(topThree)






