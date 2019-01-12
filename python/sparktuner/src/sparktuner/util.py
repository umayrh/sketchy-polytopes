

class InvalidSize(Exception):
    ERROR_STR = "Size must be specified as bytes (b), " \
                "kibibytes (k), mebibytes (m), gibibytes (g), " \
                "tebibytes (t), or pebibytes(p). " \
                "E.g. 50b, 100kb, or 250mb."


class Util:
    """
    Utilities here may be available in other packages (such as 'humanfriendly'
    and 'humanize' but these are tailored for this package, and also avoid the
    non-essential requirements.
    """
    @staticmethod
    def format_size(bytes):
        """
        This function formats sizes in bytes, kibibytes (k), mebibytes (m),
        gibibytes (g), tebibytes (t), or pebibytes(p). The format itself:
            a. contains only integral values,
            b. preserves, where possible, four significant figures
               to account for rounding errors, and
            c. converts to a byte string format that Spark finds
              readable. See Apache Spark's
              src/main/java/org/apache/spark/network/util/JavaUtils.java#L276
        Some examples:

        > format_size(0)
        '0b'
        > format_size(5)
        '5b'
        > format_size(1024)
        '1kb'
        > format_size(10240)
        '10kb'
        > format_size(1024 ** 3 * 4)
        '4gb'
        > format_size(int(1024 ** 3 * 4.12))
        '4218mb'

        :param bytes: a :class:`int` representing the number of bytes
        :return: a human-readable, :class:`str` representation of the
        input number of bytes
        """
        if not isinstance(bytes, int):
            raise InvalidSize("Input bytes must be integral")

        num = bytes
        for x in ['b', 'kb', 'mb', 'gb', 'tb']:
            if num < 1024:
                return "%d%s" % (num, x)
            if num != int(num) and num <= 9999:
                return "%d%s" % (num, x)
            num /= 1024.0
        return "%d%s" % (num, 'pb')

    @staticmethod
    def parse_size():
        pass
