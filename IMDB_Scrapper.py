from bs4 import BeautifulSoup
import requests
from collections import OrderedDict

def get_info(movie_link, rows_deep, count):
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

    for i in range(-1, -4, -1):  # iterates backwards over list and adds last three to a new dictionary
        topThree[sorted_movies[i]] = movies[sorted_movies[i]]

    print(topThree)

    # creates BeautifulSoup objects to be passed into the recursive function
    count += 1

    r1 = requests.get("http://www.imdb.com/title/" + tt_code_list[0])
    movie1 = BeautifulSoup(r1.content, "lxml")
    get_info(movie1, rows_deep, count)

    r2 = requests.get("http://www.imdb.com/title/" + tt_code_list[1])
    movie2 = BeautifulSoup(r2.content, "lxml")
    get_info(movie2, rows_deep, count)

    r3 = requests.get("http://www.imdb.com/title/" + tt_code_list[2])
    movie3 = BeautifulSoup(r3.content, "lxml")
    get_info(movie3, rows_deep, count)



def main():

    r = requests.get("http://www.imdb.com/title/tt0092099/")
    soup = BeautifulSoup(r.content, "lxml")

    rows_deep = 3
    count = 0

    get_info(soup, rows_deep, count)

if __name__ == "__main__":
    main()





