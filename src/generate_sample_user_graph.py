"""
This file generates a graph with users connected to restaurants they have visited
The graph is bipartite, where users are one partition and restaurants are the other
Weighted edges are fomred between users and restaurants, the weight being how much
they like a certain restaurant
"""
import random
import python_ta
import graph_container
import Constants


class Generate_Graph:
    """
    Class to generate different types of user - restaurant graphs
    """
    data_map: dict

    def __init__(self, data_map: dict) -> None:
        """
        Initialize a new class
        A data map should be passed, similar to one in main.usable_data
        """
        self.data_map = data_map

    def create_random_graph(self, user_size: int, rest_size: int) -> graph_container.Graph:
        """
        Creates a graph connecting a fixed size number of users
        to restaurants given in the data_map, similar to one created
        like main.usable_data

        Preconditions:
            - user_size > 10 and rest_size > 10
        """
        graph = graph_container.Graph()
        users = {i for i in range(user_size)}
        total_restaurants = list(self.data_map)
        restaurants = random.sample(total_restaurants, rest_size)

        # add vertices to the graph
        for restaurant in restaurants:
            graph.add_vertex(restaurant, Constants.RESTAURANT)
        for user in users:
            graph.add_vertex(user, Constants.USER)

        # give connections to the users
        # each user should have degree between 5 - 10
        for user in users:
            random_degree = random.randint(5, 10)
            to_connect = random.sample(sorted(restaurants), random_degree)
            for restaurant in to_connect:
                # generate random weight for edge
                # weight is in between 1 - 10
                weight = random.randint(1, 10)
                graph.add_edge(user, restaurant, weight)

        return graph

    def create_static_graph(self) -> graph_container.Graph:
        """
        Create a graph that takes in 10 users, and manually creates edges and vertices
        to 7 different restaurants
        """
        users = [i for i in range(10)]
        restaurants = list(self.data_map.keys())
        restaurants = restaurants[:7]
        graph = graph_container.Graph()

        # create vertices
        for i in users:
            graph.add_vertex(i, Constants.USER)
        for r in restaurants:
            graph.add_vertex(r, Constants.RESTAURANT)

        # create edges:
        r1 = restaurants[0]
        r2 = restaurants[1]
        r3 = restaurants[2]
        r4 = restaurants[3]
        r5 = restaurants[4]
        r6 = restaurants[5]
        r7 = restaurants[6]

        graph.add_edge(0, r1, 3)
        graph.add_edge(0, r4, 6)

        graph.add_edge(1, r7, 8)
        graph.add_edge(1, r2, 5)

        graph.add_edge(2, r3, 5)
        graph.add_edge(2, r5, 7)

        graph.add_edge(3, r4, 5)

        graph.add_edge(4, r5, 8)
        graph.add_edge(4, r7, 9)

        graph.add_edge(5, r5, 6)
        graph.add_edge(5, r6, 3)

        graph.add_edge(6, r2, 5)
        graph.add_edge(6, r6, 1)

        graph.add_edge(7, r6, 3)
        graph.add_edge(7, r7, 9)

        graph.add_edge(8, r7, 8)

        graph.add_edge(9, r7, 8)

        return graph


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['Constants', 'graph_container', 'random'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
