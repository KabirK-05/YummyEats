"""
Create the UI for showing similar restaurants to the user's favourite restaurants
"""
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import python_ta
import main
import create_usable_data
import Constants
import graph_container
import predict_from_data
import os


working_path = os.getcwd()
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(working_path)
window = Tk()

window.geometry("1080x720")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1080,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)


def relative_to_assets(path: str) -> Path:
    """images to assets"""
    return ASSETS_PATH / Path(path)


def validate_input() -> bool:
    """
    Check if the input given in the text boxes are valid inputs
    """
    r_name = restaurant_name_entry.get()
    r1_name = restaurant1_name_entry.get()
    r2_name = restaurant2_name_entry.get()

    location = location_entry.get()
    price = price_entry.get()
    cuisine_type = cuisine_type_entry.get()
    restaurant_type = restaurant_type_entry.get()

    if r_name not in main.usable_data:
        return False
    if r1_name not in main.usable_data:
        return False
    if r2_name not in main.usable_data:
        return False
    try:
        location = int(location)
        price = int(price)
        cuisine_type = int(cuisine_type)
        restaurant_type = int(restaurant_type)
        if location < 0 or location > 10:
            return False
        if price < 0 or price > 10:
            return False
        if cuisine_type < 0 or cuisine_type > 10:
            return False
        if restaurant_type < 0 or restaurant_type > 10:
            return False
    except TypeError:
        return False

    return True


def create_graph() -> graph_container.Graph:
    """
    create a graph from the valid input
    """
    graph = main.graph
    location = int(location_entry.get())
    price = int(price_entry.get())
    cuisine_type = int(cuisine_type_entry.get())
    restaurant_type = int(restaurant_type_entry.get())
    weight_map = {Constants.LOCATION: location, Constants.APPROX_COST: price,
                  Constants.CUISINES: cuisine_type, Constants.REST_TYPE: restaurant_type}
    created = create_usable_data.create_graph(main.usable_data, weight_map, graph)
    return created


def compute_results() -> tuple[list[str], float, float, str]:
    """
    Computes the results and returns a tuple in order of:
    ([list of similar restaurants], avg_price, avg_rating, common_location)
    """

    # create the graph and predictor model
    graph = create_graph()
    predictor = predict_from_data.Similarity_Computations(graph)
    # compute up to 4 similar restaurants to display
    limit = 4

    # compute the restaurants obtained from similarity scores and get similar restaurants
    r1_sims = predictor.generate_from_similarity_scores(restaurant_name_entry.get(), Constants.RESTAURANT)
    r2_sims = predictor.generate_from_similarity_scores(restaurant1_name_entry.get(), Constants.RESTAURANT)
    r3_sims = predictor.generate_from_similarity_scores(restaurant2_name_entry.get(), Constants.RESTAURANT)
    prediction_list = [r1_sims, r2_sims, r3_sims]
    similar_restaurants = predictor.find_similar_restaurants(prediction_list, limit)
    limit = len(similar_restaurants)

    # compute the average price, average ratings, and most common location
    total_price = 0
    total_ratings = 0
    common_locations = {}

    for res in similar_restaurants:
        res_data = main.usable_data[res]

        total_price += res_data.approx_cost
        total_ratings += res_data.rate

        if res_data.location in common_locations:
            common_locations[res_data.location] += 1
        else:
            common_locations[res_data.location] = 1

    # get the averages and return them
    avg_price = total_price / limit
    avg_ratings = (total_ratings / limit) * 5
    common_locations = sorted(common_locations)
    common_locations = common_locations[0]
    return similar_restaurants, avg_price, avg_ratings, common_locations


def display_results():
    """
    display the results produced to the interface
    """
    # initalize the results
    results = compute_results()
    similar_restaurants = results[0]
    avg_price = str(results[1].__round__(1))
    avg_ratings = str(results[2].__round__(1))
    common_location = results[3]

    # draw the similar restaurant names
    canvas.itemconfig(rest1, text=similar_restaurants[0])
    canvas.itemconfig(rest2, text=similar_restaurants[1])
    canvas.itemconfig(rest3, text=similar_restaurants[2])
    canvas.itemconfig(rest4, text=similar_restaurants[3])

    canvas.itemconfig(answer_price_text, text=avg_price)
    canvas.itemconfig(answer_ratings_text, text=avg_ratings)
    canvas.itemconfig(answer_location_text, text=common_location)


def run_functions():
    """
    combines the functions above to get input and compute and display the output
    """
    valid = validate_input()
    if not valid:
        print("invalid input")
        pass
    else:
        display_results()


canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    540.0,
    360.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    290.0,
    392.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    810.0,
    392.0,
    image=image_image_3
)

canvas.create_text(
    71.0,
    133.0,
    anchor="nw",
    text="Name of restaurant you like",
    fill="#585078",
    font=("OpenSansRoman Bold", 24 * -1)
)

canvas.create_text(
    68.0,
    383.0,
    anchor="nw",
    text="Scale your priority from 1 - 10",
    fill="#585078",
    font=("OpenSansRoman Bold", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    292.0,
    211.0,
    image=entry_image_1
)
restaurant1_name_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
restaurant1_name_entry.place(
    x=97.0,
    y=186.0,
    width=390.0,
    height=48.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    292.0,
    271.0,
    image=entry_image_2
)
restaurant2_name_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
restaurant2_name_entry.place(
    x=97.0,
    y=246.0,
    width=390.0,
    height=48.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    292.0,
    331.0,
    image=entry_image_3
)
restaurant_name_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
restaurant_name_entry.place(
    x=97.0,
    y=306.0,
    width=390.0,
    height=48.0
)

canvas.create_text(
    608.0,
    133.0,
    anchor="nw",
    text="Name of similar restaurant",
    fill="#585078",
    font=("OpenSansRoman Bold", 24 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    812.0,
    286.0,
    image=image_image_4
)

canvas.create_text(
    627.0,
    418.0,
    anchor="nw",
    text="Average price",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    921.0,
    429.0,
    image=image_image_5
)

canvas.create_text(
    627.0,
    488.0,
    anchor="nw",
    text="Average ratings / 5",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    921.0,
    499.0,
    image=image_image_6
)

canvas.create_text(
    627.0,
    549.0,
    anchor="nw",
    text="Most common location",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    806.0,
    621.0,
    image=image_image_7
)


# This button handles majority of the processing required to display the results
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=run_functions,
    relief="flat"
)
button_1.place(
    x=77.0,
    y=596.0,
    width=430.0,
    height=50.0
)


canvas.create_text(
    43.0,
    32.0,
    anchor="nw",
    text="Recommendation on Restaurant Types for New Store in Bangalore",
    fill="#342E2E",
    font=("OpenSansRoman Bold", 30 * -1)
)



rest1 = canvas.create_text(
    638.0,
    200,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

rest2 = canvas.create_text(
    638.0,
    250,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

rest3 = canvas.create_text(
    638.0,
    300,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

rest4 = canvas.create_text(
    638.0,
    350,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

answer_price_text = canvas.create_text(
    856.0,
    417.0,
    anchor="nw",
    text="average price",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)


answer_ratings_text = canvas.create_text(
    856.0,
    487.0,
    anchor="nw",
    text="average ratings",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)


answer_location_text = canvas.create_text(
    627.0,
    608.0,
    anchor="nw",
    text="common location",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)


canvas.create_text(
    68.0,
    458.0,
    anchor="nw",
    text="Location",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    207.0,
    469.0,
    image=entry_image_4
)
location_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
location_entry.place(
    x=182.0,
    y=444.0,
    width=50.0,
    height=48.0
)

canvas.create_text(
    261.0,
    528.0,
    anchor="nw",
    text="Restaurant type",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    207.0,
    539.0,
    image=entry_image_5
)
price_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
price_entry.place(
    x=182.0,
    y=514.0,
    width=50.0,
    height=48.0
)

canvas.create_text(
    261.0,
    458.0,
    anchor="nw",
    text="Cuisine type",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    474.0,
    469.0,
    image=entry_image_6
)
cuisine_type_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
cuisine_type_entry.place(
    x=449.0,
    y=444.0,
    width=50.0,
    height=48.0
)

canvas.create_text(
    68.0,
    528.0,
    anchor="nw",
    text="Price",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    474.0,
    539.0,
    image=entry_image_7
)
restaurant_type_entry = Entry(
    bd=0,
    bg="#FFFCFC",
    fg="#000716",
    highlightthickness=0
)
restaurant_type_entry.place(
    x=449.0,
    y=514.0,
    width=50.0,
    height=48.0
)


def run_visual():
    """
    Run this file in a loop
    """
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    # python_ta.check_all(config={
    #     'extra-imports': ['Path', 'tkinter', 'main', 'predict_from_data', 'Constants',
    #                       'create_usable_data', 'graph_container'],
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })

    run_visual()
