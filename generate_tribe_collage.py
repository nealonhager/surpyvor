import os
from PIL import Image


def image_grid(imgs, rows, cols):
    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


def main():
    # Get all the images from images.py
    image_list = [
        f"images/{filename}"
        for filename in os.listdir("images")
        if filename.endswith(".png")
    ]
    image_list = [Image.open(image_url) for image_url in image_list]

    # generate a png of image_list in  a grid where each image is 500x500 px
    image_grid(image_list, 4, 5).save("grid.png")


if __name__ == "__main__":
    main()
