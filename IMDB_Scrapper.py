from bs4 import BeautifulSoup
import requests
from collections import OrderedDict

r = requests.get("http://www.imdb.com/title/tt0092099/")
soup = BeautifulSoup(r.content, "lxml")

CONST_CONNECTIONS = 3
rows_deep = 3
count = 0

def get_info(movie_link, CONST_CONNECTIONS, rows_deep, count):
    if(count == rows_deep):
        return

    movies = {}
    tt_code_list = []

    for links in movie_link.find_all("div", class_="rec_overview"):
        # find link
        link = links.find('a')  #relative hyperlink

        # ttcode
        tt_code = link.get('href').split('/')[2]
        tt_code_list.append(tt_code)

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

    sorted_movies = sorted(movies)  # sorts movies, returns list of movie keys in sorted order
    topThree = {}

    for i in range(len(sorted_movies) - 1, len(sorted_movies) - 4, -1):  # iterates backwards over list and adds last three to a new dictionary
        topThree[sorted_movies[i]] = movies[sorted_movies[i]]

    print(topThree)

    # creates BeautifulSoup objects to be passed into the recursive function
    r1 = requests.get("http://www.imdb.com/title/" + tt_code_list[0])
    movie1 = BeautifulSoup(r1.content, "lxml")

    r2 = requests.get("http://www.imdb.com/title/" + tt_code_list[1])
    movie2 = BeautifulSoup(r2.content, "lxml")

    r3 = requests.get("http://www.imdb.com/title/" + tt_code_list[2])
    movie3 = BeautifulSoup(r3.content, "lxml")

    count += 1
    get_info(movie1, CONST_CONNECTIONS, rows_deep, count)
    get_info(movie2, CONST_CONNECTIONS, rows_deep, count)
    get_info(movie3, CONST_CONNECTIONS, rows_deep, count)



def main():
    get_info(soup, CONST_CONNECTIONS, rows_deep, count)

if __name__ == "__main__":
    main()





