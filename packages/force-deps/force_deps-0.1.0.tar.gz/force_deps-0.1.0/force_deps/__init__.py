from collections import abc
import importlib
import functools
from typing import Union, Iterable


def requires(pkg_name: str):
    """
    *Only* runs a function or initializes a class if a package is available in your environment.

    Parameters
    ----------
    pkg_name
        The name of the required package. This should not be an import as name
        or a module name. For instance, if you need to import pandas, you
        should run `@requires("pandas")`, not `@requires("pd")`.

    Raises
    ------
    ImportError
        If you cannot import the function (i.e. you have not installed it in
        your current environment)
    ValueError:
        If the package name is not a string
    """
    if not isinstance(pkg_name, str):
        # ignore coverage here because decorators get loaded before with raises test
        # and it's obvious what's happening
        raise TypeError(
            "You must enter a string into this decorator"
        )  # pragma: no cover

    def outer_wrapper(func):
        @functools.wraps(func)
        def run_function(*args, **kwargs):
            if importlib.util.find_spec(pkg_name) is None:
                raise ImportError(
                    "You must import `{}` in order to run `{}`".format(
                        pkg_name, func.__name__
                    )
                )
            return func(*args, **kwargs)

        return run_function

    return outer_wrapper


def requires_any(pkg_names: Union[Iterable[str], str]):
    """
    Runs a function if *any* item passed through the decorator is available in your environment.

    Guaranteed to return the function if the iterable
    passed through is empty (e.g. []).

    Parameters
    ----------
    opt_package_name
        Either the name of an individual package or the name of a list of packages

    Raises
    ------
    ImportError
        Only if you can't import a single one of the packages.
    ValueError:
        If you do not pass either a string or a collection of strings to this decorator
    """

    def outer_wrapper(func):
        @functools.wraps(func)
        def run_function(*args, **kwargs):
            if isinstance(pkg_names, str):
                return requires(pkg_names)(func)(*args, **kwargs)
            elif isinstance(pkg_names, abc.Iterable):
                if len(list(pkg_names)) == 0:
                    return func(*args, **kwargs)
                for pkg in pkg_names:
                    try:
                        return requires(pkg)(func)(*args, **kwargs)
                    # If there's a ValueError from requires, that still gets raised
                    # Otherwise, continue
                    except ImportError:
                        continue
                raise ImportError(
                    "None of `{}` has been installed in your environment".format(
                        ", ".join(pkg_names)
                    )
                )
            else:
                raise ValueError(
                    "This decorator requires a string or an Iterable"
                )  # pragma: no cover

        return run_function

    return outer_wrapper


def requires_all(pkg_names: Union[Iterable[str], str]):
    """Returns a function only if *all* the packages specified have been installed

    Guaranteed to return the function if the iterable
    passed through is empty (e.g. []).

    Parameters
    ----------
    opt_package_name
        Either the name of an individual package or the name of a list of packages

    Raises
    ------
    ImportError
        Only if you can't import a single one of the packages.
    ValueError:
        If you do not pass either a string or a collection of strings to this decorator
    """

    def outer_wrapper(func):
        @functools.wraps(func)
        def run_function(*args, **kwargs):
            if isinstance(pkg_names, str):
                return requires(pkg_names)(func)(*args, **kwargs)
            elif isinstance(pkg_names, abc.Iterable):
                for pkg in pkg_names:
                    if importlib.util.find_spec(pkg) is None:
                        raise ImportError(
                            "You must import `{}` in order to run `{}`".format(
                                pkg, func.__name__
                            )
                        )
                return func(*args, **kwargs)
            else:
                raise ValueError(
                    "This decorator requires a string or an Iterable"
                )  # pragma: no cover

        return run_function

    return outer_wrapper
