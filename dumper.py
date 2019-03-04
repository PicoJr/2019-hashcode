import logging


def dump(slides, output_file_path):
    nb = len(slides)
    logging.info("dumping %s", output_file_path)
    with open(output_file_path, 'w+') as output_file:
        output_file.write(str(nb)+'\n')
        for slide in slides:
            slide_txt = ' '.join(str(image_id) for image_id in slide)
            output_file.write(slide_txt+'\n')
    logging.info("dumping %s", output_file_path)
