"""
Apply collaborative filtering to get recommendations for restaurant to restaurant
and user to user data
"""
import python_ta

from graph_container import Graph


class Similarity_Computations:
    """
    A class to handle the computations to give predictions
    """
    graph: Graph

    def __init__(self, graph: Graph):
        """
        Initialize new Similarity_Computations class with a given graph
        """
        self.graph = graph

    def generate_from_similarity_scores(self, item: str, kind: str) -> set[str]:
        """
        Return a set of top 20 restaurants most similar to the given one or user
        by finding their cosine similarities
        Precondition:
            - kind == Constants.RESTAURANT or kind == Constants.USER
        """
        if item not in self.graph.get_all_vertices(kind):
            raise ValueError

        accum_dict = {}
        accum_list = []
        connections = self.graph.get_all_vertices(kind)
        for connection in connections:
            sim = self.graph.get_similarity_score(item, connection)
            if connection == item:
                pass
            else:
                accum_dict[sim] = connection
                accum_list.append(sim)

        limit = min(20, len(accum_list))
        accum_list.sort(reverse=True)

        return {accum_dict[x] for x in accum_list[:limit]}

    def find_similar_restaurants(self, sim_list: list[set[str]], limit: int) -> list[str]:
        """
        Given a list of similar restaurant sets, find the ones that are most relevant
        To do this, we will take the intersection between the various sets given in the
        list and return it as it is the most overlapped restaurants.
        Return elements up to the given limit. If limit == -1, return all the elements

        If there is no intersection, return the restaurants from the first item of the sim_list

        Precondition:
            - len(sim_list) > 0
        """

        intersect = sim_list[0]
        for lst in sim_list[1:]:
            intersect = intersect.intersection(lst)

        intersect_lst = list(intersect)
        if len(intersect_lst) == 0:
            limit = min(limit, len(sim_list[0]))
            first_sim = list(sim_list[0])
            return list(first_sim[:limit])

        if limit == -1 or limit > len(intersect):
            return intersect_lst

        return intersect_lst[:limit]

    def find_similar_qualities(self, sim_list: list[str], kind: str) -> list[str]:
        """
        Return the qualities that are most similar between similar restaurants.
        To do this, we'll compute all of the factors of the given restaurants
        and check to see when their weights are summed, which 3 factors are most
        prevalent to the given restaurants.
        If the restaurants in sim_list are not in the graph, raise ValueError

        Precondition:
            - kind == Constants.RESTAURANT or kind == Constants.USER
        """
        all_restaurants = self.graph.get_all_vertices(kind)
        # initialize an empty dictionary to begin with
        sum_dict = {}

        # add the weights of the factors to the dictionary
        for rest in sim_list:
            if rest not in all_restaurants:
                raise ValueError

            factors = self.graph.get_neighbours(rest)
            for factor in factors:
                if factor in sum_dict:
                    sum_dict[factor] += self.graph.get_weight(factor, rest)
                else:
                    sum_dict[factor] = self.graph.get_weight(factor, rest)

        # get the top 3 factors by largest sum of weights
        sorted_dict = sorted(sum_dict)
        limit = min(3, len(sorted_dict))
        return sorted_dict[:limit]

    def compute_most_liked_restaurants(self, kind: str) -> list[str]:
        """
        This method will only work if it is being used for a graph with users
        connecting to restaurants. Compute the restaurants with the highest average
        weights and return the top 3 restaurants with that value.
        This gives the restaurants that most users like.
        Precondition:
            - kind == 'user'
        """
        rest_occurences = {}
        if kind != 'user':
            raise ValueError

        restaurants = self.graph.get_all_vertices("restaurant")
        for rest in restaurants:
            if rest in rest_occurences:
                pass
            else:
                # add the given restaurants average weight
                rest_occurences[rest] = self.graph.average_weight(rest)

        sorted_rest_occurences = sorted(rest_occurences)
        return sorted_rest_occurences[:7]


if __name__ == "__main__":
    python_ta.check_all(config={
        'extra-imports': ['graph_container'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
