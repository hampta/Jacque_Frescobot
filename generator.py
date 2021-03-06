from PIL import Image, ImageDraw, ImageFont
import textwrap

font = "TimesNewRomanPSMT.ttf"


def classic(self, text1, text2=''):
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
    src_file = Image.open(f'{self}')
    file_s1 = src_file.size[0] + 50
    file_s2 = src_file.size[1] + 50
    lines1 = textwrap.wrap(text1, width=src_file.size[0] // 18)
    lines2 = textwrap.wrap(text2, width=src_file.size[0] // 15)
    base = src_file.crop((-50, -50, src_file.size[0] + 50, src_file.size[1] + 20 + 35 * len(lines1) + 25 * len(lines2)))
    d = ImageDraw.Draw(base)
    d.rectangle((50, 50, file_s1, file_s2), fill=None, outline='white')
    for i in range(int(3)):
        d.rectangle((50 - i - 6, 50 - i - 6, file_s1 + i + 6, file_s2 + i + 6), fill=None, outline='white')
    fnt1 = ImageFont.truetype(font, size=40)
    fnt2 = ImageFont.truetype(font, size=24)
    h1, h2 = file_s2 + 5, file_s2 + 45 * len(lines1)
    for line in lines1:
        d.text((((base.width - d.textsize(line, fnt1)[0]) / 2), h1), line, font=fnt1)
        h1 += 35
    for line in lines2:
        d.text(((base.width - d.textsize(line, fnt2)[0]) / 2, h2), line, font=fnt2)
        h2 += 25
    base.save(f'{self}')
    return f'{self}'