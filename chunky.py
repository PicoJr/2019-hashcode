import logging
import itertools
from random import shuffle, seed
from multiprocessing import Pool

from image import Image
from solver import Solver

SEED = 1984
CHUNK_SIZE = 100


# shamelessly stolen from https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class ChunkySolver(Solver):
    def solve(self, images):
        seed(SEED)
        logging.debug('shuffling...')
        shuffle(images)
        logging.debug('shuffling...done')
        image_chunks = [chunk for chunk in chunks(images, CHUNK_SIZE)]
        pool = Pool(8)
        slides = pool.map(ChunkySolver.solve_chunk, image_chunks)
        return list(itertools.chain(*slides))

    @staticmethod
    def get_best_horizontal(tags_set, horizontals):
        best_score_h = -1
        best_horizontal = None
        for h in horizontals:
            score = Image.score_tags(tags_set, h.tags)
            if score > best_score_h:
                best_score_h = score
                best_horizontal = h
        return best_horizontal, best_score_h

    @staticmethod
    def get_best_vertical(tags_set, verticals):
        best_score_v = -1
        best_verticals = None
        for v0 in verticals:
            for v1 in verticals:
                if v0.image_id != v1.image_id:
                    score = Image.score_tags(tags_set, v0.tags | v1.tags)
                    if score > best_score_v:
                        best_score_v = score
                        best_verticals = v0, v1
        return best_verticals, best_score_v

    @staticmethod
    def solve_chunk(image_chunk):
        slides = []
        removed = set()

        verticals, horizontals = [], []
        for image in image_chunk:
            if image.orientation == 'H':
                horizontals.append(image)
            else:
                verticals.append(image)

        if horizontals:
            h0 = horizontals.pop()
            previous_slide_tags = h0.tags
            slides.append([h0])
            removed.add(h0.image_id)
        else:
            v0 = verticals.pop()
            v1 = verticals.pop()
            previous_slide_tags = v0.tags | v1.tags
            slides.append([v0, v1])
            removed.add(v0.image_id)
            removed.add(v1.image_id)

        while len(removed) < len(image_chunk):
            verticals = [img for img in verticals if img.image_id not in removed]
            horizontals = [img for img in horizontals if img.image_id not in removed]
            best_h, score_h = ChunkySolver.get_best_horizontal(previous_slide_tags, horizontals)
            best_v, score_v = ChunkySolver.get_best_vertical(previous_slide_tags, verticals)
            if score_h >= score_v and best_h is not None:
                removed.add(best_h.image_id)
                slides.append([best_h])
                previous_slide_tags = best_h.tags
            elif score_v >= score_h and best_v is not None:
                removed.add(best_v[0].image_id)
                removed.add(best_v[1].image_id)
                slides.append([*best_v])
                previous_slide_tags = best_v[0].tags | best_v[1].tags
            else:
                break
        return slides
