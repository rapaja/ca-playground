import numpy as np
import time

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as image_coordinates
from streamlit_extras.row import row as ste_row

from PIL import Image, ImageDraw

from ca_playground.utils import grid_to_image, monochromatic_image
from ca_playground.basic_ca import game_of_life
from ca_playground.gos import game_of_schools

WIDTH = 400
HEIGHT = 400


GAMES = {
    "Conway's Game of Life": {
        "states": {"dead": (255, 255, 255), "alive": (11, 102, 35)},
        "stf": game_of_life,
    },
    "Deki's Game of Schools": {
        "states": {
            "outdoor": (255, 255, 255),
            "corridor": (50, 50, 50),
            "primary": (80, 133, 188),
            "support": (255, 174, 66),
        },
        "stf": game_of_schools,
    },
}

# Streamlit UI
st.title("CA Playground")

# Sidebar options
game = st.sidebar.selectbox("Choose game:", list(GAMES.keys()))
reset_button = st.sidebar.button("Randomize")
clear_button = st.sidebar.button("Clear")
step_button = st.sidebar.button("Step")
play = st.sidebar.button("Play/Pause")
grid_size = st.sidebar.slider(
    "Grid size (randomize or clear to change size)",
    min_value=5,
    max_value=100,
    value=50,
)

# Calculated properties
pixel_size_w = WIDTH / grid_size
pixel_size_h = HEIGHT / grid_size
game = GAMES[game]
colors = game["states"].values()

# Initialize or reset the grid
if "grid" not in st.session_state or reset_button:
    st.session_state.grid = np.random.choice(
        list(range(len(game["states"]))), size=(grid_size, grid_size)
    )

if clear_button:
    st.session_state.grid = np.zeros(shape=(grid_size, grid_size), dtype=np.uint32)

# Grid and Legend
col1, col2 = st.columns([3, 1])

with col1:
    # Draw grid
    image, key = grid_to_image(st.session_state.grid, colors)
    click_pos = image_coordinates(
        image,
        height=HEIGHT,
        width=WIDTH,
        key=key,
    )
    click_action = st.selectbox(
        "On mouse click, change cell to",
        ["next state (cycle through)"] + list(game["states"].keys()),
    )

with col2:
    # Draw legend
    for key, color in game["states"].items():
        row = ste_row(2)
        row.text(key)
        row.image(monochromatic_image(color), width=15)

# Capture mouse click position on the grid
if "click_pos" not in st.session_state:
    st.session_state.click_pos = click_pos

if click_pos is not None and not (click_pos == st.session_state.click_pos):
    x = click_pos["x"]
    y = click_pos["y"]
    c = int(x / pixel_size_w)
    r = int(y / pixel_size_h)
    if click_action == "next state (cycle through)":
        st.session_state.grid[r][c] = (st.session_state.grid[r][c] + 1) % len(
            game["states"]
        )
    else:
        st.session_state.grid[r][c] = list(game["states"].keys()).index(click_action)
    st.session_state.click_pos = click_pos
    st.rerun()

# One step update
if step_button:
    st.session_state.grid = game["stf"](st.session_state.grid)
    st.rerun()

# Auto-play/pause functionality
if play:
    if "play_state" not in st.session_state:
        st.session_state.play_state = True
    else:
        st.session_state.play_state = not st.session_state.play_state

# if st.session_state.get("play_state", False):
while st.session_state.get("play_state", False):
    st.session_state.grid = game["stf"](st.session_state.grid)
    time.sleep(0.1)
    st.rerun()
