from PIL import Image, ImageDraw, ImageFont

width = 512
height = 512
message = "Hello boss!"
font = ImageFont.truetype("arial.ttf", size=20)
img = Image.new('RGB', (width, height), color='blue')


imgDraw = ImageDraw.Draw(img)

textWidth, textHeight = imgDraw.textsize(message, font=font)
xText = (width - textWidth) / 2
yText = (height - textHeight) / 2

imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0))

img.save('imgs/result.png')