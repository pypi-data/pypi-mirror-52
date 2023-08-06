"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Tuple

import matplotlib
matplotlib.use('Qt5Agg')  # https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths.weighted import dijkstra_path
import numpy
from scipy.misc import toimage

from pyjamas.rimage.rimutils import rimutils


# SHOULD THIS BE CALLED RImageOps and all methods be static (similar to PIL.ImageOps)
class rimage:
    """
    A class to do image operations.

    The image is stored as a numpy array (image_array).

    Because numpy arrays are accessed by row and col, all methods implemented here will use the row, col convention even to
    represent points.
    """

    image_extensions: Tuple[str] = ('.tif', '.tiff', '.jpg')

    def __init__(self, image_in):
        self.image_array:numpy.array = image_in

    # Return a tuple with all the points between thesrc and thedst. thesrc and thedst are in (r, c) format
    def livewire(self, thesrc, thedst, margin, xy=False):
        # Copy parameters. This is critical. I had a headache, because the function was modifying the parameter values.
        src = thesrc.copy()
        dst = thedst.copy()

        # Crop image. Note that image_array.shape returns size in (rows, columns) format. But src and dst are in (col=x, row=y) format.
        minr = max(0, min(src[0], dst[0]) - margin)
        maxr = min(self.image_array.shape[0] - 1, max(src[0], dst[0]) + margin) + 1
        minc = max(0, min(src[1], dst[1]) - margin)
        maxc = min(self.image_array.shape[1] - 1, max(src[1], dst[1]) + margin) + 1

        # Crop image.
        if self.image_array.ndim == 3:
            im = self.image_array[0, minr:maxr, minc:maxc].copy()
        else:
            im = self.image_array[minr:maxr, minc:maxc].copy()

        # Adjust source and destination coordinates.
        src[0] -= minr
        src[1] -= minc
        dst[0] -= minr
        dst[1] -= minc

        # Make sure the cropped image is a matrix and invert it so that high intensities become low ones, and we can
        # search for the minimal cost path.
        im[:] = numpy.max(im) - im[:]  # This modifies the array in place, which avoids having to reallocate the memory
        # (which is slow).
        # Doing im = numpy.max(im) - im produces the same result, but reallocates the memory.

        # Create graph.
        G = rimutils.makeGraphX(im)
        path = dijkstra_path(G, tuple(src), tuple(dst))

        # Generate coordinates.
        if xy:
            return [[c + minc, r + minr] for (r, c) in path]
        else:
            return [[r + minr, c + minc] for (r, c) in path]

    def stretch(self, low: int = 0, high: int = 100, minimum: int = 0, maximum: int = 255) -> numpy.ndarray:
        """
        Linear stretch of the contrast of an image.
        :param low: lower percentile of the image to be mapped to the minimum value (0)
        :param high: higher percentile (100)
        :param minimum: minimum pixel value in the resulting image (0)
        :param maximum: maximum pixel value (255)
        :return: image_out, an image array.

        Has a sister method in rimutils.
        """

        image_out: numpy.array = []

        if high == low:
            return self.image_array

        if low > high:
            high, low = low, high

        # Define output variable.
        image_out = self.image_array

        # Find the appropriate pixel values for the low and high thresholds.
        if low == 0:
            low = numpy.min(self.image_array)
        else:
            low = numpy.percentile(self.image_array, low)

        if high == 100:
            high = numpy.max(self.image_array)
        else:
            high = numpy.percentile(self.image_array, high)

        # Determine the scaling factor.
        sc = (maximum - minimum) / (high - low)

        # Linear stretch of image_in.
        if low != 0:
            image_out = image_out - low

        if sc != 1:
            image_out = image_out * sc

        if minimum != 0:
            image_out = image_out + minimum

        return image_out

    def show(self):
        plt.imshow(toimage(self.image_array))
        plt.show()

        return