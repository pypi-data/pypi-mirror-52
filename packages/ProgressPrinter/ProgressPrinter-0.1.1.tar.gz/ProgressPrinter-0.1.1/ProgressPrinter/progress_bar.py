"""
.. py:module:: ProgressPrinter.ProgressBar
   :synopsis: A versatile progress bar for the command line.
.. moduleauthor:: Yannic Wehner <yannic.wehner@elcapitan.io>
.. License: MIT

"""

import sys

__author__ = "Yannic Wehner <yannic.wehner@elcapitan.io>"
__version_info__ = (0, 1, 1)
__version__ = '.'.join(map(str, __version_info__))


class ProgressBar:
    """
    Class that prints a versatile progress bar to the console
    """

    def __init__(self, units, unit_type='', length=50, pre='', post='', fill='=', head='>', empty=' '):
        """
        Initializes a ProgressBar object.

        :param units: The length of the progress to show e.g. 10 for 10 files.
        :param unit_type: The type (plural) of the units previously specified e.g. files, bytes. Omitted if not set.
        :param length: The length of the progress bar (really... I'm only talking about the bar). Defaults to 50.
        :param pre: A string that is printed before the initial empty progress bar is shown. Omitted by default.
        :param post: A string that is printed after the progress bar finished. Omitted by default.
        :param fill: The string that is used to fill the body of the advancing progress bar. Defaults to '='.
        :param head: A string that if not emtpy is displayed as the head of the advancing progress bar. Defaults to '>'.
        :param empty: A string that is used to fill the empty space that is not filled by the progress bar. Defaults to
                      spaces.

        """

        self.steps = length / units
        self.length = length
        self.units = units
        self.unit_type = unit_type
        self.pre = pre
        self.post = post
        self.fill = fill
        self.head = head
        self.empty = empty
        self.float_flag = False

    def print_progress(self, current_unit=0, pre=''):
        """
        Method to start printing the previously set-up progress bar.
        Call without current_unit and pre before starting whatever you want to track with the progress bar
        to initialize the progress bar to the terminal (show an emtpy progress bar).

        :param current_unit: The current progress unit to display in the bar. Defaults to 0.
        :param pre: A string that is appended to the console output above the progress bar. Useful to display additional
                    information like file names. Omitted by default.

        """

        if type(self.units) == float or type(current_unit) == float or self.float_flag:
            self.float_flag = True
            info_text = '] - Finished {:.2f} {} of {:.2f} {}  '.format(float(current_unit), self.unit_type,
                                                                          float(self.units), self.unit_type)
        else:
            info_text = '] - Finished {} {} of {} {}  '.format(current_unit, self.unit_type, self.units,
                                                                  self.unit_type)
        if self.head != '' and current_unit != 0:
            progress = self.fill * (round(current_unit * self.steps) - 1) + self.head
        else:
            progress = self.fill * round(current_unit * self.steps)
        empty = self.empty * (self.length - len(progress))
        if current_unit == 0:
            if self.pre != '':
                sys.stdout.write('\n' + self.pre + '\n')
            if pre != '':
                sys.stdout.write(pre + '\n')
            sys.stdout.write('[' + progress + empty + info_text)
        else:
            if pre != '':
                sys.stdout.write('\r' + pre + ' ' * (self.length + len(info_text) - len(pre)) + '\n')
                sys.stdout.write('[' + progress + empty + info_text)
            else:
                sys.stdout.write('\r[' + progress + empty + info_text)
        if current_unit == self.units:
            sys.stdout.write('\n')
            if self.post != '':
                sys.stdout.write(self.post + '\n\n')
            self.float_flag = False
        sys.stdout.flush()
