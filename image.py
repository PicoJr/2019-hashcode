class Image(object):
    def __init__(self, image_id, orientation, tags):
        self.image_id = image_id
        self.orientation = orientation
        self.tags = set(tags)

    def __str__(self):
        return str(self.image_id)

    @staticmethod
    def score(images):
        """
        :param images: [VVVV] | [HVV] | [VVH] | [HH]
        :return: score
        """
        if not 1 < len(images) <= 4:
            raise AssertionError()
        orientations = ''.join(img.orientation for img in images)
        if orientations == 'VVVV':
            tags_set = images[0].tags | images[1].tags
            other_tags_set = images[2].tags | images[3].tags
        elif orientations == 'HVV':
            tags_set = images[0].tags
            other_tags_set = images[1].tags | images[2].tags
        elif orientations == 'VVH':
            tags_set = images[0].tags | images[1].tags
            other_tags_set = images[2].tags
        else:  # 'HH'
            if orientations != "HH":
                raise AssertionError()
            tags_set = images[0].tags
            other_tags_set = images[1].tags
        return Image.score_tags(tags_set, other_tags_set)

    @staticmethod
    def score_tags(tags_set, other_tags_set):
        return min(len(tags_set - other_tags_set), len(other_tags_set - tags_set), len(tags_set & other_tags_set))

