import numpy as np
from PIL import Image

bayer_matrix_4x4 = np.array([[0, 8, 2, 10],
                             [12, 4, 14, 6],
                             [3, 11, 10, 1],
                             [5, 13, 12, 5]])


def dither_image(image_path):
    # Load the image
    image_pre = Image.open(image_path).convert("L")
    width_pre, height_pre = image_pre.size
    image = image_pre.resize((int(width_pre*0.2), int(height_pre*0.2)))
    width, height = image.size

    # Create a blank dithered image with the same size as the original image
    dithered_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            # Get the original grayscale pixel value
            orig_color = image.getpixel((x, y))

            # Calculate the dithering threshold
            threshold = bayer_matrix_4x4[y % 4, x % 4]

            # Apply dithering
            dithered_color = 0 if orig_color < threshold*16 else int(255-threshold)

            # Set the dithered pixel value in the new image
            dithered_image.putpixel((x, y), dithered_color)

    return dithered_image

# Example usage
input_image_path = "cats.jpg"
output_image_path = "catsout.jpg"
dithered_image = dither_image(input_image_path)
dithered_image.save(output_image_path)