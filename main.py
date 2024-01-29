from PIL import Image

invert="True"

im = Image.open('monalisa.jpg', 'r')
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))





gray_scale_map = {256: 'Ǆ', 254: 'Ǆ', 252: 'Ǆ', 250: 'Ǆ', 248: 'Ǆ', 246: 'Ǆ', 244: 'Ǆ', 242: 'Ǌ', 240: 'Ǌ', 238: 'Ǌ', 236: 'Ǌ', 234: 'ǋ', 232: 'ǋ', 230: 'ǋ', 228: 'ǋ', 226: 'ǅ', 224: 'Ŵ', 222: 'Ŵ', 220: 'Ẁ', 218: 'Ẁ', 216: 'Ḿ', 214: '®', 212: '®', 210: 'ǆ', 208: 'ǲ', 206: 'ǲ', 204: 'ǲ', 202: 'ǣ', 200: 'ǣ', 198: 'ǣ', 196: 'Ø', 194: 'ǳ', 192: 'œ', 190: 'œ', 188: 'æ', 186: 'æ', 184: 'ȹ', 182: 'Ǣ', 180: 'Œ', 178: 'Ȭ', 176: 'Ñ', 174: 'Ɋ', 172: 'Õ', 170: 'Æ', 168: 'Ô', 166: 'Ģ', 164: '¾', 162: 'Ó', 160: 'Ò', 158: 'Ö', 156: 'Ŝ', 154: '§', 152: '@', 150: 'Ś', 148: 'Ã', 146: '½', 144: '}', 142: '¼', 140: 'Ù', 138: 'Á', 136: 'À', 134: 'ã', 132: 'ß', 130: '¢', 128: 'õ', 126: 'ê', 124: 'à', 122: 'ø', 120: 'B', 118: '¥', 116: 'Q', 114: 'M', 112: '&', 110: '6', 108: '$', 106: 'G', 104: 'A', 102: 'W', 100: 'V', 98: 'Ē', 96: 'N', 94: '3', 92: 'Ė', 90: 'ü', 88: 'ċ', 86: 'Î', 84: 'm', 82: 'c', 80: '4', 78: 'Y', 76: 'l', 74: 'İ', 72: 'E', 70: 'Ĺ', 68: 'Ļ', 66: 'h', 64: '"', 62: '7', 60: '»', 58: ';', 56: '¡', 54: '>', 52: '²', 50: 'ƚ', 48: 'L', 46: '¦', 44: 'ï', 42: ',', 40: ',', 38: 'ı', 36: 'ı', 34: 'ı', 32: '¬', 30: '¹', 28: '+', 26: '+', 24: '¸', 22: '`', 20: '_', 18: '_', 16: '-', 14: '.', 12: '.', 10: '¨', 8: '¨', 6: '¨', 4: '¨', 2: '¨', 0: '¨'}
gray_scale_list=list(gray_scale_map.values())
step_size = round(255 / len(gray_scale_list))

def round_to_number(number1,number2):
  rounded_number = round(number1 / number2) * number2
  return rounded_number

def to_file(ascii_conversion,invert):
  for x_list in range(0,len(ascii_conversion)):
    ascii_conversion[x_list]="".join(ascii_conversion[x_list])

  if invert=="True":
    file="invert.txt"
  else:
    file="normal.txt"
  with open(file,"w",encoding="utf-8") as f:
    f.write("\n".join(ascii_conversion))

def generate(invert):
  if invert == "Both":
      generate("True")
      generate("False")
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
              inverted = gray_scale_list[index * -1 if index != 0 else -1]
          elif invert == "True":
              inverted = coro
          y_conversion.append(inverted)

      ascii_conversion.append(y_conversion)
  to_file(ascii_conversion, invert)
  return ascii_conversion



generate("Both")

# add image conversion to gray-scale
# make code better