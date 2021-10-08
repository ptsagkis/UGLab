import sys


class Progress:
    """
    Class to support progress bar notification
    """

    def __init__(self, bar_length=60):
        self.bar_length = bar_length

    def progress(self, count, total, prefix='', suffix=''):
        """
        prints a progress bar on the console
        :param count:
        :param total:
        :param prefix:
        :param suffix:
        :return:
        """
        bar_len = self.bar_length
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '#' * filled_len + '-' * (bar_len - filled_len)

        fmt = '%s[%s] %s%s ...%s' % (prefix, bar, percents, '%', suffix)
        print('\b' * len(fmt), end='')  # clear the line
        sys.stdout.write(fmt)
        sys.stdout.flush()
