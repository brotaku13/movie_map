from bs4 import BeautifulSoup
import requests

def get_info(movie_link, rows_deep, count, movies_visited):

    if(count == rows_deep):
        return

    movies = {}
    tt_code_list = []

    for links in movie_link.find_all("div", class_="rec_overview"):
        # find link
        link = links.find('a')  #relative hyperlink

        # get ttcode
        tt_code = link.get('href').split('/')[2]
        #creates list of all ttCode of recommended movies
        tt_code_list.append(tt_code)


        # find title
        title = link.next_element['alt']

        # find rating
        div = links.find('div', class_='rating rating-list')
        rating = float(div.attrs['id'].split('|')[2])

        # find votes
        temp = div.attrs['title']

        # finds number between parentheses, replaces the ',' with '' and then turns the number into an int
        votes = int(temp[temp.find('(') + 1:temp.find(' ', temp.find('('))].replace(',', ''))

        #adds information to a dictionary
        movies[votes] = [title, tt_code, rating]

    sorted_movies = sorted(movies)  # sorts movies, returns list of movie keys in sorted order

    topThree = {}

    visit = 0
    index = len(sorted_movies) - 1
    while visit < 3 and index > 0:  #visit 3 movies or the whole movies list, whichever comes first.
        if movies[sorted_movies[index]][1] not in movies_visited:
            topThree[sorted_movies[index]] = movies[sorted_movies[index]]
            movies_visited.append(topThree[sorted_movies[index]][1])
            visit += 1
        else:
            print('{} already visited'.format(movies[sorted_movies[index]][0]), end=', ')
        index -= 1
    print('')

    print('topThree:', topThree)

    count += 1  # increment count for recursive function

    for key, value in topThree.items():
        r1 = requests.get("http://www.imdb.com/title/" + value[1])
        movie = BeautifulSoup(r1.content, "lxml")
        if count != 3:
            print('visiting {}'.format(value))
        get_info(movie, rows_deep, count, movies_visited)




'''
keep for testing:
def main():

    r = requests.get("http://www.imdb.com/title/tt0092099/")
    soup = BeautifulSoup(r.content, "lxml")

    rows_deep = 3
    count = 0
    movies_visited = []
    get_info(soup, rows_deep, count, movies_visited)

if __name__ == "__main__":
    main()
'''






