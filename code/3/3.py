import os

from PIL import Image, ImageDraw, ImageFont


def get_position(image_width, image_height, text_width, text_height, position_id=9, margin=10):
    '''
    Get the position of the text by the position_id
    1: top left, 2: top center, 3: top right
    4: middle left, 5: middle center, 6: middle right
    7: bottom left, 8: bottom center, 9: bottom right
    :param image_width: image width
    :param image_height: image height
    :param text_width: text width
    :param text_height: text height
    :param position_id: position_id
    :param margin: the text position margin value to the image
    :return: text position tuple
    '''
    margin = 10
    if position_id == 1:
        return (margin, margin)
    elif position_id == 2:
        return (image_width // 2 - text_width // 2, margin)
    elif position_id == 3:
        return (image_width - text_width - margin, margin)
    elif position_id == 4:
        return (margin, image_height // 2 - text_height // 2)
    elif position_id == 5:
        return (image_width // 2 - text_width // 2, image_height // 2 - text_height // 2)
    elif position_id == 6:
        return (image_width - text_width - margin, image_height // 2 - text_height // 2)
    elif position_id == 7:
        return (margin, image_height - text_height - margin)
    elif position_id == 8:
        return (image_width // 2 - text_width // 2, image_height - text_height - margin)
    elif position_id == 9:
        return (image_width - text_width - margin, image_height - text_height - margin)


def add_watermark(filename, text, font_name='PMingLiU.ttf', font_size=20, font_opacity=50, position_id=9):
    '''
    Add watermark function
    :param filename: origin image filename
    :param text: watermark text
    :param font_name: Roboto-Italic.ttf, you can use your font, please make sure your program can find it
    :param font_size: font size, default is 20
    :param font_opacity: font opacity, default is 50
    :param position_id: position id, defalut is 9 (bottom right)
    :return:
    '''
    # get an image
    with Image.open(filename).convert("RGBA") as base:
        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype(font_name, font_size)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        # get the text widht and height
        text_width, text_height = d.textsize(text, font=fnt)
        # get the text position of the image
        pos = get_position(base.size[0], base.size[1], text_width, text_height, position_id=position_id)
        # draw text with opacity
        d.text(pos, text, font=fnt, fill=(255, 255, 255, 256 * font_opacity // 100))
        out = Image.alpha_composite(base, txt)

        # save the image file
        out_filename = 'watermark/{}'.format(os.path.basename(filename))
        if not os.path.exists('watermark'):
            os.makedirs('watermark')
        out.save(out_filename, 'PNG')


if __name__ == '__main__':
    text = input('Please input a watermark text: ').strip()
    font_size = int(input('Please input the font size: [20]') or '20')
    font_opacity = int(input('Please input the font opacity: [50]') or '50')
    # 1: top left, 2: top center, 3: top right
    # 4: middle left, 5: middle center, 6: middle right
    # 7: bottom left, 8: bottom center, 9: bottom right
    position_id = int(input('Please input the position: [9]') or '9')

    for f in os.listdir('images'):
        if f.endswith('.png'):
            filename = 'images/{}'.format(f)
            print('add watermark for {}'.format(filename))
            add_watermark(filename=filename, text=text, font_size=font_size, font_opacity=font_opacity,
                          position_id=position_id)
