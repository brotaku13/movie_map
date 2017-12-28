from bs4 import BeautifulSoup
import requests
import networkx as nx
import time

def get_info(G, movie_link, rows_deep, count, movies_visited, parent_node):

    #  base case
    if(count == rows_deep):
        return

    movies = {}
    tt_code_list = []

    for links in movie_link.find_all("div", class_="rec_overview"):
        # find link
        link = links.find('a')  # relative hyperlink

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
    while visit < 3 and index > 0:  # visit 3 movies or the whole movies list, whichever comes first.
        if movies[sorted_movies[index]][1] not in movies_visited:

            # adding movies to top three list
            topThree[sorted_movies[index]] = movies[sorted_movies[index]]

            #adding new top three movies to list of movies already seen
            movies_visited.append(topThree[sorted_movies[index]][1])

            #visit only 3 movies
            visit += 1
        else:
            #if already in movies_visited list, then print. this is mostly a log function and will be removed later
            print('{} already visited'.format(movies[sorted_movies[index]][0]), end=', ')

        #  go backwards through the sorted movies to find top three
        index -= 1
    print('')

    #logging
    print('topThree:', topThree)

    count += 1  # increment count for recursive function

    #  going through top three
    for key, movie_specs in topThree.items():
        r1 = requests.get("http://www.imdb.com/title/" + movie_specs[1])
        movie = BeautifulSoup(r1.content, "lxml")
        if count != 3:  # logging
            print('visiting {}'.format(movie_specs))

        # build node
        G.add_node(movie_specs[1], title=movie_specs[0], votes=key, rating=movie_specs[2])
        #attach node to graph
        G.add_edge(parent_node, movie_specs[1])

        # call recursive function
        get_info(G, movie, rows_deep, count, movies_visited, movie_specs[1])  # passing in the tt_code as the parent_node

def create_parent_node(G, soup):
    '''
    This finds and creates the central, parent node and associates it with the graph
    :param G: networkx Graph object
    :param soup: beautiful_soup object
    :return: node_key (str)
    '''
    # insert actual web scraping for parent node
    G.add_node('tt0092099', title='Top Gun', votes=123456, imdb_score=7.9)
    return 'tt0092099'

# keep for testing:
def scraper():
    G = nx.Graph()
    r = requests.get("http://www.imdb.com/title/tt0092099/")
    soup = BeautifulSoup(r.content, "lxml")
    rows_deep = 3
    count = 0

    #  need to create a parent node
    #  Node(tt028365, 'title': 'original_title', 'votes', 123445, 'score', 7.0)
    parent_node_key = create_parent_node(G, soup)

    movies_visited = []
    get_info(G, soup, rows_deep, count, movies_visited, parent_node_key)

    return G
'''
if __name__ == "__main__":
    main()
'''








