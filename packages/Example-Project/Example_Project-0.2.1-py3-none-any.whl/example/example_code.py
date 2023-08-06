from random import randint


def random_number_generator(start, stop):
    """Returns a random number between start and stop.

    Parameters
    ----------
    start : int
        Lowest possible number.
    stop : int
        Highest possible number.

    Returns
    -------
    int
        A random integer between start and stop.

    Examples
    --------
    >>> random_number_generator(0, 10)
    5  #random

    """
    return randint(start, stop)


def random_sequence_generator(length, start, stop):
    """Returns a list of random numbers between start and stop.

    Parameters
    ----------
    length : int
        Length of the list.
    start : int
        Lowest possible number.
    stop : int
        Highest possible number.

    Returns
    -------
    list
        A list of random integers between start and stop.

    Raises
    ------
    ValueError
        If length < 1

    Examples
    --------
    >>> random_sequence_generator(5, 0, 10)
    [3, 4, 9, 5, 2]  #random

    """
    python_list = []
    for _x in range(length):
        python_list.append(randint(start, stop))

    if length < 1:
        raise ValueError('Sequence must be longer than 1')
    return python_list
