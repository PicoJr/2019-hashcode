from solver import Solver


class DummySolver(Solver):
    def solve(self, images):
        slides = []
        verticals = []
        for image in images:
            if image.orientation == 'H':
                slides.append([image.image_id])
            else:  # V
                if verticals:
                    slides.append([verticals.pop(), image.image_id])
                else:
                    verticals.append(image.image_id)
        return slides
