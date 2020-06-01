from typing import Tuple
from typing import List
from typing import Union
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


class Digit(PixelArray):
    """ Represent digit display (like seven segment display) in pixel array """
    _DIGIT_CONFIG = {
        0: {'top', 'bot', 'top_left', 'top_right', 'bot_left', 'bot_right'},
        1: {'top_right', 'bot_right'},
        2: {'top', 'mid', 'bot', 'top_right', 'bot_left'},
        3: {'top', 'mid', 'bot', 'top_right', 'bot_right'},
        4: {'mid', 'top_left', 'top_right', 'bot_right'},
        5: {'top', 'mid', 'bot', 'top_left', 'bot_right'},
        6: {'top', 'mid', 'bot', 'top_left', 'bot_left', 'bot_right'},
        7: {'top', 'top_right', 'bot_right'},
        8: {'top', 'mid', 'bot', 'top_left', 'top_right', 'bot_left', 'bot_right'},
        9: {'top', 'mid', 'bot', 'top_left', 'top_right', 'bot_right'}
    }  # Contains instruction how to draw a line for each digit

    def __init__(self, digit: Union[int,str], mag_vert: int = 1, mag_horiz: int = 1):
        """ Initialize digit display
        Args:
            digit (Union[int,str]): single number
            mag_vert (int): vertical magification ratio 
            mag_horiz (int): horizontal magification ratio 
        """
        super().__init__(5*mag_horiz, 5*mag_vert, ' ')
        self.digit = int(digit)
        self.mag_vert = mag_vert
        self.mag_horiz = mag_horiz
        # render
        self.render()

    def render(self):
        """ Render a digit onto pixel array """
        for location in self._DIGIT_CONFIG[self.digit]:
            self._draw_line_segment(location)

    def _draw_line_segment(self, location: str):
        """ Draw a line in different location on the display

        Args:
            location (str): a string of location
        """
        # Horizontal line
        if location == 'top' or location == 'mid' or location == 'bot':
            # determine starting row position
            if location == 'top': 
                row = 0
            elif location == 'mid': 
                row = self.mag_vert*2
            elif location == 'bot': 
                row = self.mag_vert*4
            # draw according to magification ratio
            for offset in range(self.mag_vert):
                self.line(row + offset, 0, self.width,
                          PixelArray.DIR_RIGHT, self.digit)
        # Vertical line
        elif location == 'top_left' or location == 'top_right' or location == 'bot_left' or location == 'bot_right':
            # determine starting col position
            if location == 'top_left' or location == 'bot_left': 
                col = 0
            elif location == 'top_right' or location == 'bot_right': 
                col = self.mag_horiz*4
            # determine starting row position
            if location == 'top_left' or location == 'top_right': 
                row = 0
            elif location == 'bot_left' or location == 'bot_right': 
                row = self.mag_vert*2
            # draw according to magification ratio
            for offset in range(self.mag_horiz):
                self.line(row, col + offset, self.mag_vert*3,
                          PixelArray.DIR_DOWN, self.digit)


def main():
    pass


if __name__ == '__main__':
    main()
