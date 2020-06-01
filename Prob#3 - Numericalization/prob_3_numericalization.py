from typing import Tuple
from typing import List
import math


class PixelArray:
    """ Represent 2d array of pixel element that can be display on the terminal """
    DIR_UP = (-1, 0)
    DIR_DOWN = (1, 0)
    DIR_LEFT = (0, -1)
    DIR_RIGHT = (0, 1)

    def __init__(self, width: int, height: int, initial_pixel_value=' '):
        """ Initialize PixelArray
        Args:
            width (int): width of 2d array or column length
            height (int): height of 2d array or row length
            initial_pixel_value: default value for each cell of array
        """
        self.width = width
        self.height = height
        self._pixel_array = [[str(initial_pixel_value)
                              for j in range(width)] for i in range(height)]

    def get_array(self) -> List[List]:
        """ Return 2d array that represent pixel matrix """
        return self._pixel_array

    def line(self, i: int, j: int, length: int, direction: Tuple[int], pixel_value):
        """ Draw a line on the pixel array
        Args:
            i (int): row coordinate
            j (int): column coordinate
            length (int): length of the line to be drawn
            direction (Tupple[int]): ordered pair of direction of the line
            pixel_value: value to be set
        """
        if not self.range_check(i, j):
            return
        # move corrdinate by "length" times
        for _ in range(length):
            # set pixel
            self.set_pixel(i, j, pixel_value)
            # update coordinate
            i += direction[0]
            j += direction[1]

    def set_pixel(self, i: int, j: int, pixel_value):
        """ Set value for given pixel

        Args:
            i (int): row coordinate
            j (int): column coordinate
            pixel_value: value to be set
        """
        if not self.range_check(i, j):
            return
        self._pixel_array[i][j] = pixel_value

    def range_check(self, i: int, j: int) -> bool:
        """ Check if given coordinate is within current pixel array

        Args:
            i (int): row coordinate
            j (int): column coordinate

        Returns:
            bool: True if given coordinate is within current pixel array, otherwise False
        """
        return i >= 0 and i < self.height and j >= 0 and j < self.width

    def __str__(self):
        """ Convert pixel array to string representation """
        result = ''
        # for each row
        for i in range(self.height):
            # for each column
            for j in range(self.width):
                # append character
                result += str(self._pixel_array[i][j])
            result += '\n'
        return result


def main():
    pass


if __name__ == '__main__':
    main()
