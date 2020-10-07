from PIL import Image, ImageDraw
sizeX = 200
sizeY = 200

image = Image.new("1", (sizeX,sizeY), color='black')
draw = ImageDraw.Draw(image)

for i in range(round(sizeY/8)+1):
    y = 8*i
    for j in range(round(sizeX/8)+1):
        x = 8*j
        if j > 0 and i > 0:
            draw.rectangle((x-2, y-2, x+1, y+1), fill='black')
            draw.rectangle((x-6, y-6, x-2, y-3), fill='white')

image.show()
image.save("test.bmp", "bmp")


