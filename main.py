from PIL import Image

invert="Both"
image_file_path="puppy.jpg"
inverted_text_file="inverted.txt"
normal_text_file="normal.txt"
characters_per_pixel_width=2
characters_per_pixel_height=1



im = Image.open(image_file_path, 'r')
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))
gray_scale_map = {256: '▀', 254: '▀', 252: '▀', 250: 'Ѭ', 248: '₧', 246: '₧', 244: 'Ǆ', 242: 'Ǌ', 240: 'Ѡ', 238: 'Ѹ', 236: 'Ѽ', 234: '₨', 232: 'Ꜳ', 230: '▄', 228: 'ǋ', 226: 'ǅ', 224: 'Ŵ', 222: '₩', 220: 'ʥ', 218: 'Ҧ', 216: 'Ж', 214: '№', 212: '®', 210: 'ǆ', 208: '‰', 206: 'ǲ', 204: 'Μ', 202: 'ʤ', 200: 'Ԭ', 198: 'ǣ', 196: 'Ϣ', 194: 'ǳ', 192: 'œ', 190: 'ѹ', 188: 'æ', 186: 'ʣ', 184: 'ȹ', 182: 'Ǣ', 180: 'Œ', 178: 'Ȭ', 176: 'Ñ', 174: 'Ɋ', 172: 'Õ', 170: 'Æ', 168: 'Ô', 166: 'Ģ', 164: '¾', 162: 'Ó', 160: 'Ò', 158: 'Ö', 156: 'Ŝ', 154: '§', 152: '@', 150: 'Ś', 148: 'Ã', 146: '½', 144: '}', 142: '¼', 140: 'Ù', 138: 'Á', 136: 'À', 134: 'ã', 132: 'ß', 130: '¢', 128: 'õ', 126: 'ê', 124: 'à', 122: 'ø', 120: 'B', 118: '¥', 116: 'Q', 114: 'M', 112: '&', 110: '6', 108: '$', 106: 'G', 104: 'A', 102: 'W', 100: 'V', 98: 'Ē', 96: 'N', 94: '3', 92: 'Ė', 90: 'ü', 88: 'ċ', 86: 'Î', 84: 'm', 82: 'c', 80: '4', 78: 'Y', 76: 'l', 74: 'İ', 72: 'E', 70: 'Ĺ', 68: 'Ļ', 66: 'h', 64: '"', 62: '7', 60: '»', 58: ';', 56: '¡', 54: '>', 52: '²', 50: '‹', 48: 'L', 46: '¦', 44: 'ï', 42: 'ɨ', 40: 'ʟ', 38: 'ʲ', 36: 'ا', 34: 'ı', 32: '¬', 30: '¹', 28: '+', 26: 'ˮ', 24: '՝', 22: '`', 20: '_', 18: 'ʼ', 16: '-', 14: '.', 12: 'ʻ', 10: '̂', 8: '¨', 6: '˙', 4: 'ˑ', 2: '̇', 0: ' '}
gray_scale_list=list(gray_scale_map.values())
step_size = round(255 / len(gray_scale_list))

def round_to_number(number1,number2):
  rounded_number = round(number1 / number2) * number2
  return rounded_number

def to_file(ascii_conversion,invert):
  for x_list in range(0,len(ascii_conversion)):
    ascii_conversion[x_list]="".join(ascii_conversion[x_list])

  if invert=="True":
    file=inverted_text_file
  else:
    file=normal_text_file
  with open(file,"a+") as f:
    f.close()
  with open(file,"w",encoding="utf-8") as f:
    f.write("\n".join(ascii_conversion))

def generate_full(invert):
  global characters_per_pixel_height,characters_per_pixel_width
  if characters_per_pixel_width<1 or characters_per_pixel_height<1:
    return "Error: characters_per_pixel_width and characters_per_pixel_height can't be less than 1"
  if invert == "Both":
      generate_full("True")
      generate_full("False")
      return
  ascii_conversion = []
  for y_pixel in range(rgb_im.size[1]):  # Iterate over height first
      y_conversion = []
      for x_pixel in range(rgb_im.size[0]):  # Then iterate over width
          r, g, b = rgb_im.getpixel((x_pixel, y_pixel))
          average = (r + g + b) / 3
          closest_rgb = round_to_number(average, step_size)
          coro = gray_scale_map[closest_rgb]
          index = gray_scale_list.index(coro)
          if invert == "False":
              symbol = gray_scale_list[index * -1 if index != 0 else -1]
          elif invert == "True":
              symbol = coro
          pixel_x=symbol*characters_per_pixel_width
          y_conversion.append(pixel_x)

      ascii_conversion.append(y_conversion)
  
  final_list=[x_list for x_list in ascii_conversion for _ in range(characters_per_pixel_height)] if characters_per_pixel_height > 1 else ascii_conversion
  
  to_file(final_list, invert)
  return ascii_conversion


if characters_per_pixel_width%1==0 and characters_per_pixel_height%1==0:
  generate_full(invert)
else:
  print("Error: Make sure that characters_per_pixel values are greater than or equal to 1 and are integers.")
