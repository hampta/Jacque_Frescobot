from PIL import Image, ImageDraw, ImageFont
import textwrap

font = "TimesNewRomanPSMT.ttf"
TOP_BORDER = 40
BOTTOM_BORDER = 20
LEFT_BORDER = 40
RIGHT_BORDER = 40
BIG_FONT_SIZE = 48
SMALL_FONT_SIZE = 16
BG_COLOR = "#010101"

def classic(self, text1, text2=""):
    lines1 = textwrap.wrap(text1, width=30)
    lines2 = textwrap.wrap(text2, width=45)
    src_file = Image.open(f'{self}')
    base = Image.new('RGB', (640, 430 + 35 * len(lines1) + 25 * len(lines2)))
    base.paste(src_file.resize((555, 370), Image.LANCZOS), (43, 25))
    d = ImageDraw.Draw(base)
    d.rectangle((43, 25, 598, 395), fill=None, outline='white')
    for i in range(int(3)):
        d.rectangle((43 - i - 6, 25 - i - 6, 598 + i + 6, 395 + i + 6), fill=None, outline='white')
    fnt1 = ImageFont.truetype(font, size=40)
    fnt2 = ImageFont.truetype(font, size=24)
    h1, h2 = 405, 420 + 35 * len(lines1)
    for line in lines1:
        d.text((((base.width - d.textsize(line, fnt1)[0]) / 2), h1), line, font=fnt1)
        h1 += 35
    for line in lines2:
        d.text(((base.width - d.textsize(line, fnt2)[0]) / 2, h2), line, font=fnt2)
        h2 += 25
    base.save(f'{self}')
    return f'{self}'


def auto(self, text1, text2=''):
    # Loading fonts
    big_font = ImageFont.truetype("TimesNewRomanPSMT.ttf", BIG_FONT_SIZE)
    big_font_size = big_font.getsize(text1)
    small_font = ImageFont.truetype("TimesNewRomanPSMT.ttf", SMALL_FONT_SIZE)
    small_font_size = small_font.getsize(text2)
    # Calculating size of demotivator
    src_img = Image.open(f'{self}')
    src_size = src_img.getbbox()[2:]
    dst_size = list(src_size)
    dst_size[0] += LEFT_BORDER + RIGHT_BORDER
    dst_size[1] += TOP_BORDER + BOTTOM_BORDER + \
                   big_font_size[1] + small_font_size[1] + 5
    # Making border
    dst_img = Image.new("RGB", dst_size, "black")
    dst_draw = ImageDraw.Draw(dst_img)
    dst_draw.rectangle([0, 0, dst_size[0], dst_size[1]], fill=BG_COLOR)
    dst_img.paste(src_img, (LEFT_BORDER, TOP_BORDER))
    # Drawing border lines
    dst_draw.line(
        (LEFT_BORDER - 3, TOP_BORDER - 3,
         dst_size[0] - RIGHT_BORDER + 3, TOP_BORDER - 3),
        width=1)
    dst_draw.line(
        (dst_size[0] - RIGHT_BORDER + 3, TOP_BORDER - 3,
         dst_size[0] - RIGHT_BORDER + 3, TOP_BORDER + src_size[1] + 3),
        width=1)
    dst_draw.line(
        (LEFT_BORDER - 3, TOP_BORDER + src_size[1] + 3,
         dst_size[0] - RIGHT_BORDER + 3, TOP_BORDER + src_size[1] + 3),
        width=1)
    dst_draw.line(
        (LEFT_BORDER - 3, TOP_BORDER + src_size[1] + 3,
         LEFT_BORDER - 3, TOP_BORDER - 3),
        width=1)
    # Drawing text
    text_pos_x = (dst_size[0] - big_font_size[0]) / 2
    text_pos_y = src_img.getbbox()[3] + TOP_BORDER + 5
    dst_draw.text((text_pos_x, text_pos_y), text1, font=big_font)
    text_pos_x = (dst_size[0] - small_font_size[0]) / 2
    text_pos_y += big_font_size[1] + 5
    dst_draw.text((text_pos_x, text_pos_y), text2, font=small_font)
    # Saving and showing image
    dst_img.save(f'{self}')
    return f'{self}'
