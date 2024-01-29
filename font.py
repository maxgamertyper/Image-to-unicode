from PIL import Image, ImageDraw, ImageFont
import math

all_extended_ascii_characters = [chr(i) for i in range(0x0021, 0x024F)] + [chr(i) for i in range(0x1E00, 0x1EFF)]
dicta = {}

def round_to_number(number1, number2):
    rounded_number = round(number1 / number2) * number2
    return rounded_number

def generate_image(letter, font_size=20):
    width = 30
    image = Image.new("RGB", (width, math.ceil(font_size/0.75)), color="white")

    draw = ImageDraw.Draw(image)

    # Use a basic font (adjust the path based on your font file)
    font = ImageFont.truetype("arial.ttf", font_size)

    text_height = 20/0.75
    text_width = draw.textlength(letter)

    draw.text((0, 0), letter, font=font, fill="black")
    image.save(f"Imageletter.png")
    pixel_count = 0
    for x_pixel in range(0, image.size[0]):
        for y_pixel in range(0, image.size[1]):
            r, g, b = image.getpixel((x_pixel, y_pixel))
            if r != 255 or g != 255 or b != 255:
                pixel_count += 1

    pixel_saturation = pixel_count / (text_width * text_height) if pixel_count != 0 else 0
    return pixel_saturation

def assemble_dict():

  for i in all_extended_ascii_characters:
      if i.isprintable():
          dicta[i] = generate_image(i, font_size=16)
  
  # Sort the dictionary based on values in descending order
  sorted_dicta = dict(sorted(dicta.items(), key=lambda item: item[1], reverse=True))
  
  # Create a new dictionary with the first occurrence of symbols with equal values
  final_dicta = {}
  used_values = set()  # Keep track of used values
  for symbol, value in sorted_dicta.items():
      if value not in used_values:
          final_dicta[value] = symbol
          used_values.add(value)
  
  rgb_dict = {i: {"difference":256,"symbol":""} for i in range(255, 0, -2)}
  rgb_dict[0]={"difference":256,"symbol":""}
  
  for value,symbol in final_dicta.items():
      value=value*255
      for key in rgb_dict.keys():
          if rgb_dict[key]["difference"]>abs(key-value):
              rgb_dict[key]["difference"]=abs(key-value)
              rgb_dict[key]["symbol"]=symbol
  
  for key in rgb_dict.keys():
      rgb_dict[key]=rgb_dict[key]["symbol"]
  
  return rgb_dict

print(assemble_dict())
#add more unicode characters for more accuracy/image quality