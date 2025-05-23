"""
This file handles reading the data and creating a graph from a raw csv file
"""
import csv
import sys
from dataclasses import dataclass
import python_ta
import Constants
from graph_container import Graph

csv.field_size_limit(sys.maxsize)


@dataclass
class Restaurant:
    """
    Data container to hold values of a given restaurant
    """
    online_order: bool
    book_table: bool
    rate: float
    location: str
    rest_type: list[str]
    cuisines: list[str]
    approx_cost: int
    listed_in: str


def select_valid_rows(input_file, num_rows=5000) -> dict[str, Restaurant]:
    """
    Given the large input file of data,
    select num_rows amount of lines to create a smaller subset of data.
    Use this smaller subset of data to return dictionary mapping restaurant name
    to its respective Restaurant dataclass.
    """
    # Read the original CSV file and store its rows
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        rows = list(reader)

    selected_rows = rows[:num_rows]
    created_dict = {}

    for row in selected_rows:
        name = row[2]
        online_order = row[3]
        book_table = row[4]
        rate = row[5]
        location = row[8]
        rest_type = row[9]
        cuisines = row[11]
        approx_cost = row[12]
        listed_in = row[15]

        # Flag to check if all the components are valid
        valid = True

        if not name or len(name) >= 30:
            valid = False
        if online_order and book_table in {"Yes", "No"}:
            if online_order == "Yes":
                online_order = True
            else:
                online_order = False

            if book_table == "Yes":
                book_table = True
            else:
                book_table = False
        if online_order and book_table not in {"Yes", "No"}:
            valid = False
        if "/" in rate:
            compute = rate.split("/")
            rate = round(float(compute[0]) / float(compute[1]), 2)
        elif "/" not in rate:
            valid = False
        elif not location or location == "":
            valid = False
        elif not rest_type or rest_type == "":
            valid = False
        elif not approx_cost or approx_cost == "":
            valid = False
        elif not listed_in or listed_in == "":
            valid = False

        if valid:
            try:
                if "," in approx_cost:
                    approx_cost = approx_cost.replace(",", "")
                    approx_cost = int(approx_cost)
                else:
                    approx_cost = int(approx_cost)

                rest_type = [item.strip() for item in rest_type.split(',')]
                cuisines = [item.strip() for item in cuisines.split(',')]

                restaurant = Restaurant(online_order, book_table, rate, location, rest_type,
                                        cuisines, approx_cost, listed_in)
                created_dict[name] = restaurant

            except ValueError:
                continue

    return created_dict


def create_graph(mapped_values: dict[str, Restaurant], weight_map: dict[str, int], graph: Graph) -> Graph:
    """
    Creates and returns a graph given the mapped_values mapping restaurant's name to its qualities.
    The weights are dynamically chosen by the user and given in the weight_map

    Preconditions:
        - len(weight_map) == 6
        - all([key in {'restaurant', 'location', 'rest_type', 'cuisines', 'approx_cost', 'other', 'user'}
                for key in weight_map])
    """

    for key in mapped_values:
        graph.add_vertex(key, Constants.RESTAURANT)
        rest_data = mapped_values[key]

        # add vertex for has online order and its corresponding edge
        if rest_data.online_order:
            graph.add_vertex("yes_online_order", Constants.OTHER)
            graph.add_edge(key, "yes_online_order")
        else:
            graph.add_vertex("no_online_order", Constants.OTHER)
            graph.add_edge(key, "no_online_order")

        # add vertex for has table booking
        if rest_data.book_table:
            graph.add_vertex("yes_book_table", Constants.OTHER)
            graph.add_edge(key, "yes_book_table")
        else:
            graph.add_vertex("no_book_table", Constants.OTHER)
            graph.add_edge(key, "no_book_table")

        # add vertex for restaurant's rating
        # split ratings into 5 sets, (0, 0.2) , (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.0)
        param = rest_data.rate
        if 0 <= param < 0.2:
            graph.add_vertex("worst_rated", Constants.OTHER)
            graph.add_edge(key, "worst_rated")
        elif 0.2 <= param < 0.4:
            graph.add_vertex("poor_rated", Constants.OTHER)
            graph.add_edge(key, "poor_rated")
        elif 0.4 <= param < 0.6:
            graph.add_vertex("moderate_rated", Constants.OTHER)
            graph.add_edge(key, "moderate_rated")
        elif 0.6 <= param < 0.8:
            graph.add_vertex("good_rated", Constants.OTHER)
            graph.add_edge(key, "good_rated")
        else:
            graph.add_vertex("excellent_rated", Constants.OTHER)
            graph.add_edge(key, "excellent_rated")

        # add vertex for restaurant's location
        graph.add_vertex(rest_data.location, Constants.LOCATION)
        graph.add_edge(key, rest_data.location, weight_map[Constants.LOCATION])

        # add vertices for rest_type
        for r_type in rest_data.rest_type:
            graph.add_vertex(r_type, Constants.REST_TYPE)
            graph.add_edge(key, r_type, weight_map[Constants.REST_TYPE])

        # add verticies for cuisine type
        for cuisine in rest_data.cuisines:
            graph.add_vertex(cuisine, Constants.CUISINES)
            graph.add_edge(key, cuisine, weight_map[Constants.CUISINES])

        # add vertex for restaurant's approx price
        # split ratings into 3 sets, (0, 750), (600, 2000), (2000, ...)
        price = rest_data.approx_cost
        if 0 <= price < 750:
            graph.add_vertex("low_cost", Constants.APPROX_COST)
            graph.add_edge(key, "low_cost", weight_map[Constants.APPROX_COST])
        elif 600 <= price < 2000:
            graph.add_vertex("medium_price", Constants.APPROX_COST)
            graph.add_edge(key, "medium_price", weight_map[Constants.APPROX_COST])
        else:
            graph.add_vertex("high_price", Constants.APPROX_COST)
            graph.add_edge(key, "high_price", weight_map[Constants.APPROX_COST])

        # add vertex and edge for listed_in
        graph.add_vertex(rest_data.listed_in, Constants.OTHER)
        graph.add_edge(key, rest_data.listed_in)

    return graph


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['csv', 'sys', 'dataclass', 'python_ta', 'Constants', 'Graph'],
        'allowed-io': ['select_random_rows'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
