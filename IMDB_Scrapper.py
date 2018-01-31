from bs4 import BeautifulSoup
import requests
import networkx as nx

def get_info(G, movie_link, rows_deep, count, movies_visited, parent_node, shells):
    '''
    This is the recursive function that goes into the different movies. it gets called on each movie.
    :param G: A graph object.
    :param movie_link: A beautiful soup object.
    :param rows_deep: the number of levels to go into. Note that As this becomes higher, the run time increases exponentially.
    :param count: the number of rows deep already visited.
    :param movies_visited: a list object of movie's tt_codes that have already been visited so that they are not visited again.
    :param parent_node: the parent node to the movies being visited. part of the Graph Object.
    :param shells: a list of lists where each sublist is a list of nodes at that concentric level. used to graph in the shell_layout
    :return: void. this function builds the graph object.
    '''

    #  base case
    if(count == rows_deep):
        return

    movies = {}
    tt_code_list = []

    try:
        for links in movie_link.find_all("div", class_="rec_overview"):
            # find link
            link = links.find('a')  # relative hyperlink

            # get ttcode
            tt_code = link.get('href').split('/')[2]
            #creates list of all ttCode of recommended movies
            tt_code_list.append(tt_code)

            # find title
            try:
                title = link.next_element['alt']
            except TypeError:
                title = 'Error Retrieving Title'
            print('currently scraping:', title)  # logging

            # find rating
            div = links.find('div', class_='rating rating-list')
            try:
                rating = float(div.attrs['id'].split('|')[2])
            except KeyError:
                rating = 5.0
            # find votes
            temp = div.attrs['title']

            # finds number between parentheses, replaces the ',' with '' and then turns the number into an int
            votes = int(temp[temp.find('(') + 1:temp.find(' ', temp.find('('))].replace(',', ''))

            # gets the short description of the movie
            try:
                synopsis = links.find("div", class_="rec-outline")
                synopsis = synopsis.find("p")
                synopsis = synopsis.string.replace("\n", "")
            except Exception as e:
                print(e, 'movie = {}, tt_code = {}'.format(title, tt_code))
                synopsis = "Error reading synopsis."
            # print(synopsis.text)

            # gets the year of the movie
            try:
                date = int(links.find("span", class_="nobr").text.replace('(', '').replace(')', ''))

            except:
                print("Error: Unable to find release date.")
                date = 0

            # gest all the recommended directors as a list
            try:
                all_rec_director = links.find("div", class_="rec-director rec-ellipsis").text.replace(',', '').split("\n")
                rec_director = []

                for i in range(2, len(all_rec_director)):
                    rec_director.append(all_rec_director[i].strip())

            except:
                print("Error: Unable to find recommended directors.")
                rec_director = "N/A"

            #adds information to a dictionary
            movies[votes] = [title, tt_code, rating, synopsis, date, rec_director]

    except:
        print("Error: Unable to find recommended movies.")

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

            # still want to create connection even if its been visited before
            G.add_edge(parent_node, movies[sorted_movies[index]][1])

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
        G.add_node(movie_specs[1], title=movie_specs[0], votes=key, rating=movie_specs[2], synopsis=movie_specs[3], release_date=movie_specs[4], director=movie_specs[5])

        shells[count].append(movie_specs[1]) # add the node to the current level of the graph's shell

        # attach node to graph
        G.add_edge(parent_node, movie_specs[1])

        # call recursive function
        get_info(G, movie, rows_deep, count, movies_visited, movie_specs[1], shells)  # passing in the tt_code as the parent_node


def create_parent_node(G, soup, movies_visited):
    '''
       This finds and creates the central, parent node and associates it with the graph
       :param G: networkx Graph object
       :param soup: beautiful_soup object
       :param movies_visited: a list of movies that have already been visited
       :return: node_key (str)
       '''

    # gets where most of the information is stored
    try:
        parent_info = soup.find("div", class_="imdbRating")

    except:
        print("Error: No imdbRating.")

    # gets the rating of the searched movie
    try:
        rating = parent_info.find("span", itemprop="ratingValue").text

    except:
        print("Error: Unable to get rating.")
        rating = 0

    # gets the tt code of the movie
    try:
        tt_code = parent_info.find("a").get("href").split('/')[2]

    except:
        print("Error: Unable to get tt_code.")
        tt_code = "N/A"

    # ges the rating count of the movie
    try:
        rating_count = parent_info.find("span", class_="small").text

    except:
        print("Error: Unable to get rating count.")
        rating_count = 0

    # gets the original title of the movie
    try:
        original_title = soup.find("div", class_="title_wrapper").find("h1").text

    except:
        print("Error: Unable to get original title.")
        original_title = "N/A"

    # gets the basic description of the movie
    summary_text = soup.find("div", class_="summary_text")

    try:
        summary_text = soup.find("div", class_="summary_text")
        summary_text = summary_text.string.replace("\n", "")
    except AttributeError:
        summary_text = 'Error Retrieving Information'

    print(summary_text)

    # gets the release date of the movie
    try:
        date = soup.find('a', title="See more release dates").text.split(' ')
        date = int(date[2])

    except:
        print("Error: Unable to get release date.")
        date = "N/A"

    # gets the director of the movie. so far i've only seen one director and would need to see a movie with multiple
    # directors in order to webscrape it
    parent_director = []
    try:
        parent_director.append(soup.find("span", itemprop="director").find('a').text)

    except:
        print("Error: Unable to find parent director.")
        parent_director.append("N/A")


    # creates the parent node for the graph and returns the tt code of the movie
    G.add_node(tt_code, title=original_title, votes=rating_count, rating=float(rating), synopsis=summary_text, release_date=date, director=parent_director)

    movies_visited.append(tt_code)

    return tt_code


def scraper(hyperlink, shells):
    '''
    This is the backbone of the webscaping. Starts by  creatinga  dummy graph, creating the
    parent node based off of the user movie input and then calls the recurvsive function to gather the
    rest of the data based of the recommended movies
    :param hyperlink: the name of the movie that the user entered
    :param shells: a list of lists that holds the nodes of the movies
    :return: by value of the network x graph
    '''
    try:
        G = nx.Graph()

        movies_visited = []

        # replaces the user entered spaces for + so that the movie can be searched for in imdb
        user_movie = hyperlink.replace(" ", "+")

        # get the link of the movie
        print(user_movie)
        movie_link = get_hyperlink(user_movie)
        print(movie_link)

        r = requests.get(movie_link)
        soup = BeautifulSoup(r.content, "lxml")

        # number of recursive levels. change this to creat larger or smaller graphs
        rows_deep = 3

        count = 0

    except:
        print("Error: Invalid input.")
        exit(0)

    try:
        # initialize the shell list with the number of sublists needed
        for i in range(rows_deep + 1):
            shells.append([])

        # parent node key is a tt_code (str)
        parent_node_key = create_parent_node(G, soup, movies_visited)

    except:
        print("Error: Unable to create parent node.")
        shells[0].append(parent_node_key)
        return G


    try:
        # set the origin node for the graph layout
        shells[0].append(parent_node_key)

        # call recursive function
        get_info(G, soup, rows_deep, count, movies_visited, parent_node_key, shells)

        return G

    except:
        print("Error: In the recursive function.")
        exit(0)

def get_hyperlink(movie_name):
    """
    Gets the link of the movie being searched for by the user
    :param movie_name: the movie to be searched for by the user
    :return: a hyperlink of the top movie that the user is searching for
    """

    try:

        temp_r = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + movie_name + "&s=all")
        temp_soup = BeautifulSoup(temp_r.content, "lxml")

        # in case the movie is not found right away it will look through all
        # the sections of the movie searched page and then look for the tt code once
        # in the right section of the page
        for item in temp_soup.find_all("div", class_="findSection"):
            link = item.find("a")
            link = link.get("name")

            if(link == "tt"):
                # finds the title with the most votes and sets that as the user entered movie
                # a precaution if there are tv shows and other stuff mixed in with movie titles

                all_movies = {}
                top = 0
                bad_title_count = 0

                # looks through all the titles in the right section and gets the link with the most votes
                for movie in item.find_all("td", class_="result_text"):
                    link = movie.find('a').get("href")
                    link = "http://www.imdb.com" + link
                    r = requests.get(link)
                    soup = BeautifulSoup(r.content, "lxml")
                    try:
                        votes = int(soup.find("span", itemprop="ratingCount").string.replace(',', ''))
                    except:
                        votes = bad_title_count
                        bad_title_count += 1

                    all_movies[votes] = link

                    if(top < votes):
                        top = votes

                return all_movies[top]

    except:
        # if the movie can not be found
        print("Error : Movie(" + movie_name + ") was not found.")
        exit(0)