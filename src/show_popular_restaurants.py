"""
Create the UI to show the popular restaurants
"""
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import python_ta
import main
import predict_from_data
import Constants
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


def compute_results() -> tuple[list[str], list[str]]:
    """
    Compute the most popular restaurants as chosen by users
    and the qualities that are common between the most popular restaurants
    """
    # initialize the data and the predictors
    user_rest_graph = main.create_user_graph()
    rest_graph = main.sample_graph
    user_predictor = predict_from_data.Similarity_Computations(user_rest_graph)
    rest_predictor = predict_from_data.Similarity_Computations(rest_graph)

    # find the top restaurants as chosen by users
    top_restaurants = user_predictor.compute_most_liked_restaurants(Constants.USER)

    # find what qualities the most popular restaurants have in common
    qualities = rest_predictor.find_similar_qualities(top_restaurants, Constants.RESTAURANT)

    return top_restaurants, qualities


def draw_results():
    """
    Draw the results computed by the above function
    """
    results = compute_results()

    # draw the most popular restaurants
    rests = results[0]
    factors = results[1]
    trending = [trending_1, trending_2, trending_3, trending_4, trending_5, trending_6, trending_7]
    for i in range(len(rests)):
        canvas.itemconfig(trending[i], text=rests[i])

    canvas.itemconfig(answer_one_text, text=factors[0])
    canvas.itemconfig(answer_two_text, text=factors[1])
    canvas.itemconfig(answer_three_text, text=factors[2])


canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_1 = canvas.create_image(
    540.0,
    360.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_2 = canvas.create_image(
    540.0,
    392.0,
    image=image_image_2
)

canvas.create_text(
    71.0,
    133.0,
    anchor="nw",
    text="Trending Restaurant",
    fill="#585078",
    font=("OpenSansRoman Bold", 24 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_3 = canvas.create_image(
    296.0,
    414.0,
    image=image_image_3
)

canvas.create_text(
    617.0,
    187.0,
    anchor="nw",
    text="Common Factors",
    fill="#736E8A",
    font=("OpenSansRoman Bold", 20 * -1)
)


image_image_4 = PhotoImage(
    file=relative_to_assets("image_14.png"))
image_4 = canvas.create_image(
    806.0,
    256.0,
    image=image_image_4
)


image_image_5 = PhotoImage(
    file=relative_to_assets("image_15.png"))
image_5 = canvas.create_image(
    806.0,
    367.0,
    image=image_image_5
)


image_image_6 = PhotoImage(
    file=relative_to_assets("image_16.png"))
image_6 = canvas.create_image(
    806.0,
    491.0,
    image=image_image_6
)

canvas.create_text(
    43.0,
    32.0,
    anchor="nw",
    text="Most Popular Restaurants in Bangalore By Users",
    fill="#342E2E",
    font=("OpenSansRoman Bold", 30 * -1)
)


# start ycoord at 214
# add 50 to each y coord

trending_1 = canvas.create_text(
    92.0,
    214.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_2 = canvas.create_text(
    92.0,
    264.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_3 = canvas.create_text(
    92.0,
    314.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_4 = canvas.create_text(
    92.0,
    364.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_5 = canvas.create_text(
    92.0,
    414.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_6 = canvas.create_text(
    92.0,
    464.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

trending_7 = canvas.create_text(
    92.0,
    514.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

answer_one_text = canvas.create_text(
    621.0,
    244.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

answer_two_text = canvas.create_text(
    621.0,
    355.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)

answer_three_text = canvas.create_text(
    621.0,
    478.0,
    anchor="nw",
    text="",
    fill="#B5B0CA",
    font=("OpenSansRoman Regular", 16 * -1)
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_11.png"))

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=draw_results,
    relief="flat"
)
button_1.place(
    x=611.0,
    y=577.0,
    width=390.0,
    height=50.0
)


def run_visual():
    """
    Run this file in a loop
    """
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    # python_ta.check_all(config={
    #     'extra-imports': ['Path', 'tkinter', 'main', 'predict_from_data', 'Constants'],
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })

    run_visual()
