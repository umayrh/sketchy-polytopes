class InvalidSize(Exception):
    ERROR_STR = "Size must be specified as bytes (b), " \
                "kibibytes (k), mebibytes (m), gibibytes (g), " \
                "tebibytes (t), or pebibytes(p). " \
                "E.g. 50b, 100kb, or 250mb."


class Util:
    """
    Utilities here may be available in other packages (such as 'humanfriendly'
    and 'humanize') but these are tailored for this package, and also avoid the
    non-essential requirements.
    """
    @staticmethod
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    @staticmethod
    def format_size(num_bytes, units=""):
        """
        This function formats sizes in bytes, kibibytes (k), mebibytes (m),
        gibibytes (g), tebibytes (t), or pebibytes(p). The format itself:
            a. contains only integral values,
            b. preserves, where possible, four significant figures
               to account for rounding errors, and
            c. converts to a byte string format that Spark finds
              readable. See Apache Spark's
              src/main/java/org/apache/spark/network/util/JavaUtils.java#L276
        Note that, in case of float values, the function doesn't round to avoid
        going out of some arbitrary min-max bounds.
        The choice of units in ('b', 'k', 'm', 'g', 't', 'p') instead of
        ('b', 'kb', 'mb', 'gb', 'tb', 'pb') was constrained by by JVM's format
        for heap size arguments (Xms and Xmx).

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

        :param num_bytes: a :class:`int` representing the number of bytes
        :param units: units to express the number bytes in. Must be a value
        in the set ('b', 'k', 'm', 'g', 't', 'p'), and defaults
        to an empty string allowing the function to choose an appropriate
        representation. The given unit may be ignored if it results in
        'significant' rounding error.
        :return: a human-readable, :class:`str` representation of the
        input number of bytes
        """
        if not isinstance(num_bytes, int):
            raise InvalidSize("Input bytes must be integral")

        num = num_bytes
        for x in ['b', 'k', 'm', 'g', 't']:
            if x == units or num < 1024 or (num != int(num) and num <= 9999):
                return "%d%s" % (num, x)
            num /= 1024.0
        return "%d%s" % (num, 'p')

    @staticmethod
    def parse_size():
        pass
