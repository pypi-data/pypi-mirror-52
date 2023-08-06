# Chronos
Utilities for parsing time strings in Python.

## Building and installation

Before installing chronos you will have to generate some of its
modules as it is explained in [Chronos readme](../readme.md)
Then, you can simply run

```shell
pip install bigml-chronos
```

## Requirements
Python 2.7 and Python 3 are currently supported.

The basic third-party dependencies are
[isoweek](https://pypi.org/project/isoweek/) and
[pytz](http://pytz.sourceforge.net/). These libraries are
automatically installed during the setup.

## Running the tests
The tests will be run using nose, that is installed on setup. You can
run the test suite simply by issuing

```shell
python setup.py nosetests
```

## Basic methods
Chronos offers the following main functions:

  - With **parse** you can parse a date. You can specify a format name
    with `format_name`, a list of possible format names with
    `format_names` or not specify any format. In the last case, `parse`
    will try all the possible formats until it finds the correct one:

    ```python
    from chronos import chronos
    chronos.parse("1969-W29-1", format_name="week-date")
    ```

    ```python
    from chronos import chronos
    chronos.parse("1969-W29-1", format_names=["week-date", "week-date-time"])
    ```

    ```python
    from chronos import chronos
    chronos.parse("7-14-1969 5:36 PM")
    ```

  - You can also find the format_name from a date with **find_format**:

    ```python
    from chronos import parser
    chronos.find_format("1969-07-14Z")
    ```

If both `format_name` and `format_names` are passed, it will try all the
possible formats in `format_names` and `format_name`.

You can find all the supported formats, and an example for each one of
them inside the [test file](./bigml/chronos/tests/test_chronos.py).
