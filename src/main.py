"""
This is the main file to run this project
"""

import create_usable_data
import graph_container
import generate_sample_user_graph

input_file = 'zomato.csv'
number_rows = 10000
usable_data = create_usable_data.select_valid_rows(input_file, number_rows)
graph = graph_container.Graph()

# this is a sample graph
wm = {'location': 9, 'rest_type': 8, 'cuisines': 4, 'approx_cost': 7}
g = graph_container.Graph()
sample_graph = create_usable_data.create_graph(usable_data, wm, g)


# creating graph helper functions
# comment one out so only one is working
# code to generate random graph:

def create_user_graph() -> graph_container.Graph:
    """
    Creates a random user graph
    """
    generator = generate_sample_user_graph.Generate_Graph(usable_data)
    user_rest_graph = generator.create_random_graph(50, 15)
    return user_rest_graph


# code to generate structured hard coded graph:

# def create_user_graph() -> graph_container.Graph:
#     """
#     create static graph
#     """
#     generator = generate_sample_user_graph.Generate_Graph(usable_data)
#     user_rest_graph = generator.create_static_graph()
#     return user_rest_graph


if __name__ == '__main__':
    # uncomment this to run the interface to show either interface
    # see report for more information

    # with open("show_popular_restaurants.py") as file:
    #     exec(file.read())

    with open("show_similar_restaurants.py") as file:
        exec(file.read())

    # Take a look at these restaurants, pick your top 3 that sound the most
    # appetizing to you. Try to copy paste this into the similar restaurants' predictor:

    # Farzi Cafe
    # Lotus Pavilion - ITC Gardenia
    # Royal Chef Naati Oota
    # Gundappa Donne Biryani
    # Bruncherz
    # Inhouse Burger

    # Play around with the importance factors and try to see if
    # different numbers give different predictions

    # there is a known bug where sometimes the text fields don't register a click
    # please be patient, maybe move the window around and force click the input field
    # and or the submit button
    # sometimes hitting the center of the field works best or use the tab key to navigate
