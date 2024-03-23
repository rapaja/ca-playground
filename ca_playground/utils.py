import numpy as np
from PIL import Image, ImageDraw


def grid_to_image_1(grid, colors):
    image = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
    for i, c in enumerate(colors):
        image[:, :, 0] += ((grid == i) * c[0]).astype(np.uint8)  # Red channel
        image[:, :, 1] += ((grid == i) * c[1]).astype(np.uint8)  # Green channel
        image[:, :, 2] += ((grid == i) * c[2]).astype(np.uint8)  # Blue channel
    return image, "numpy"


def grid_to_image_2(grid, colors, image_size=500):
    colors = list(colors)
    # Create a new image with a white background
    image = Image.new("RGB", (image_size, image_size), "white")
    draw = ImageDraw.Draw(image)

    # Size of each square
    square_size_x = image_size // grid.shape[1]
    square_size_y = image_size // grid.shape[0]

    # Draw the squares
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            # Calculate the top left corner of the square
            top_left = (col * square_size_y, row * square_size_x)
            # Calculate the bottom right corner of the square
            bottom_right = ((col + 1) * square_size_y, (row + 1) * square_size_x)
            # If the sum of row and col is even, the square is white; if odd, it's black
            # if (row + col) % 2 == 0:
            #     color = "white"
            # else:
            #     color = "black"
            # Draw the rectangle
            draw.rectangle([top_left, bottom_right], fill=colors[grid[row, col]])

    # Draw the vertical lines of the grid
    for x in range(0, image_size, square_size_x):
        line = ((x, 0), (x, image_size))
        draw.line(line, fill="black")

    # Draw the horizontal lines of the grid
    for y in range(0, image_size, square_size_y):
        line = ((0, y), (image_size, y))
        draw.line(line, fill="black")

    # Draw border
    border_width = 2
    imgsz = image_size - 1
    draw.line(((0, 0), (0, imgsz)), fill="black", width=border_width)
    draw.line(((imgsz, 0), (imgsz, imgsz)), fill="black", width=border_width)
    draw.line(((0, 0), (imgsz, 0)), fill="black", width=border_width)
    draw.line(((0, imgsz), (imgsz, imgsz)), fill="black", width=border_width)

    return image, "pil"


grid_to_image = grid_to_image_2


def monochromatic_image(color, image_size=50, border_color="black", border_width=2):
    image = Image.new("RGB", (image_size, image_size), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        ((0, 0), (image_size - 1, image_size - 1)),
        fill=color,
        outline=border_color,
        width=border_width,
    )
    # image = np.zeros((10, 10, 3), dtype=np.uint8)
    # image[:, :, 0] = color[0]  # Red channel
    # image[:, :, 1] = color[1]  # Green channel
    # image[:, :, 2] = color[2]  # Blue channel
    return image
