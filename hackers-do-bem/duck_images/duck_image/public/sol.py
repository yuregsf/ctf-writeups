import sys
from PIL import Image
flag = sys.argv[1]

old_image = Image.open("./in.png").convert("RGB")
width, height = old_image.size
print(width, height)
new_image = Image.new("RGB", (width, height))
old_matrix = old_image.load()
new_matrix = new_image.load()
for i in range(width):
    for j in range(height):
        new_matrix[(i, j)] = old_matrix[(i, j)]
    else:
        enc(old_matrix, new_matrix, flag)
        new_image.save("./out.png")
        old_image.close()
        new_image.close()
        print("done!")
