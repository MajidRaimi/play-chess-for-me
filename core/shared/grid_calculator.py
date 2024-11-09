from . import PerspectiveTransformer
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class GridCalculator:

    def __init__(self):
        pass

    @staticmethod
    def plot_grid_on_transformed_image(image, padding=30, output_path=None):
        corners = np.array([[padding, padding],
                            [image.size[0] - padding, padding],
                            [padding, image.size[1] - padding],
                            [image.size[0] - padding, image.size[1] - padding]])

        corners = PerspectiveTransformer.order_points(corners)
        TL, TR, BL, BR = corners[0], corners[1], corners[3], corners[2]

        def interpolate(xy0, xy1):
            x0, y0 = xy0
            x1, y1 = xy1
            dx, dy = (x1 - x0) / 8, (y1 - y0) / 8
            return [(x0 + i * dx, y0 + i * dy) for i in range(9)]

        ptsT = interpolate(TL, TR)
        ptsL = interpolate(TL, BL)

        if output_path:
            plt.figure(figsize=(10, 10))
            plt.imshow(image)
            for a, b in zip(ptsL, interpolate(TR, BR)):
                plt.plot([a[0], b[0]], [a[1], b[1]], 'ro', linestyle="--")
            for a, b in zip(ptsT, interpolate(BL, BR)):
                plt.plot([a[0], b[0]], [a[1], b[1]], 'ro', linestyle="--")
            plt.axis('off')
            plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
            plt.close()

        return ptsT, ptsL



