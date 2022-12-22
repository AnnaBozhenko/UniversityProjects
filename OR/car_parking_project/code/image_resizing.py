from PIL import Image

def resize_image(image_name, new_length, new_image_name):
    with Image.open(image_name) as im:
        hpercent = (new_length / float(im.size[1]))
        wsize = int((float(im.size[0]) * float(hpercent)))
        im = im.resize((wsize, new_length), Image.ANTIALIAS)
        im.save(new_image_name)


def fit_image_to(new_width, new_length, image_name, new_image_name):
    get_greater_devisible_numenator = lambda numerator, denominator: ((numerator // denominator) + (numerator % denominator == 0)) * denominator
    with Image.open(image_name) as im:
        width, length = im.size

        if width <= new_width and length <= new_length:
            im = im.resize((new_width, new_length))
        elif width <= new_width and length >= new_length:
            length = get_greater_devisible_numenator(length, new_length)
            im = im.resize((new_width, length))
            im = im.reduce((1, int(length/new_length)))
        elif width >= new_width and length <= new_length:
            width = get_greater_devisible_numenator(width, new_width)
            im = im.resize((width, new_length))
            im = im.reduce((int(width/new_width), 1))
        else:
            width = get_greater_devisible_numenator(width, new_width)
            length = get_greater_devisible_numenator(length, new_length)
            im = im.resize((width, length))
            im = im.reduce((int(new_width/width), int(new_length/length)))
        print(im.size)
        im.save(new_image_name)
            
            
def crop_image(image_name, new_image_coords, new_image_name):
    with Image.open(image_name) as im:
        im = im.crop(new_image_coords)
        im.save(new_image_name)