import logging

from image import Image


def parse(input_file_path):
    """
    Parse input file
    :param input_file_path: input file path
    :return: Image list
    """
    verticals, horizontals = 0, 0
    logging.info("parsing %s", input_file_path)
    with open(input_file_path, 'r') as input_file:
        nb = int(input_file.readline())  # images nb
        images = []
        for i, img_txt in enumerate(input_file.readlines()):
            data = img_txt.rstrip().split(' ')
            orientation = data[0]
            tags = data[2:]
            images.append(Image(i, orientation, set(tags)))
            if orientation == 'V':
                verticals += 1
            else:  # H
                horizontals += 1
        logging.info('parsing %s done', input_file_path)
        logging.info('%d images found (%d V,%d H)', nb, verticals, horizontals)
        return images
