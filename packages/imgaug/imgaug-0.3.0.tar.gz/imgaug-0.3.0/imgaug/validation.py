"""Helper functions to validate input data and produce error messages."""
import imgaug as ia


def convert_iterable_to_string_of_types(iterable_var):
    """Convert an iterable of values to a string of their types.

    Parameters
    ----------
    iterable_var : iterable
        An iterable of variables, e.g. a list of integers.

    Returns
    -------
    str
        String representation of the types in `iterable_var`. One per item
        in `iterable_var`. Separated by commas.

    """
    types = [type(var_i) for var_i in iterable_var]
    return ", ".join(types)


def is_iterable_of(iterable_var, classes):
    """Check whether `iterable_var` contains only instances of given classes.

    Parameters
    ----------
    iterable_var : iterable
        An iterable of items that will be matched against `classes`.

    classes : type or iterable of type
        One or more classes that each item in `var` must be an instanceof.
        If this is an iterable, a single match per item is enough.

    Returns
    -------
    bool
        Whether `var` only contains instances of `classes`.
        If `var` was empty, ``True`` will be returned.

    """
    if not ia.is_iterable(iterable_var):
        return False

    for var_i in iterable_var:
        if not isinstance(var_i, classes):
            return False

    return True


def assert_is_iterable_of(iterable_var, classes):
    """Assert that `iterable_var` only contains instances of given classes.

    Parameters
    ----------
    iterable_var : iterable
        See :func:`imgaug.validation.is_iterable_of`.

    classes : type or iterable of type
        See :func:`imgaug.validation.is_iterable_of`.

    """
    assert is_iterable_of(iterable_var, classes), (
        "Expected an iterable of the following types: %s. "
        "Got an iterable of types: %s." % (
            (
                ", ".join([class_.__name__ for class_ in classes])
                if not isinstance(classes, type)
                else classes.__name__
            ),
            convert_iterable_to_string_of_types(iterable_var))
    )
