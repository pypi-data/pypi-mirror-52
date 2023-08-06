"""
.. py:module:: ProgressPrinter.ByteProgressBar
   :synopsis: A versatile progress bar for the command line.
.. moduleauthor:: Yannic Wehner <yannic.wehner@elcapitan.io>
.. License: MIT

"""

from enum import IntEnum

from ProgressPrinter import ProgressBar

__author__ = "Yannic Wehner <yannic.wehner@elcapitan.io>"
__version_info__ = (0, 1, 1)
__version__ = '.'.join(map(str, __version_info__))


class ByteProgressBar(ProgressBar):
    """
    This class extends the base ProgressBar module and adds unit conversion capabilities for working with bytes.
    """

    POWER_LABELS = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    class UNITS(IntEnum):
        """
        This enum represents the conversion units available to the ByteProgressBar.
        """
        BYTES = 0
        KILOBYTES = 1
        MEGABYTES = 2
        GIGABYTES = 3
        TERABYTES = 4
        AUTO = 5

    def __init__(self, byte_size, conversion=UNITS.AUTO, length=50, pre='', post='', fill='=', head='>', empty=' '):
        """
        Initializes a ByteProgressBar object.

        :param byte_size: The length of the progress to show in bytes
        :param conversion: The unit to convert the bytes to for display. Omit to automatically infer the best unit from
                           the byte size. For supported values see the UNITS enum.
        :param length: The length of the progress bar (really... I'm only talking about the bar). Defaults to 50.
        :param pre: A string that is printed before the initial empty progress bar is shown. Omitted by default.
        :param post: A string that is printed after the progress bar finished. Omitted by default.
        :param fill: The string that is used to fill the body of the advancing progress bar. Defaults to '='.
        :param head: A string that if not emtpy is displayed as the head of the advancing progress bar. Defaults to '>'.
        :param empty: A string that is used to fill the empty space that is not filled by the progress bar. Defaults to
                      spaces.

        """

        self.conversion = conversion

        if conversion == ByteProgressBar.UNITS.AUTO:
            unit = ByteProgressBar._get_auto_unit(byte_size)
            self.conversion = unit

        super(ByteProgressBar, self).__init__(ByteProgressBar._format_bytes(byte_size, self.conversion),
                                              ByteProgressBar.POWER_LABELS[self.conversion],
                                              length, pre, post, fill, head, empty)

    def print_progress(self, current_byte=0, pre=''):
        """
        Method to start printing the previously set-up progress bar with the converted values.
        Call without current_byte and pre before starting whatever you want to track with the progress bar
        to initialize the progress bar to the terminal (show an emtpy progress bar).

        :param current_byte: The current byte progress to display in the bar. Defaults to 0.
        :param pre: A string that is appended to the console output above the progress bar. Useful to display additional information like file names. Omitted by default.

        """

        super(ByteProgressBar, self).print_progress(ByteProgressBar._format_bytes(current_byte, self.conversion), pre)

    @staticmethod
    def _format_bytes(size, unit):
        base = 1024
        n = 0

        if unit == ByteProgressBar.UNITS.AUTO:
            while size > base:
                size /= base
                n += 1
        else:
            while n < unit:
                size /= base
                n += 1
            return size

    @staticmethod
    def _get_auto_unit(size):
        base = 1024
        n = 0
        while size > base:
            size /= base
            n += 1
        return n
