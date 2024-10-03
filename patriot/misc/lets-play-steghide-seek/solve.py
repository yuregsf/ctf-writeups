import cv2
import math
from qrtools import qrtools

def divide_image(image_path, num_parts):
    # Read the image
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_RGB2GRAY)

    # Get the dimensions of the image
    height, width = image.shape

    # Calculate the number of parts per dimension
    parts_per_dimension = int(math.sqrt(num_parts))
    while num_parts % parts_per_dimension != 0:
        parts_per_dimension -= 1

    # Calculate the dimensions of each part
    part_height = height // parts_per_dimension
    part_width = width // (num_parts // parts_per_dimension)

    # Divide the image into parts
    parts = []
    for i in range(parts_per_dimension):
        for j in range(num_parts // parts_per_dimension):
            part = image[i * part_height: (i + 1) * part_height, j * part_width: (j + 1) * part_width]
            parts.append(part)

    return parts

chunks = divide_image('qr_mosaic.bmp', 40*25)
for i in range(len(chunks)):
    cv2.imwrite(f'chunk_{i}.bmp', chunks[i])

a = ''

q = qrtools.QR()

for chunk in chunks:
    r = qr.decode(chunk)
    print(r.data)
